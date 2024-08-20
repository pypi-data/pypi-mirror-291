from dataclasses import dataclass

from pkgs.argument_parser import CachedParser
from uncountable.core.async_batch import AsyncBatchProcessor
from uncountable.integration.construct_client import construct_uncountable_client
from uncountable.integration.executors.executors import resolve_executor
from uncountable.integration.job import CronJobArguments, JobLogger
from uncountable.types.job_definition_t import JobDefinition, ProfileMetadata


@dataclass
class CronJobArgs:
    definition: JobDefinition
    profile_metadata: ProfileMetadata


cron_args_parser = CachedParser(CronJobArgs)


def cron_job_executor(**kwargs: dict) -> None:
    args_passed = cron_args_parser.parse_storage(kwargs)
    client = construct_uncountable_client(profile_meta=args_passed.profile_metadata)
    batch_processor = AsyncBatchProcessor(client=client)
    args = CronJobArguments(
        job_definition=args_passed.definition,
        client=client,
        batch_processor=batch_processor,
        profile_metadata=args_passed.profile_metadata,
        logger=JobLogger(
            profile_metadata=args_passed.profile_metadata,
            job_definition=args_passed.definition,
        ),
    )

    job = resolve_executor(args_passed.definition.executor, args_passed.profile_metadata)

    print(f"running job {args_passed.definition.name}")

    job.run(args=args)

    if batch_processor.current_queue_size() != 0:
        batch_processor.send()

    print(f"completed job {args_passed.definition.name}")
    submitted_batch_job_ids = batch_processor.get_submitted_job_ids()
    if len(submitted_batch_job_ids) != 0:
        print("submitted batch jobs", submitted_batch_job_ids)
