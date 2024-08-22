import builtins
import contextlib
import importlib
import os
import pkgutil
from copy import deepcopy
from unittest.mock import patch

import pytest

from pconfig import loaders


def modules_to_reload():
    modules = [
        name
        for _, name, _ in pkgutil.iter_modules(loaders.__path__)
        if name != "loader"
    ]
    return [getattr(loaders, name) for name in ["loader"] + modules]


@pytest.fixture(autouse=True)
def reload_modules():
    yield
    for module_to_reload in modules_to_reload():
        importlib.reload(module_to_reload)


@pytest.fixture(autouse=True)
def clean_env():
    original_environ = deepcopy(os.environ)
    yield
    os.environ.clear()
    os.environ.update(original_environ)


@contextlib.contextmanager
def change_dir(destination):
    orig_dir = os.getcwd()
    os.chdir(destination)
    yield
    os.chdir(orig_dir)


original_import = builtins.__import__


@contextlib.contextmanager
def import_error(import_to_fail):
    def raise_import_error(name, *args, **kwargs):
        if name == import_to_fail:
            raise ImportError
        return original_import(name, *args, **kwargs)

    with patch("builtins.__import__", side_effect=raise_import_error):
        for module_to_reload in modules_to_reload():
            importlib.reload(module_to_reload)
        yield
