Polidoro Config
===============

Polidoro Config it is a configuration manager for you project

.. toctree::
  :hidden:

  Home <self>
  Classes <classes/index>

Usage
============
Create a class inheriting from ConfigBase

.. code:: python

  from pconfig import ConfigBase

  class Config(ConfigBase):
    MY_VAR = 'default_value'
    ...

When the class is created will load the configuration values from the :doc:`classes/loaders`.

.. code:: python

  # script.py
  from pconfig import ConfigBase

  class Config(ConfigBase):
    MY_VAR = 'default_value'

  print(Config.MY_VAR)


.. code:: bash

  $ python script.py
  default_value

  $ MY_VAR="new_value" python script.py
  new_value

See :class:`ConfigBase <pconfig.config.ConfigBase>` documentation for a more interesting usage
