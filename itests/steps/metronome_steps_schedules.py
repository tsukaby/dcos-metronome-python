from metronome import models
from metronome.exceptions import MetronomeHttpError
from behave import given, when, then
from google.protobuf.json_format import Parse


def base_job():
    json_str = """
{
  "description": "desc",
  "id": "example.run",
  "labels": {},
  "run": {
    "artifacts": [],
    "cmd": "sleep",
    "args": ["30"],
    "cpus": 0.1,
    "disk": 0,
    "docker": {
      "image": "library/alpine"
    },
    "maxLaunchDelay": 1,
    "mem": 32,
    "restart": {
      "activeDeadlineSeconds": 120,
      "policy": "NEVER"
    },
    "user": "root",
    "volumes": []
  }
}
    """
    job = Parse(json_str, models.JobSpec())
    return job


def base_schedule():
    json_str = """
{
  "id": "everyminute",
  "cron": "* * * * *",
  "concurrencyPolicy": "ALLOW",
  "enabled": true,
  "startingDeadlineSeconds": 60,
  "timezone": "America/Chicago"
}
    """
    schedule = Parse(json_str, models.ScheduleSpec())
    return schedule


@when(u'we create a schedule')
def step_impl(context):
    job = base_job()
    context.client.create_job(job=job)
    schedule = base_schedule()
    context.client.create_schedule(job_id=job.id, schedule=schedule)


@then(u'we should see the schedule via the metronome api')
def step_impl(context):
    actual = context.client.get_schedule(job_id=base_job().id, schedule_id=base_schedule().id).id
    expected = base_schedule().id
    assert expected == actual


@when(u'we update a schedule')
def step_impl(context):
    job = base_job()
    context.client.create_job(job=job)
    schedule = base_schedule()
    context.client.create_schedule(job_id=job.id, schedule=schedule)
    schedule_for_update = base_schedule()
    schedule_for_update.cron = '0 * * * *'
    context.client.update_schedule(job_id=job.id, schedule_id=schedule.id, schedule=schedule_for_update)


@then(u'we should see the updated schedule via the metronome api')
def step_impl(context):
    actual = context.client.get_schedule(job_id=base_job().id, schedule_id=base_schedule().id).cron
    expected = '0 * * * *'
    assert expected == actual


@when(u'we delete a schedule')
def step_impl(context):
    job = base_job()
    context.client.create_job(job=job)
    schedule = base_schedule()
    context.client.create_schedule(job_id=job.id, schedule=schedule)
    context.client.delete_schedule(job_id=job.id, schedule_id=schedule.id)


@then(u'we should not see the schedule via the metronome api')
def step_impl(context):
    expected = 'Schedule not found'
    try:
        context.client.get_schedule(job_id=base_job().id, schedule_id=base_schedule().id)
        actual = 'No error'
    except MetronomeHttpError as e:
        actual = e.error_message

    assert expected == actual
