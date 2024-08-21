"""
Module: error.py

This module contains all the exceptions for pconfig.
"""


class ConfigError(AttributeError):
    """Raised when the config attribute is not found."""


class MissingConfig(AttributeError):
    """Raised when a config is missing."""
