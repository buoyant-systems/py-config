A modular and typed yaml configuration system for python with easy secret support

## Install ##

`pip install buoyant.config`
or
`uv add buoyant.config`

## Example Usage ##

Define your configuration in a modular fashion:
```python
from typing import Annotated, Literal

from buoyant.config import ModularConfig

class ConfigBase(ModularConfig):
    CONFIG_PATH = "settings.test.yaml"
    CONFIG_PATH_FROM_ENV_VAR = "SETTINGS_PATH"


class LoggingConfig(ConfigBase):
    CONFIG_SECTION = "logging"
    level: Literal["info", "warning", "error"]


from buoyant.config.annotations.gsm import gsm_secret

class BackendConfig(ConfigBase):
    CONFIG_SECTION = "server"
    host: str
    api_key: Annotated[str, gsm_secret(project="buoyant-open-projects")]
```

Use it easily:
```python
config = BackendConfig.load()
config.host
```
