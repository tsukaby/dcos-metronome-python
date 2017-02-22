from metronome.exceptions import MetronomeHttpError
from behave import given, when, then

try:
    import json
except ImportError:
    import simplejson as json


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
    return json_str


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
    return json_str


@when(u'we create a schedule')
def step_impl(context):
    job = base_job()
    context.client.create_job(json_text=job)
    schedule = base_schedule()
    context.client.create_schedule(job_id=json.loads(job)['id'], json_text=schedule)


@then(u'we should see the schedule via the metronome api')
def step_impl(context):
    job = base_job()
    schedule = base_schedule()
    actual = context.client.get_schedule(job_id=json.loads(job)['id'], schedule_id=json.loads(schedule)['id']).id
    expected = json.loads(schedule)['id']
    assert expected == actual


@when(u'we update a schedule')
def step_impl(context):
    job = base_job()
    context.client.create_job(json_text=job)
    schedule = base_schedule()
    context.client.create_schedule(job_id=json.loads(job)['id'], json_text=schedule)
    tmp = json.loads(base_schedule())
    tmp['cron'] = '0 * * * *'
    schedule_for_update = json.dumps(tmp)
    context.client.update_schedule(
        job_id=json.loads(job)['id'], schedule_id=json.loads(schedule)['id'], json_text=schedule_for_update
    )


@then(u'we should see the updated schedule via the metronome api')
def step_impl(context):
    job = base_job()
    schedule = base_schedule()
    actual = context.client.get_schedule(job_id=json.loads(job)['id'], schedule_id=json.loads(schedule)['id']).cron
    expected = '0 * * * *'
    assert expected == actual


@when(u'we delete a schedule')
def step_impl(context):
    job = base_job()
    context.client.create_job(json_text=job)
    schedule = base_schedule()
    context.client.create_schedule(job_id=json.loads(job)['id'], json_text=schedule)
    context.client.delete_schedule(job_id=json.loads(job)['id'], schedule_id=json.loads(schedule)['id'])


@then(u'we should not see the schedule via the metronome api')
def step_impl(context):
    expected = 'Schedule not found'
    try:
        job = base_job()
        schedule = base_schedule()
        context.client.get_schedule(job_id=json.loads(job)['id'], schedule_id=json.loads(schedule)['id'])
        actual = 'No error'
    except MetronomeHttpError as e:
        actual = e.error_message

    assert expected == actual
