import importlib

import pytest
from pydantic import BaseModel

from pconfig import ConfigBase, NotSet, config
from pconfig.config_value import ConfigValue
from pconfig.error import MissingConfig
from tests.conftest import import_error


def test_when_pydantic_is_not_installed():
    # noinspection PyGlobalUndefined

    with (import_error("pydantic"),):
        importlib.reload(config)

        class ConfigTest(ConfigBase):
            LOAD_ENV_VAR = None

        assert ConfigTest.LOAD_ENV_VAR is None
        assert config.BaseModel is None
    importlib.reload(config)


def test_repr():
    class ConfigTest(ConfigBase):
        file_path = "file_name"
        config = ConfigValue(var1=ConfigValue(var2="default"))

    assert (
        str(ConfigTest)
        == "ConfigTest(file_path='file_name', config=ConfigValue(var1=ConfigValue(var2='default')))"
    )


def test_repr_pydantic():
    class AnotherConfig(BaseModel):
        another_var1: str = "default1"
        another_var2: str = "default2"

    class MyConfig(BaseModel):
        var1: str = "default1"
        var2: str = "default2"
        another_config: AnotherConfig = AnotherConfig()

    class ConfigTest(ConfigBase):
        file_path = None
        config = MyConfig()

    assert str(ConfigTest) == (
        "ConfigTest(file_path=None, config=MyConfig(var1='default1', var2='default2', "
        "another_config=AnotherConfig(another_var1='default1', another_var2='default2')))"
    )


def test_missing_config():
    class ConfigTest(ConfigBase):
        EXISTING_VAR: str = None
        VAR_WITHOUT_DEFAULT: str

    assert ConfigTest.EXISTING_VAR is None
    with pytest.raises(MissingConfig):
        assert ConfigTest.VAR_WITHOUT_DEFAULT
    with pytest.raises(MissingConfig):
        assert ConfigTest.MY_MISSING_VAR


def test_missing_config_global_dont_raise():
    class ConfigTest(ConfigBase):
        raise_on_missing_config = False
        EXISTING_VAR: str = None
        VAR_WITHOUT_DEFAULT: str
        CONFIG_VALUE: str = ConfigValue()

    assert ConfigTest.EXISTING_VAR is None
    assert ConfigTest.VAR_WITHOUT_DEFAULT == NotSet
    assert bool(ConfigTest.VAR_WITHOUT_DEFAULT) is False
    assert ConfigTest.MY_MISSING_VAR == NotSet
    assert ConfigTest.CONFIG_VALUE == NotSet


def test_missing_config_local_dont_raise():
    class ConfigTest(ConfigBase):
        EXISTING_VAR: str = None
        VAR_WITHOUT_DEFAULT_FALSE: str = ConfigValue(raise_on_missing_config=False)
        VAR_WITHOUT_DEFAULT_TRUE: str = ConfigValue(raise_on_missing_config=True)

    assert ConfigTest.EXISTING_VAR is None
    assert ConfigTest.VAR_WITHOUT_DEFAULT_FALSE == NotSet
    with pytest.raises(MissingConfig):
        assert ConfigTest.VAR_WITHOUT_DEFAULT_TRUE
    with pytest.raises(MissingConfig):
        assert ConfigTest.MY_MISSING_VAR
