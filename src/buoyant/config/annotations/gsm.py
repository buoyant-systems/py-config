import logging
from functools import cache, lru_cache
from typing import Callable

from google.cloud.secretmanager import SecretManagerServiceClient
from google_crc32c import Checksum
from pydantic import PlainValidator

from buoyant.config.errors import SecretChecksumFailed

_logger = logging.getLogger(__name__)


@cache
def get_gsm_client():
    return SecretManagerServiceClient()


def get_secret_value(
    project: str,
    secret_name: str,
    client_factory: Callable[[], SecretManagerServiceClient] = get_gsm_client,
) -> str:
    """
    Gets a secret from GSM, for the configured data project
    """
    secret_name = f"projects/{project}/secrets/{secret_name}/versions/latest"

    _logger.debug("Getting GSM secret %s", secret_name)
    response = client_factory().access_secret_version(  # pyright: ignore[reportUnknownMemberType]
        request={"name": secret_name}
    )

    crc32c = Checksum()
    crc32c.update(response.payload.data)  # pyright: ignore[reportUnknownMemberType]
    computed_checksum = int(crc32c.hexdigest(), 16)
    if response.payload.data_crc32c != computed_checksum:
        raise SecretChecksumFailed(
            secret=secret_name,
            expected_checksum=response.payload.data_crc32c,
            actual_checksum=computed_checksum,
        )

    return response.payload.data.decode()


def gsm_secret(
    project: str | None = None,
    secret: str | None = None,
    delimiter: str = ":",
    client_factory: Callable[[], SecretManagerServiceClient] = get_gsm_client,
):
    """
    This can be used to annotate fields on a `ModularConfig` in order to fetch their value
    from a secret in Google Secrets Manager (GSM).

    The a secret within GSM is identified by a `project` and a `secret`. By default, the value
    in the config file will be parsed as `project:secret`. A value for either can be passed
    directly with the `project` and `secret` parameters respectively. Additionally, the
    delimiter used when neither `project` nor `secret` params are supplied can be adjusted with
    the `delimiter` parameter.

    Use this by annotating the configuration field with `Annotated[str, gsm_secret()]` or
    `Annotated[str, gsm_secret(project="my-project")]`.
    """

    @lru_cache
    def _possible_gsm_key(value: str) -> str:
        if project and secret:
            return get_secret_value(
                project=project, secret_name=secret, client_factory=client_factory
            )

        params: list[str] = [
            p
            for p in [project, *value.split(sep=delimiter, maxsplit=1), secret]
            if p is not None
        ]
        return get_secret_value(*params, client_factory=client_factory)

    return PlainValidator(_possible_gsm_key)
