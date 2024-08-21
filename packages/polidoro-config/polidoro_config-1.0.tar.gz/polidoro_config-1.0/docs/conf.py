"""
Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html

-- Project information -----------------------------------------------------
https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
"""

import os
import sys
from string import Template

sys.path.insert(0, os.path.abspath("../"))
sys.path.insert(0, os.path.abspath("../pconfig"))

from pconfig import loaders

project = "Polidoro Config"
copyright = "2024, Heitor Polidoro"
author = "Heitor Polidoro"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx_copybutton",
    "sphinx.ext.napoleon",
]
myst_enable_extensions = ["colon_fence", "fieldlist"]

pygments_style = "sphinx"

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Whether to prepend module names to object names in `.. autoclass::` etc.
add_module_names = False
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "titles_only": True,
}

napoleon_google_docstring = True
autodoc_member_order = "bysource"


def generate_class_doc(clazz):
    template = """$className
==================

.. currentmodule:: $module
.. autoclass:: $className
  :show-inheritance:
  :members:
"""
    return Template(template).substitute(
        className=clazz.__name__, module=clazz.__module__
    )


def generate_module_docs(module, path=".", exclude=None):
    exclude = exclude or []
    for clazz in vars(module).values():
        if isinstance(clazz, type) and clazz.__name__ not in exclude:
            file_name = clazz.__module__.replace(f"{module.__package__}.", "") + ".rst"

            content = generate_class_doc(clazz)
            with open(os.path.join(path, file_name), "w") as file:
                file.write(content)


generate_module_docs(loaders, "classes", exclude=["ConfigEnvVarLoader", "ConfigLoader"])
