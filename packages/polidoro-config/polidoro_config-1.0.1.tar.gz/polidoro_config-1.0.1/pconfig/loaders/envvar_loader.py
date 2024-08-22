"""
Module: dotenv_loader.py
This module provides functionality for load configuration from dotenv files
"""

import os
import sys
from typing import Any

from pconfig.loaders.loader import ConfigLoader


class ConfigEnvVarLoader(ConfigLoader):
    """
    Load the configuration values from environment variables.
    ::

        # script.py
        from pconfig import ConfigBase

        class Config(ConfigBase):
          MY_VAR = 'default_value'

        print(Config.MY_VAR)

    .. code-block:: bash

        $ python script.py
        default_value

        $ MY_VAR="new_value" python script.py
        new_value
    """

    order = -sys.maxsize

    @classmethod
    def load_config(cls, **_kwargs) -> dict[str, Any]:
        """Return the environment variables as ``dict``

        Returns:
            The configuration ``dict``
        """
        return dict(os.environ)
