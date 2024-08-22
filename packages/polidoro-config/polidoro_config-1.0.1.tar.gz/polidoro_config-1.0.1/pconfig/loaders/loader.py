"""
Module: loader.py
This module provides functionality for managing configuration loads
"""

import inspect
import logging
import sys
from abc import abstractmethod
from typing import Any

logger = logging.getLogger(__name__)


def load_configs(**params) -> dict[str, Any]:
    """Calls the ``load_config`` for all the ConfigLoader child classes,
    returning the consolidated configuration ``dict``.

    Args:
        params: Key word arguments to be passed as parameters to the
            :meth:`load_config() <pconfig.loaders.loader.ConfigLoader.load_config>`
            method from each loader

    Returns:
        dict[str, object]: The consolidated configuration ``dict``
    """
    config = {}
    for loader in sorted(
        ConfigLoader.__subclasses__(),
        key=lambda loader_: loader_.order,
        reverse=True,
    ):
        signature = inspect.signature(loader.load_config)
        if (filtered_params := _get_parameters(params, signature)) is not None:
            config.update(loader.load_config(**filtered_params))
    return config


def _get_parameters(
    params: dict[str, Any], signature: inspect.Signature
) -> dict[str, Any] | None:
    """
    Returns the parameters that the method needs or accepts that are in ``params`` or
    None if the method needs a parameter that is not in ``params``

    Args:
        params: The parameters to be filtered
        signature: The method signature

    Returns:
        dict[str, object] | None: The filtered parameters or None if a parameter is missing
    """
    filtered_params = {}
    for param_name, param in signature.parameters.items():
        if param_name in params:
            filtered_params[param_name] = params.get(param_name)
        elif (
            param.kind not in {param.VAR_POSITIONAL, param.VAR_KEYWORD}
            and param.default == param.empty
        ):
            return None
    return filtered_params


class ConfigLoader:
    """Loader base class.

    To create a configuration loader, create a subclass and implement the
    :meth:`load_config() <pconfig.loaders.loader.ConfigLoader.load_config>` method
    returning a ``dict`` of configuration values.
    ::

        class ConfigCustomLoader(ConfigLoader):
            order = 1  # Optional, leaving it blank will run first

            @classmethod
            def load_config(cls, **_kwargs) -> dict[str, object]:
                return {"value1": 1, "value2": 2}

    """

    order: int = sys.maxsize
    """ The order in which loaders will be called. Biggest first."""

    @classmethod
    @abstractmethod
    def load_config(cls, **kwargs) -> dict[str, Any]:
        """
        Method to be implemented by the child class. Must return a ``dict`` of configuration values.

        Returns:
            dict[str, object]: The loaded configuration ``dict``
        """
        raise NotImplementedError(f"{cls.__name__} must implement this method.")
