import copy
import time

import metronome
from metronome import models
from metronome.exceptions import MetronomeHttpError
from behave import given, when, then
from itest_utils import get_metronome_connection_string
from google.protobuf.json_format import Parse


@given(u'a working metronome instance')
def step_impl(context):
    """Adds a working metronome client as context.client for the purposes of
    interacting with it in the test."""
    if not hasattr(context, 'client'):
        metronome_connection_string = "http://%s" % \
                                     get_metronome_connection_string()
        context.client = metronome.MetronomeClient(metronome_connection_string)


@then(u'we get the metronome pong')
def step_impl(context):
    assert context.client.ping() == 'pong'


@when(u'we create a trivial new job')
def step_impl(context):
    request = """
{
  "description": "desc",
  "id": "example.trivial",
  "labels": {},
  "run": {
    "artifacts": [],
    "cmd": "echo hello",
    "cpus": 0.1,
    "disk": 0,
    "maxLaunchDelay": 3600,
    "mem": 32,
    "restart": {
      "activeDeadlineSeconds": 120,
      "policy": "NEVER"
    },
    "volumes": []
  }
}
    """
    job = Parse(request, models.JobSpec())
    context.client.create_job(job=job)


@then(u'we should see the trivial job running via the metronome api')
def step_impl(context):
    time.sleep(5)
    actual = context.client.get_job(job_id='example.trivial')
    assert actual.id == 'example.trivial'
    assert actual.run.cmd == 'echo hello'
    assert actual.run.restart.activeDeadlineSeconds == 120


@when(u'we create a complex new job')
def step_impl(context):
    request = """
{
  "description": "Example Application",
  "id": "example.complex",
  "labels": {
    "location": "olympus",
    "owner": "zeus"
  },
  "run": {
    "artifacts": [
      {
        "uri": "http://foo.example.com/application.zip",
        "extract": true,
        "executable": true,
        "cache": false
      }
    ],
    "cmd": "nuke --dry --master local",
    "cpus": 1.5,
    "mem": 32,
    "disk": 128,
    "docker": {
      "image": "foo/bla:test"
    },
    "env": {
      "MON": "test",
      "CONNECT": "direct"
    },
    "maxLaunchDelay": 3600,
    "placement": {
      "constraints": [
        {
          "attribute": "rack",
          "operator": "EQ",
          "value": "rack-2"
        }
      ]
    },
    "restart": {
      "activeDeadlineSeconds": 120,
      "policy": "NEVER"
    },
    "user": "root",
    "volumes": [
      {
        "containerPath": "/mnt/test",
        "hostPath": "/etc/guest",
        "mode": "RW"
      }
    ]
  }
}
    """
    job = Parse(request, models.JobSpec())
    context.client.create_job(job=job)


@then(u'we should see the complex job running via the metronome api')
def step_impl(context):
    time.sleep(5)
    actual = context.client.get_job(job_id='example.complex')
    expected = models.JobSpec()
    expected.id = 'example.complex'
    expected.description = 'Example Application'
    expected.labels['location'] = 'olympus'
    expected.labels['owner'] = 'zeus'
    run = expected.run
    artifact = run.artifacts.add()
    artifact.uri = 'http://foo.example.com/application.zip'
    artifact.extract = True
    artifact.executable = True
    artifact.cache = False
    run.cmd = 'nuke --dry --master local'
    run.cpus = 1.5
    run.mem = 32
    run.disk = 128
    run.docker.image = 'foo/bla:test'
    run.env['MON'] = 'test'
    run.env['CONNECT'] = 'direct'
    run.maxLaunchDelay = 3600
    constraint = run.placement.constraints.add()
    constraint.attribute = 'rack'
    constraint.operator = constraint.EQ
    constraint.value = 'rack-2'
    run.restart.activeDeadlineSeconds = 120
    run.restart.policy = run.restart.NEVER
    run.user = 'root'
    volume = run.volumes.add()
    volume.containerPath = '/mnt/test'
    volume.hostPath = '/etc/guest'
    volume.mode = volume.RW
    print(actual)
    print(expected)
    assert actual == expected


@then(u'we should update a above job via the metronome api')
def step_impl(context):
    time.sleep(5)
    before = context.client.get_job(job_id='example.trivial')
    for_update = copy.deepcopy([before])[0]
    expected = 'desc_updated'
    for_update.description = expected
    context.client.update_job(job_id=for_update.id, job=for_update)
    actual = context.client.get_job(job_id='example.trivial')

    assert actual.description == expected


@then(u'we should delete a job via the metronome api')
def step_impl(context):
    time.sleep(5)
    status_code = context.client.delete_job(job_id='example.trivial').status_code
    assert status_code == 200

    expected = 'Job not found'
    try:
        context.client.get_job(job_id='example.trivial')
        actual = 'No error'
    except MetronomeHttpError as e:
        actual = e.error_message

    assert actual == expected
