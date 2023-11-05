import logging
import os

import openai
from dotenv import load_dotenv
from mongoengine import connect


def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
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
    connect(get_db_name(), host="localhost", port=27017)


def setup_openai():
    """Connect to OpenAI API"""
    openai.organization = get_openai_organisation()
    openai.api_key = get_openai_api_key()


def initialise_app():
    """Initialise the application"""
    setup_logging()
    setup_env_variables()

    setup_db_connection()
    setup_openai()


def get_root_package_path():
    return os.path.dirname(os.path.realpath(__file__))


def get_dot_env_path():
    """Return the path to the .env file"""
    return os.path.join(os.path.dirname(get_root_package_path()), ".env")


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