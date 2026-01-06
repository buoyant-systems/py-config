from typing import Literal

from buoyant.config import ModularConfig


class ConfigBase(ModularConfig):
    CONFIG_PATH = "settings.test.yaml"
    CONFIG_PATH_FROM_ENV_VAR = "SETTINGS_PATH"


class LoggingConfig(ConfigBase):
    CONFIG_SECTION = "logging"
    level: Literal["info", "warning", "error"]


class BackendConfig(ConfigBase):
    CONFIG_SECTION = "server"
    host: str
    api_key: str


def test_sample_section_logging():
    logging = LoggingConfig.load()
    assert logging.level == "info"


def test_sample_section_backend():
    backend = BackendConfig.load()
    assert backend.host == "0.0.0.0"
    assert (
        backend.api_key == "modular-config-gsm"
    )  # Does not test the GSM functionality
