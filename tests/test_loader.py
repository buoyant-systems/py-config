import pytest

from buoyant.config import ModularConfig
from buoyant.config._loader import load
from buoyant.config.errors import ConfigFileError


class InvalidConfigTest(ModularConfig):
    value: str


def test_missing_file():
    path = "./tests/test.nonexistent.yaml"
    with pytest.raises(
        ConfigFileError,
        check=lambda e: e.config_path == path,
        match="Config file not found",
    ):
        load(InvalidConfigTest, path, None, None)


def test_invalid_yaml_file():
    path = "./tests/test.unsafeyaml.yaml"
    with pytest.raises(
        ConfigFileError,
        check=lambda e: e.config_path == path,
        match="Config file not valid yaml",
    ):
        load(InvalidConfigTest, path, None, None)


def test_invalid_config_file():
    path = "./tests/test.invalidconfig.yaml"
    with pytest.raises(
        ConfigFileError,
        check=lambda e: e.config_path == path,
        match="Config file not valid config: SingleKeyNoValue",
    ):
        load(InvalidConfigTest, path, None, None)

def test_invalid_nonstring_keys_file():
    path = "./tests/test.nonstringkeys.yaml"
    with pytest.raises(
        ConfigFileError,
        check=lambda e: e.config_path == path,
        match="Config file contains non-string keys: {0: 'nonstringkey'}",
    ):
        load(InvalidConfigTest, path, None, None)