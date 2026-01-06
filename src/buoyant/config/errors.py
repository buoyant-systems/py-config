from pydantic import ValidationError


class ModularConfigError(Exception):
    """Base mixin for all errors raised by py-config"""

    pass


class ConfigFileError(ModularConfigError):
    """An error with a configuration file"""

    config_path: str

    def __init__(self, config_path: str, error: str):
        self.config_path = config_path
        super().__init__(error)


class ConfigSectionMissingError(ModularConfigError):
    """Configuration file is missing a required section"""

    config_path: str
    section: str

    def __init__(self, config_path: str, section: str):
        self.config_path = config_path
        self.section = section
        super().__init__(f"Config file missing required section '{self.section}'")


class ConfigValueError(ModularConfigError, ValidationError):
    """An invalid value within a configuration section"""

    config_path: str
    section: str | None

    def __init__(
        self, config_path: str, section: str | None, original_error: ValidationError
    ):
        self.config_path = config_path
        self.section = section
        
        # Special sauce for remaining a working pydantic.ValidationError, which is unusual
        new_instance = ValidationError.from_exception_data(
            title=original_error.title,
            line_errors=original_error.errors(), # pyright: ignore[reportArgumentType]
        )
        self.__dict__.update(new_instance.__dict__)
        for slot in getattr(new_instance, "__slots__", []):
            setattr(self, slot, getattr(new_instance, slot))


class SecretChecksumFailed(ModularConfigError):
    secret: str
    expected_checksum: str | int
    actual_checksum: str | int

    def __init__(
        self, secret: str, expected_checksum: str | int, actual_checksum: str | int
    ):
        super().__init__(
            f"Checksum did not match while fetching secret '{secret}'. Expected: {expected_checksum}, got: {actual_checksum}"
        )
