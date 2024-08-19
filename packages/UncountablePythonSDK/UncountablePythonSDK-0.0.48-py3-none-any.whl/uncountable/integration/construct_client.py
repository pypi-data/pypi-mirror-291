import os

from uncountable.core import AuthDetailsApiKey, Client
from uncountable.core.client import ClientConfig
from uncountable.core.types import AuthDetailsAll
from uncountable.types.job_definition_t import (
    AuthRetrievalEnv,
    ProfileMetadata,
)


def _get_env_var(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise Exception(f"environment variable {name} is missing")
    return value


def _construct_auth_details(profile_meta: ProfileMetadata) -> AuthDetailsAll:
    match profile_meta.auth_retrieval:
        case AuthRetrievalEnv():
            api_id = _get_env_var(f"UNC_PROFILE_{profile_meta.name.upper()}_API_ID")
            api_secret_key = _get_env_var(
                f"UNC_PROFILE_{profile_meta.name.upper()}_API_SECRET_KEY"
            )

            assert api_id is not None
            assert api_secret_key is not None

            return AuthDetailsApiKey(api_id=api_id, api_secret_key=api_secret_key)


def _construct_client_config(profile_meta: ProfileMetadata) -> ClientConfig | None:
    if profile_meta.client_options is None:
        return None
    return ClientConfig(
        allow_insecure_tls=profile_meta.client_options.allow_insecure_tls,
        extra_headers=profile_meta.client_options.extra_headers,
    )


def construct_uncountable_client(profile_meta: ProfileMetadata) -> Client:
    return Client(
        base_url=profile_meta.base_url,
        auth_details=_construct_auth_details(profile_meta),
        config=_construct_client_config(profile_meta),
    )
