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


class ConfigValueError(ModularConfigError):
    """A configuration value does not match the defined schema"""

    config_path: str
    section: str | None
    validation_error: ValidationError

    def __init__(
        self,
        config_path: str,
        section: str | None,
        validation_error: ValidationError,
    ):
        self.config_path = config_path
        self.section = section
        self.validation_error = validation_error
        super().__init__(
            f"Configuration section incorrectly configured '{self.section}'. {self.validation_error}"
        )


class SecretChecksumFailed(ModularConfigError):
    secret: str
    expected_checksum: str | int
    actual_checksum: str | int

    def __init__(
        self, secret: str, expected_checksum: str | int, actual_checksum: str | int
    ):
        self.secret = secret
        self.expected_checksum = expected_checksum
        self.actual_checksum = actual_checksum
        super().__init__(
            f"Checksum did not match while fetching secret '{secret}'. Expected: {expected_checksum}, got: {actual_checksum}"
        )
