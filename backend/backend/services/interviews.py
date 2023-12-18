import logging
from datetime import datetime
from typing import List, Optional

from pydantic import ValidationError

from backend import conf
from backend.converters import interviews as model_converter
from backend.db.dao import interviews as dao
from backend.db.models import interviews as db_models
from backend.models import interviews as models
from backend.models import llm as llm_models
from backend.services import llm as llm_service
from backend.services import tokens as tokens_service

LOGGER = logging.getLogger(__name__)


def create_interview_session(
    interview_config: models.InterviewSessionCreate,
) -> models.InterviewSessionRead:
    """Create an interview session with the given configuration"""

    dao.get_interview_type(
        interview_config.interview_type.name
    )  # Check if interview type exists

    role = db_models.ConversationEntryRole.SYSTEM.value
    init_text = interview_config.interview_type.init_prompt
    tokens = tokens_service.calculate_tokens(init_text)
    current_time = datetime.now()

    conversation_entry = db_models.ConversationEntryEmbedded(
        role=role,
        message=init_text,
        tokens=tokens,
        start_timestamp=current_time,
        end_timestamp=current_time,
        model=db_models.ConversationEntryModel.NONE.value,
    )

    interview_session = db_models.InterviewSessionDocument(
        interview_type=interview_config.interview_type.dict(),
        user_id=interview_config.user_id,
    ).save()
    dao.add_message_to_interview_session(
        interview_id=interview_session.id, conversation_entry=conversation_entry
    )

    try:
       interview_session_read = model_converter.convert_db_interview_session_document_to_read(interview_session)
    except Exception as e:
        LOGGER.error(f"Deleting interview session {interview_session.id} due to error")
        interview_session.delete()
        raise e

    return interview_session_read


def start_interview(interview_id: str) -> models.InterviewSessionStartedRead:
    """Start an interview session"""
    interview_session = dao.get_interview_session(interview_id)
    interview_session.start_time = datetime.now()
    interview_session.save()
    return model_converter.convert_db_interview_session_document_to_read(interview_session)


def end_interview(interview_id: str) -> models.InterviewSessionFinishedRead:
    """End an interview session"""
    interview_session = dao.get_interview_session(interview_id)

    # Validate interview has started
    if interview_session.start_time is None:
        raise models.InterviewNotStartedError("Interview session has not been started yet")
    
    interview_session.end_time = datetime.now()
    interview_session.save()
    return model_converter.convert_db_interview_session_document_to_read(interview_session)


