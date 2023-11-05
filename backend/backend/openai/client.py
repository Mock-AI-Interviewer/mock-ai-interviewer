import logging
from typing import Optional

import openai
from dataclasses import dataclass
from backend.conf import get_openai_model

LOGGER = logging.getLogger("openai")
LOGGER.setLevel(logging.INFO)

@dataclass
class GPTSentanceResponse:
    text: str
    timestamp: str
    finish_reason: str

def get_sentance_response(
    messages: list,
    model: str = get_openai_model(),
    stream: bool = True,
    sentance_stoppers: list = [".", "?", "!", ",", "\n"],
    max_tokens=50,
):
    """
    Returns a sentance response from the OpenAI API
    Use sentance_stoppers to specify which characters should be used to end a sentance
    """
    completion = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        stream=stream,
        max_tokens=max_tokens,
    )

    full_text = []
    curr_sentance = []
    for chunk in completion:
        finish_reason = chunk.choices[0].finish_reason
        timestamp = chunk.created

        delta = chunk.choices[0].delta
        if delta and delta.content:
            content = delta.content
            curr_sentance.append(content)
            # check if any setance stoppers are in the delta
            if any(stopper in content for stopper in sentance_stoppers):
                curr_str = "".join(curr_sentance)

                yield GPTSentanceResponse(
                    text=curr_str, timestamp=timestamp, finish_reason=finish_reason
                )
                # if so, add the current sentance to the full text
                full_text.extend(curr_sentance)
                # and clear the current sentance
                curr_sentance = []
