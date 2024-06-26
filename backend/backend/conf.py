import logging
import os
from google.oauth2 import service_account
import json
import openai
from dotenv import load_dotenv
from mongoengine import connect
from elevenlabs import set_api_key


ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
LOGGER = logging.getLogger(__name__)

_google_sa_credentials = None


def initialise_app():
    """Initialise the application"""
    setup_logging()
    setup_env_variables()

    # Setup External Services
    setup_db_connection()
    setup_openai()
    setup_google()
    setup_elevn_labs()


def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s:Line:%(lineno)d - %(levelname)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
    )


def setup_env_variables():
    """
    In production environments, environment variables are set outside of the application.
    In local environments, environment variables are set in a .env file.
    This function loads environment variables from a .env file if it exists.
    """
    load_dotenv(dotenv_path=get_dot_env_path())


def setup_db_connection():
    """Connect to MongoDB (it will create a new database if it doesn"t exist)"""
    LOGGER.info(f"Connecting to MongoDB with configuration: [{get_db_host()}]")
    connect(get_db_name(), host=get_db_host())


def setup_openai():
    """Connect to OpenAI API"""
    openai.organization = get_openai_organisation()
    openai.api_key = get_openai_api_key()


def setup_google():
    """Load Google Service Account Credentials"""
    client_file = get_google_service_account_file_path()
    with open(client_file, "r") as file:
        config = json.load(file)

    # Need to replace the escaped newlines with actual newlines
    private_key = get_google_service_account_private_key().replace("\\n", "\n")
    config["private_key"] = private_key
    config["private_key_id"] = get_google_service_account_private_key_id()

    global _google_sa_credentials
    _google_sa_credentials = service_account.Credentials.from_service_account_info(
        config
    )


def setup_elevn_labs():
    set_api_key(get_eleven_labs_api_key())


def get_root_package_path():
    return os.path.dirname(os.path.realpath(__file__))


def get_dot_env_path():
    """Return the path to the .env file"""
    return os.path.join(os.path.dirname(get_root_package_path()), ".env")


def get_db_host():
    return os.getenv("DB_HOST")


def get_db_name():
    return os.getenv("DB_NAME")


def get_openai_api_key():
    return os.getenv("OPENAI_API_KEY")


def get_openai_organisation():
    return os.getenv("OPENAI_ORGANIZATION")


def get_openai_model():
    return os.getenv("OPENAI_MODEL")


def get_eleven_labs_api_key():
    return os.getenv("ELEVEN_LABS_API_KEY")


def get_google_credentials():
    global _google_sa_credentials
    if _google_sa_credentials is None:
        _google_sa_credentials = setup_google()
    return _google_sa_credentials


def get_google_service_account_file_path():
    return os.path.join(
        get_root_package_path(), "services", "google", "service_account.json"
    )


def get_google_service_account_private_key():
    return os.getenv("GOOGLE_SA_PRIVATE_KEY")


def get_google_service_account_private_key_id():
    return os.getenv("GOOGLE_SA_PRIVATE_KEY_ID")


def get_jinja_templates_path():
    return os.path.join(get_root_package_path(), "html_templates")


def get_review_prompt():
    """Returns the review prompt for the LLM API"""
    return os.getenv("LLM_REVIEW_PROMPT")
