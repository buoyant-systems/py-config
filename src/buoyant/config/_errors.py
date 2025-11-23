class ModularConfigError(Exception):
    """A known error state of Modular Config"""


class ConfigFileError(ModularConfigError):
    """An error with a configuration file"""
