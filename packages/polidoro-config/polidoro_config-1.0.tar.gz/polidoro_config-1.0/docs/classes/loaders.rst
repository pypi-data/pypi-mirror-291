Loaders
=======


Loaders
------------

.. currentmodule:: pconfig.loaders.loader
.. autofunction:: load_configs


Default Loaders
---------------

.. toctree::
  :hidden:

  loader
  envvar_loader
  dotenv_loader
  yaml_loader

.. list-table::
   :header-rows: 1

   * - Class
     - Description
     - Order
   * - :class:`ConfigEnvVarLoader <pconfig.loaders.ConfigEnvVarLoader>`
     - Load configuration from Environment Variables
     - last
   * - :class:`ConfigDotEnvLoader <pconfig.loaders.ConfigDotEnvLoader>`
     - Load configuration from dot env files
     - 0
   * - :class:`ConfigYAMLLoader <pconfig.loaders.ConfigYAMLLoader>`
     - Load configuration from YAML files
     - 100
