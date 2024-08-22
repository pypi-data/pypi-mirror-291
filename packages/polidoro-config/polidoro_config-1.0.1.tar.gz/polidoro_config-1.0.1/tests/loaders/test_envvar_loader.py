from pconfig.config import ConfigBase
from pconfig.config_value import ConfigValue


def test_get_from_environ(monkeypatch):
    monkeypatch.setenv("MY_ENV", "my_value")

    class ConfigTest(ConfigBase):
        MY_ENV = None
        MY_DEFAULT_VALUE = "default_value"

    assert ConfigTest.MY_ENV == "my_value"
    assert ConfigTest.MY_DEFAULT_VALUE == "default_value"


def test_config_from_env(monkeypatch):
    monkeypatch.setenv("config", '{"var1": 1}')

    class ConfigTest(ConfigBase):
        config = ConfigValue(var1=None, var2="default")

    assert ConfigTest.config.var1 == 1
    assert ConfigTest.config.var2 == "default"


def test_complex_config_from_env(monkeypatch):
    monkeypatch.setenv("config", '{"var1": {"var2": 2}}')

    class ConfigTest(ConfigBase):
        config = ConfigValue(var1=ConfigValue(var2="default"))

    assert ConfigTest.config.var1.var2 == 2
