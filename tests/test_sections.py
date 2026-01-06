import pytest

from buoyant.config import ModularConfig
from buoyant.config.errors import ConfigSectionMissingError


def test_no_sections():

    class NoSectionsTest(ModularConfig):
        CONFIG_PATH = "./tests/test.nosections.yaml"
        value: str
        
    config = NoSectionsTest.load()
    assert config.value == "nosections"

def test_sections():

    class SectionsTest(ModularConfig):
        CONFIG_PATH = "./tests/test.sections.yaml"
        CONFIG_SECTION = "section"
        value: str

    config = SectionsTest.load()
    assert config.value == "section"

def test_missing_section():

    class MissingSectionsTest(ModularConfig):
        CONFIG_PATH = "./tests/test.sections.yaml"
        CONFIG_SECTION = "missing-section"
        value: str

    with pytest.raises(
        ConfigSectionMissingError,
        check=lambda e: e.config_path == MissingSectionsTest.CONFIG_PATH and e.section == MissingSectionsTest.CONFIG_SECTION,
    ):
        MissingSectionsTest.load()


def test_missing_section_work_with_default_values():

    class MissingSectionsTest(ModularConfig):
        CONFIG_PATH = "./tests/test.sections.yaml"
        CONFIG_SECTION = "missing-section"
        value: str = "but has a default"

    config = MissingSectionsTest.load()
    assert config.value == "but has a default"