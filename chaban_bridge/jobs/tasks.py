# Third-party
from celery.schedules import crontab

# Application
from chaban_bridge.celery import celery_app
from jobs.chaban_api import chaban_api
from jobs.enums import ExecutionStatus, JobFrequency, JobType
from jobs.models import Execution, Job
from jobs.weather_api import weather_api


@celery_app.task
def execute_job(execution_id: int, job_type: JobType) -> None:
    execution = Execution.objects.get(id=execution_id)
    execution.status = ExecutionStatus.ON_GOING
    execution.save()

    if job_type == JobType.CHABAN:
        execution.result = chaban_api()
        execution.status = ExecutionStatus.EXECUTED
        execution.save()
    elif job_type == JobType.WEATHER:
        execution.result = weather_api()
        execution.status = ExecutionStatus.EXECUTED
        execution.save()
    else:
        raise ("Job type is not valid")


@celery_app.task
def daily_jobs() -> None:
    for job in Job.objects.filter(frequency=JobFrequency.DAILY):
        print(f"Daily execution created for job {job.name}")
        execution = Execution.objects.create(job=job, status=ExecutionStatus.PENDING)
        execute_job.delay(execution_id=execution.id, job_type=job.type)


@celery_app.task
def weekly_jobs() -> None:
    for job in Job.objects.filter(frequency=JobFrequency.WEEKLY):
        print(f"Weekly execution created for job {job.name}")
        execution = Execution.objects.create(job=job, status=ExecutionStatus.PENDING)
        execute_job.delay(execution_id=execution.id, job_type=job.type)


celery_app.conf.beat_schedule = {
    "daily": {
        "task": "jobs.tasks.daily_jobs",
        "schedule": crontab(minute=0, hour=12),
        "args": (),
    },
    "weekly": {
        "task": "jobs.tasks.weekly_jobs",
        "schedule": crontab(hour=12, minute=0, day_of_week="mon"),
        "args": (),
    },
}
celery_app.conf.timezone = "UTC"