def review_interview(interview_id: str) -> models.InterviewSessionReviewRead:
    """Review an interview session
    TODO: Refactor this function as it's too big and similar to the output_handlers.py file
    """
    start_time = datetime.now()
    interview_session = dao.get_interview_session(interview_id)

    # Validate interview has finished
    if interview_session.end_time is None:
        raise models.InterviewNotFinishedError("Interview session has not been finished yet")
    if interview_session.review is not None:
        return model_converter.convert_db_interview_session_document_to_read(interview_session)

    # Get conversation history
    # Add a new entry to the end of the list with the role as SYSTEM
    # The new entry should ask the interviewer to review the interview and generate a json containing areas that matches the stsructure of InterviewSessionReviewRead
    example_output = models.InterviewReviewBase(score="A+", feedback="...")
    example_output_json = example_output.json()
    interview_spec = str(interview_session.conversation_history[0].message)
    job_description = str(interview_session.interview_type.job_description)

    prompt = _generate_review_prompt(
        example_json=example_output_json,
        interview_spec=interview_spec,
        job_description=job_description,
    )

    new_entry = db_models.ConversationEntryEmbedded(
        role=db_models.ConversationEntryRole.SYSTEM.value,
        message=prompt,
        tokens=llm_service.calculate_num_tokens(prompt),
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now(),
        model=db_models.ConversationEntryModel.NONE.value,
    )
    interview_session = dao.add_message_to_interview_session(
        interview_id=interview_id, conversation_entry=new_entry
    )

    try:
        # Generate GPT Response
        llm_messages = llm_service.generate_llm_messages_from_interview_session(
            interview_id
        )
        full_text = llm_service.get_response(
            messages=llm_messages, response_format=llm_models.ResponseFormat.JSON
        )

        # Double check if resopnse is valid
        LOGGER.info(f"Response from LLM: {full_text}")
        try:
            session_review = models.InterviewReviewBase.parse_raw(full_text)
        except ValidationError as e:
            LOGGER.error(f"Response from LLM is not valid json: {full_text}")
            LOGGER.error(e)
            session_review = models.InterviewSessionReviewRead(
                score="N/A", feedback=full_text
            )

        # Add resopnse to conversation history so the total tokens is correct
        # Also add the review to the interview session object so it can be returned and can be searched for easily later on
        message = session_review.json()
        end_time = datetime.now()

        interview_session = dao.add_message_to_interview_session(
            interview_id=interview_id,
            conversation_entry=db_models.ConversationEntryEmbedded(
                role=db_models.ConversationEntryRole.INTERVIEWER.value,
                message=message,
                tokens=llm_service.calculate_num_tokens(message),
                start_timestamp=start_time,
                end_timestamp=end_time,
                model=llm_service.get_current_model(),
            ),
        )
        interview_session = dao.add_review_to_interview_session(
            interview_id=interview_id,
            review=db_models.InterviewReviewEmbeedded(
                score=session_review.score, feedback=session_review.feedback
            ),
        )
        interview_session_read = model_converter.convert_db_interview_session_document_to_read(interview_session)
        return interview_session_read

    except Exception as e:
        # If there is an error, delete the last message from the interview session
        dao.delete_last_message_from_interview_session(interview_id=interview_id)
        raise e


def _generate_review_prompt(
    example_json: str, interview_spec: str, job_description: str
) -> str:
    """Generate a review prompt that returns the correct json output format of InterviewSessionReviewRead"""
    prompt = conf.get_review_prompt()

    prompt = _prompt_replace(
        placeholder="example_json", value=example_json, prompt=prompt
    )
    prompt = _prompt_replace(
        placeholder="interview_spec", value=interview_spec, prompt=prompt
    )
    prompt = _prompt_replace(
        placeholder="job_description", value=job_description, prompt=prompt
    )

    return prompt


def _prompt_replace(placeholder: str, value: str, prompt: str):
    """Replace a placeholder with a value inside the prompt"""
    if f"[[{placeholder}]]" not in prompt:
        LOGGER.error(prompt)
        raise ValueError(
            f"Prompt does not contain [[{placeholder}]]. Please add this to the prompt"
        )
    prompt = prompt.replace(f"[[{placeholder}]]", value)
    return prompt


def get_interview_type_read(name: str) -> models.InterviewTypeRead:
    """Get an interview type by name."""
    interview_type = dao.get_interview_type(name)
    return model_converter.convert_db_interview_type_to_read(interview_type)

def get_interview_session_read(interview_id:str) -> models.InterviewSessionRead:
    """Get an interview session by id."""
    interview_session = dao.get_interview_session(interview_id)
    return model_converter.convert_db_interview_session_document_to_read(interview_session)


def list_all_interview_types() -> List[models.InterviewTypeRead]:
    """List all available interview types"""
    all_interview_types = dao.list_all_interview_types()
    ret = []
    for interview_type in all_interview_types:
        interview_type_read = model_converter.convert_db_interview_type_to_read(
            interview_type
        )
        ret.append(interview_type_read)
    return ret

def list_all_interview_type_summaries() -> List[models.InterviewTypeSummary]:
    """List names and initial prompts of all interview types"""
    all_interview_types = dao.list_all_interview_types()
    summaries = [
        models.InterviewTypeSummary(name=interview_type.name, init_prompt=interview_type.init_prompt)
        for interview_type in all_interview_types
    ]
    return summaries