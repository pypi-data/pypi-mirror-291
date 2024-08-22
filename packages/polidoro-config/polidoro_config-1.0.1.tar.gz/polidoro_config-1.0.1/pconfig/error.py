"""
Module: error.py

This module contains all the exceptions for pconfig.
"""


class ConfigError(AttributeError):
    """Raised when a config error happens."""


class MissingConfig(AttributeError):
    """Raised when a config is missing."""
