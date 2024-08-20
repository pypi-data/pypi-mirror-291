import os

from uncountable.types.job_definition_t import ProfileMetadata
from uncountable.types.secret_retrieval_t import (
    SecretRetrieval,
    SecretRetrievalAWS,
    SecretRetrievalEnv,
)


class SecretRetrievalError(BaseException):
    def __init__(
        self, secret_retrieval: SecretRetrieval, message: str | None = None
    ) -> None:
        self.secret_retrieval = secret_retrieval
        self.message = message

    def __str__(self) -> str:
        append_message = ""
        if self.message is not None:
            append_message = f": {self.message}"
        return f"{self.secret_retrieval.type} secret retrieval failed{append_message}"


def retrieve_secret(
    secret_retrieval: SecretRetrieval, profile_metadata: ProfileMetadata
) -> str:
    match secret_retrieval:
        case SecretRetrievalEnv():
            env_name = (
                f"UNC_{profile_metadata.name.upper()}_{secret_retrieval.env_key.upper()}"
            )
            secret = os.environ.get(env_name)
            if secret is None:
                raise SecretRetrievalError(
                    secret_retrieval, f"environment variable {env_name} missing"
                )
            return secret
        case SecretRetrievalAWS():
            raise NotImplementedError("aws secret retrieval not yet implemented")
