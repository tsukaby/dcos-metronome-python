import time
from behave import when, then
from metronome.exceptions import MetronomeHttpError

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


@when(u'we create a run')
def step_impl(context):
    job = base_job()
    context.client.create_job(json_text=job)
    run = context.client.run_job(job_id=json.loads(job)['id'])
    context.run_ids = {'we_create_a_run': run.id}


@then(u'we should see the run via the metronome api')
def step_impl(context):
    job = base_job()
    run_id = context.run_ids['we_create_a_run']
    actual = context.client.get_run(job_id=json.loads(job)['id'], run_id=run_id)
    assert run_id == actual.id


@when(u'we stop a run')
def step_impl(context):
    job = base_job()
    context.client.create_job(json_text=job)
    run = context.client.run_job(job_id=json.loads(job)['id'])
    context.run_ids = {'we_stop_a_run': run.id}
    time.sleep(5)
    print('debug')
    print(context.client.list_runs(job_id=json.loads(job)['id']))
    context.client.stop_run(job_id=json.loads(job)['id'], run_id=run.id)


@then(u'we should see the stopped run via the metronome api')
def step_impl(context):
    job = base_job()
    run_id = context.run_ids['we_stop_a_run']

    expected = 'Job Run not found'
    try:
        context.client.get_run(job_id=json.loads(job)['id'], run_id=run_id)
        actual = 'No error'
    except MetronomeHttpError as e:
        actual = e.error_message

    assert expected == actual
