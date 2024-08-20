from abc import ABC, abstractmethod
from dataclasses import dataclass

from uncountable.core.async_batch import AsyncBatchProcessor
from uncountable.core.client import Client
from uncountable.types.job_definition_t import JobDefinition, JobResult, ProfileMetadata


class JobLogger:
    def __init__(
        self, *, profile_metadata: ProfileMetadata, job_definition: JobDefinition
    ) -> None:
        self.profile_metadata = profile_metadata
        self.job_definition = job_definition

    def log_info(self, *log_objects: object) -> None:
        # IMPROVE: log a json message with context that can be parsed by OT
        print(
            f"[{self.job_definition.id}] in profile ({self.profile_metadata.name}): ",
            *log_objects,
        )


@dataclass
class JobArgumentsBase:
    job_definition: JobDefinition
    profile_metadata: ProfileMetadata
    client: Client
    batch_processor: AsyncBatchProcessor
    logger: JobLogger


@dataclass
class CronJobArguments(JobArgumentsBase):
    # can imagine passing additional data such as in the sftp or webhook cases
    pass


JobArguments = CronJobArguments


class Job(ABC):
    _unc_job_registered: bool = False

    @abstractmethod
    def run(self, args: JobArguments) -> JobResult: ...


class CronJob(Job):
    @abstractmethod
    def run(self, args: CronJobArguments) -> JobResult: ...


def register_job(cls: type[Job]) -> type[Job]:
    cls._unc_job_registered = True
    return cls
