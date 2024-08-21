"""
This module is part of Polidoro Config.

It holds all the available loaders classes
"""

__all__ = [
    "ConfigLoader",
    "ConfigEnvVarLoader",
    "ConfigDotEnvLoader",
    "ConfigYAMLLoader",
]

from pconfig.loaders.dotenv_loader import ConfigDotEnvLoader
from pconfig.loaders.envvar_loader import ConfigEnvVarLoader
from pconfig.loaders.loader import ConfigLoader
from pconfig.loaders.yaml_loader import ConfigYAMLLoader
