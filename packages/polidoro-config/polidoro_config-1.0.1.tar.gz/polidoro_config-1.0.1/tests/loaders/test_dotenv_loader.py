import importlib
from unittest.mock import Mock, patch

from pconfig.config import ConfigBase
from pconfig.loaders import dotenv_loader
from tests.conftest import change_dir, import_error


def test_load_dotenv(tmp_path):
    dotenv_file = tmp_path / ".env"
    dotenv_file.write_text("LOAD_ENV_VAR=load_value")

    with (
        change_dir(tmp_path),
        patch("dotenv.main.find_dotenv", return_value=dotenv_file),
    ):

        class ConfigTest(ConfigBase):
            LOAD_ENV_VAR = None

        assert ConfigTest.LOAD_ENV_VAR == "load_value"


def test_load_dotenv_when_dotenv_is_not_installed(tmp_path):
    dotenv_file = tmp_path / ".env"
    dotenv_file.write_text("LOAD_ENV_VAR=load_value")

    logger = Mock()
    with (
        change_dir(tmp_path),
        patch("logging.getLogger", return_value=logger),
        import_error("dotenv"),
    ):

        class ConfigTest(ConfigBase):
            LOAD_ENV_VAR = None

        assert ConfigTest.LOAD_ENV_VAR is None
        logger.info.assert_called_once_with(
            "There's a .env file present but python-dotenv is not installed. Run 'pip install python-dotenv' to use it."
        )


def test_load_dotenv_when_dotenv_is_not_installed_and_there_is_no_dot_env_file():
    logger = Mock()
    with (
        patch("logging.getLogger", return_value=logger),
        import_error("dotenv"),
    ):
        importlib.reload(dotenv_loader)

        class ConfigTest(ConfigBase):
            LOAD_ENV_VAR = None

        assert ConfigTest.LOAD_ENV_VAR is None
        logger.info.assert_not_called()


def test_load_dotenv_from_another_file(tmp_path, monkeypatch):
    dotenv_file = tmp_path / ".env"
    dotenv_file.write_text("LOAD_ENV_VAR=load_value")
    another_dotenv_file = tmp_path / ".another_env"
    another_dotenv_file.write_text("LOAD_ENV_VAR=another_load_value")
    monkeypatch.setenv("CONFIG_ENV", ".another_env")

    with change_dir(tmp_path):

        class ConfigTest(ConfigBase):
            LOAD_ENV_VAR = None

        assert ConfigTest.LOAD_ENV_VAR == "another_load_value"
