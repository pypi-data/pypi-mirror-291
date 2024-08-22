from typing import Any

import pytest

from pconfig.config import ConfigBase

loader_calls = []


# noinspection PyUnusedLocal
def test_loader():
    from pconfig.loaders.loader import ConfigLoader

    class LoaderTest0(ConfigLoader):
        calls = 0

        @classmethod
        def load_config(cls) -> dict[str, Any]:
            loader_calls.append("LoaderTest0")
            cls.calls += 1
            return {"name": "value0"}

    class LoaderTest1(ConfigLoader):
        order = 100
        calls = 0

        @classmethod
        def load_config(cls) -> dict[str, Any]:
            loader_calls.append("LoaderTest1")
            cls.calls += 1
            return {"name": "value1"}

    class Config(ConfigBase):
        name = None

    assert loader_calls == ["LoaderTest0", "LoaderTest1"]
    assert Config.name == "value1"
    assert LoaderTest0.calls == 1
    assert LoaderTest1.calls == 1


# noinspection PyAbstractClass,PyUnusedLocal
def test_raise_not_implemented_error():
    from pconfig.loaders.loader import ConfigLoader

    # skipcq: PYL-W0223
    class LoaderTest(ConfigLoader):
        calls = 0

    with pytest.raises(NotImplementedError) as err:

        class Config(ConfigBase):
            name = None

    assert str(err.value) == "LoaderTest must implement this method."
    assert LoaderTest.calls == 0
    # Config class was not created
    assert "Config" not in locals()
