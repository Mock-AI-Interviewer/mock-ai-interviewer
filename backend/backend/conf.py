import os
import logging
import os
from dotenv import load_dotenv


def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
    )


def load_environment():
    """
    In production environments, environment variables are set outside of the application.
    In local environments, environment variables are set in a .env file.
    This function loads environment variables from a .env file if it exists.
    """
    load_dotenv(dotenv_path=get_dot_env_path())


def initialise():
    setup_logging()
    load_environment()


def get_root_package_path():
    return os.path.dirname(os.path.realpath(__file__))


def get_dot_env_path():
    """Return the path to the .env file"""
    return os.path.join(os.path.dirname(get_root_package_path()), ".env")


def get_openai_api_key():
    return os.getenv("OPENAI_API_KEY")


def get_openai_organisation():
    return os.getenv("OPENAI_ORGANIZATION")


def get_openai_model():
    return os.getenv("OPENAI_MODEL")
