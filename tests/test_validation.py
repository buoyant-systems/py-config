import pytest
from pydantic import ValidationError

from buoyant.config import ModularConfig
from buoyant.config.errors import ConfigValueError


def test_validation():
    class InvalidTypesTest(ModularConfig):
        CONFIG_PATH = "./tests/test.sections.yaml"
        CONFIG_SECTION = "section"
        value: int

    with pytest.raises(
        ConfigValueError,
        check=lambda e: e.config_path == InvalidTypesTest.CONFIG_PATH
        and e.section == InvalidTypesTest.CONFIG_SECTION,
    ):
        InvalidTypesTest.load()


def test_pydantic_validation():
    class InvalidTypesTest(ModularConfig):
        CONFIG_PATH = "./tests/test.sections.yaml"
        CONFIG_SECTION = "section"
        value: int

    val_err = None
    try:
        InvalidTypesTest.load()
    except ConfigValueError as err:
        val_err = err.validation_error

    assert isinstance(val_err, ValidationError)
    assert val_err.error_count() == 1
