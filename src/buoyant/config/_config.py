from typing import ClassVar, Self

from pydantic import (
    BaseModel,
)

from buoyant.config._loader import load


class ModularConfig(BaseModel):
    CONFIG_PATH: ClassVar[str]
    CONFIG_SECTION: ClassVar[str | None] = None
    CONFIG_PATH_FROM_ENV_VAR: ClassVar[str | None] = None
    """If present overrides the path with the value from the env var specified"""

    @classmethod
    def load(cls) -> Self:
        return load(
            cls,
            cls.CONFIG_PATH,
            cls.CONFIG_SECTION,
            cls.CONFIG_PATH_FROM_ENV_VAR,
        )
