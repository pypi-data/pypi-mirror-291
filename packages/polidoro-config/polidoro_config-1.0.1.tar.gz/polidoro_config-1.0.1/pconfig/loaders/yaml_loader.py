"""
Module: file_loader.py
This module provides functionality for load configuration from file
"""

import logging
from typing import Any

from pconfig.error import ConfigError
from pconfig.loaders.loader import ConfigLoader

logger = logging.getLogger(__name__)


try:
    import yaml
except ImportError:
    yaml = None


class ConfigYAMLLoader(ConfigLoader):
    """
    Load configuration from YAML file.
    ::

        from pconfig import ConfigBase

        class Config(ConfigBase):
          file_path = "my_config.yml"
          MY_VAR = 'default_value'

        print(Config.MY_VAR)

    .. code-block:: bash

        # my_config.yml file
        MY_VAR: 'yaml_value'

        $ python script.py
        yaml_value

    """

    order = 100

    @classmethod
    def load_config(cls, file_path: str, **_kwargs) -> dict[str, Any]:
        """Load the configuration fom a YAML file.

        Args:
            file_path: YAML file path

        Returns:
            The configuration ``dict``
        """
        if yaml is None:
            raise ConfigError(
                "Must install pyyaml to use this feature. `pip install pyyaml`"
            )
        config = {}
        if file_path and (file_path.endswith(".yml") or file_path.endswith(".yaml")):
            with open(file_path, "r") as file:
                config = yaml.safe_load(file)
        return config
