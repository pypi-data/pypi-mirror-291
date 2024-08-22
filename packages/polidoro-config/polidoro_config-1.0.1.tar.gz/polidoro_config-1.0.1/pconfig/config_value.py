"""
Module: config_value.py
This module provides functionality for managing configurations
It allows you to load configuration settings from various sources such as
environment variables, configuration files (e.g., YAML).
"""

from typing import Any

from typing_extensions import TypeVar

ConfigValueType = TypeVar("ConfigValue")


class ConfigValue:
    """
    A class representing a configuration value.

    This class allows updating and accessing configuration values using attribute and item notation.

    :param values: A dictionary of initial configuration values.
    :param raise_on_missing_config: If it should raise the MissingConfig exception if this configuration is missing.

    Example usage
    ::

        config = ConfigValue(config1='value1', config2='value2')
        print(config.config1)  # Output: 'value1'
        print(config['config2'])  # Output: 'value2'


    """

    def __init__(self, raise_on_missing_config: bool = True, **values) -> None:
        self.raise_on_missing_config = raise_on_missing_config
        self.values = values

    def update(self, values: dict[str, Any | dict] | Any) -> ConfigValueType | Any:
        """
        Update the configuration values with new values.

        :param values: A dictionary of new values to update the configuration.
                       The keys are the parameter names and the values are the
                       corresponding new values.

                       Each value can be one of the following:
                       - An object of any type, which will be directly set as the new value.
                       - Another dictionary, representing nested configuration values.

        :return: The updated configuration object.
                 If the input values are not a dictionary, the original configuration object is returned.
        """
        if not isinstance(values, dict):
            return values
        for name, value in values.items():
            if isinstance((self_value := self[name]), ConfigValue):
                value = self_value.update(value)
            self.values[name] = value
        return self

    def __repr__(self) -> str:
        attributes = ", ".join(f"{k}={repr(v)}" for k, v in self.values.items())
        return f"{self.__class__.__name__}({attributes})"

    def __getattr__(self, item: str) -> ConfigValueType | Any:
        return self.values[item]

    def __getitem__(self, item: str) -> ConfigValueType | Any:
        return self.values[item]
