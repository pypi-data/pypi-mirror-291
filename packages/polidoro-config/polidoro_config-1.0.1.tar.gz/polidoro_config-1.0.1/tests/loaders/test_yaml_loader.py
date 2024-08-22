import pytest
from pydantic import BaseModel

from pconfig.config import ConfigBase, ConfigValue
from pconfig.error import ConfigError

# noinspection PyUnresolvedReferences
from tests.conftest import change_dir, import_error


def test_load_yaml(tmp_path):
    yaml_file = tmp_path / ".yaml"
    yaml_file.write_text("LOAD_ENV_VAR: 'load_value'")

    with change_dir(tmp_path):

        class ConfigTest(ConfigBase):
            file_path = yaml_file.name
            LOAD_ENV_VAR = None

        assert ConfigTest.LOAD_ENV_VAR == "load_value"


def test_load_yaml_when_yaml_is_not_installed(tmp_path):
    # noinspection PyGlobalUndefined
    dotenv_file = tmp_path / ".env"
    dotenv_file.write_text("LOAD_ENV_VAR=load_value")

    yaml_file = tmp_path / ".yaml"
    yaml_file.write_text("LOAD_ENV_VAR: 'load_value'")

    with (
        change_dir(tmp_path),
        import_error("yaml"),
        pytest.raises(ConfigError) as c_err,
    ):
        # noinspection PyUnusedLocal
        class ConfigTest(ConfigBase):
            file_path = yaml_file.name
            LOAD_ENV_VAR = None

    assert (
        str(c_err.value)
        == "Must install pyyaml to use this feature. `pip install pyyaml`"
    )


def test_load_with_falsy_file_path():
    class ConfigTest(ConfigBase):
        file_path = None
        LOAD_ENV_VAR = None

    assert ConfigTest.LOAD_ENV_VAR is None


def test_load_without_file_path():
    class ConfigTest(ConfigBase):
        LOAD_ENV_VAR = None

    assert ConfigTest.LOAD_ENV_VAR is None


def test_load_with_not_eligible_file_path(tmp_path):
    yaml_file = tmp_path / ".not_yaml"
    yaml_file.write_text("LOAD_ENV_VAR: 'load_value'")

    with change_dir(tmp_path):

        class ConfigTest(ConfigBase):
            file_path = yaml_file.name
            LOAD_ENV_VAR = None

        assert ConfigTest.LOAD_ENV_VAR is None


def test_load_yaml_config(tmp_path):
    yaml_file = tmp_path / ".yaml"
    yaml_file.write_text(
        """config: 
        var1: 1"""
    )

    with change_dir(tmp_path):

        class ConfigTest(ConfigBase):
            file_path = yaml_file.name
            config = ConfigValue(var1=None, var2="default")

        assert ConfigTest.config.var1 == 1
        assert ConfigTest.config.var2 == "default"


def test_load_yaml_complex_config(tmp_path):
    yaml_file = tmp_path / ".yaml"
    yaml_file.write_text(
        """config: 
        var1: 
            var2: 2"""
    )

    with change_dir(tmp_path):

        class ConfigTest(ConfigBase):
            file_path = yaml_file.name
            config = ConfigValue(var1=ConfigValue(var2="default"))

        assert ConfigTest.config.var1.var2 == 2


def test_load_yaml_wrong_complex_config(tmp_path):
    yaml_file = tmp_path / ".yaml"
    yaml_file.write_text(
        """config: 
        var1: 1"""
    )

    with change_dir(tmp_path):

        class ConfigTest(ConfigBase):
            file_path = yaml_file.name
            config = ConfigValue(var1=ConfigValue(var2="default"))

        assert ConfigTest.config.var1 == 1


def test_load_yaml_complex_config_with_pydantic(tmp_path):
    yaml_file = tmp_path / ".yaml"
    yaml_file.write_text(
        """config: 
        var1: "1"
        another_config:
            another_var2: "2" """
    )

    with change_dir(tmp_path):

        class AnotherConfig(BaseModel):
            another_var1: str = "default1"
            another_var2: str = "default2"

        class MyConfig(BaseModel):
            var1: str = "default1"
            var2: str = "default2"
            another_config: AnotherConfig = AnotherConfig()

        class ConfigTest(ConfigBase):
            file_path = yaml_file.name
            config = MyConfig()

        assert ConfigTest.config.var1 == "1"
        assert ConfigTest.config.var2 == "default2"
        assert ConfigTest.config.another_config.another_var1 == "default1"
        assert ConfigTest.config.another_config.another_var2 == "2"
