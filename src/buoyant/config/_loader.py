import os
from contextvars import ContextVar
from functools import lru_cache
from typing import Any, Tuple

import yaml
from pydantic import BaseModel

from buoyant.config._errors import ConfigFileError

_global: ContextVar[dict[Tuple[str, str | None], BaseModel]] = ContextVar(
    "__modular_configs", default={}
)


@lru_cache
def _load_yaml(path: str) -> dict[str, Any]:
    try:
        with open(path) as config_file:
            loaded_yaml = yaml.safe_load(config_file)
    except FileNotFoundError:
        raise ConfigFileError(f"Config file not found: {path}")
    except yaml.YAMLError:
        raise ConfigFileError(f"Config file not valid yaml: {path}")
    if not isinstance(loaded_yaml, dict): # pyright: ignore[reportUnnecessaryIsInstance]
        raise ConfigFileError(f"Config file not valid config: {loaded_yaml}")
    if not all(isinstance(k, str) for k in loaded_yaml.keys()):
        raise ConfigFileError(f"Config file contains non-string keys: {loaded_yaml}")
    return loaded_yaml


def load[T: BaseModel](
    config: type[T],
    path: str,
    section: str | None,    path_from_env_var: str | None,
    cache_context: ContextVar[dict[Tuple[str, str | None], BaseModel]] = _global,
) -> T:
    if path_from_env_var:
        path = os.getenv(path_from_env_var, path)

    cache = cache_context.get()
    if (path, section) in cache:
        cached = cache[(path, section)]
        assert isinstance(cached, config)
        return cached

    loaded = _load_yaml(path)
    if section:
        for subsection in section.split("."):
            loaded = loaded.get(subsection, {})

    return config(**loaded)
