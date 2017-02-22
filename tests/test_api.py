import requests_mock
from metronome import MetronomeClient
from metronome import models


def test_create_job():
    fake_response = """
{
  "description": "desc",
  "id": "example",
  "labels": {},
  "run": {
    "artifacts": [],
    "cmd": "example",
    "cpus": 0.1,
    "disk": 0,
    "env": {},
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
    request = fake_response
    with requests_mock.mock() as m:
        m.post('http://fake_server/v1/jobs', text=fake_response, status_code=201)
        mock_client = MetronomeClient(servers='http://fake_server')
        actual = mock_client.create_job(json_text=request)
        expected = models.JobSpec()
        expected.description = 'desc'
        expected.id = 'example'
        run = expected.run
        run.cmd = 'example'
        run.cpus = 0.1
        run.disk = 0
        run.maxLaunchDelay = 3600
        run.mem = 32.0
        restart = run.restart
        restart.activeDeadlineSeconds = 120
        restart.policy = restart.NEVER
        assert expected == actual


def test_list_job():
    fake_response = """
[
  {
    "description": "desc",
    "id": "example",
    "labels": {},
    "run": {
      "artifacts": [],
      "cmd": "example",
      "cpus": 0.1,
      "disk": 0,
      "env": {},
      "maxLaunchDelay": 3600,
      "mem": 32,
      "restart": {
        "activeDeadlineSeconds": 120,
        "policy": "NEVER"
      },
      "volumes": []
    }
  }
]
    """
    with requests_mock.mock() as m:
        m.get('http://fake_server/v1/jobs', text=fake_response)
        mock_client = MetronomeClient(servers='http://fake_server')
        actual = mock_client.list_jobs()
        expected = [models.JobSpec()]
        expected[0].description = 'desc'
        expected[0].id = 'example'
        run = expected[0].run
        run.cmd = 'example'
        run.cpus = 0.1
        run.disk = 0
        run.maxLaunchDelay = 3600
        run.mem = 32.0
        restart = run.restart
        restart.activeDeadlineSeconds = 120
        restart.policy = restart.NEVER
        assert expected == actual


def test_get_job():
    fake_response = """
{
  "description": "desc",
  "id": "example",
  "labels": {},
  "run": {
    "artifacts": [],
    "cmd": "example",
    "cpus": 0.1,
    "mem": 32,
    "disk": 0,
    "docker": {
      "image": "foo"
    },
    "env": {
      "key1": "val1"
    },
    "maxLaunchDelay": 3600,
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
    with requests_mock.mock() as m:
        m.get('http://fake_server/v1/jobs/example', text=fake_response)
        mock_client = MetronomeClient(servers='http://fake_server')
        actual = mock_client.get_job(job_id='example')
        expected = models.JobSpec()
        expected.description = 'desc'
        expected.id = 'example'
        run = expected.run
        run.cmd = 'example'
        run.cpus = 0.1
        run.mem = 32.0
        run.disk = 0
        run.docker.image = 'foo'
        run.env['key1'] = 'val1'
        run.maxLaunchDelay = 3600
        restart = run.restart
        restart.activeDeadlineSeconds = 120
        restart.policy = restart.NEVER
        run.user = 'root'
        volume = run.volumes.add()
        volume.containerPath = '/mnt/test'
        volume.hostPath = '/etc/guest'
        volume.mode = volume.RW
        assert expected == actual


def test_delete_job():
    with requests_mock.mock() as m:
        m.delete('http://fake_server/v1/jobs/example', status_code=200)
        mock_client = MetronomeClient(servers='http://fake_server')
        actual = mock_client.delete_job(job_id='example').status_code
        expected = 200
        assert expected == actual


def test_create_schedule():
    fake_response = """
{
  "id": "everyminute",
  "cron": "* * * * *",
  "concurrencyPolicy": "ALLOW",
  "enabled": true,
  "startingDeadlineSeconds": 60,
  "timezone": "America/Chicago"
}
    """
    request = fake_response
    with requests_mock.mock() as m:
        m.post('http://fake_server/v1/jobs/example/schedules', text=fake_response, status_code=201)
        mock_client = MetronomeClient(servers='http://fake_server')
        actual = mock_client.create_schedule(job_id='example', json_text=request)
        expected = models.ScheduleSpec()
        expected.id = 'everyminute'
        expected.cron = '* * * * *'
        expected.concurrencyPolicy = expected.ALLOW
        expected.enabled = True
        expected.startingDeadlineSeconds = 60
        expected.timezone = 'America/Chicago'
        assert expected == actual


def test_list_schedules():
    fake_response = """
[
  {
    "id": "everyminute",
    "cron": "* * * * *",
    "concurrencyPolicy": "ALLOW",
    "enabled": true,
    "startingDeadlineSeconds": 60,
    "timezone": "America/Chicago"
  },
  {
    "id": "everyhour",
    "cron": "0 * * * *",
    "concurrencyPolicy": "ALLOW",
    "enabled": true,
    "startingDeadlineSeconds": 60,
    "timezone": "America/Chicago"
  }
]
    """
    with requests_mock.mock() as m:
        m.get('http://fake_server/v1/jobs/example/schedules', text=fake_response)
        mock_client = MetronomeClient(servers='http://fake_server')
        actual = mock_client.list_schedules(job_id='example')
        schedule1 = models.ScheduleSpec()
        schedule1.id = 'everyminute'
        schedule1.cron = '* * * * *'
        schedule1.concurrencyPolicy = schedule1.ALLOW
        schedule1.enabled = True
        schedule1.startingDeadlineSeconds = 60
        schedule1.timezone = 'America/Chicago'
        schedule2 = models.ScheduleSpec()
        schedule2.id = 'everyhour'
        schedule2.cron = '0 * * * *'
        schedule2.concurrencyPolicy = schedule2.ALLOW
        schedule2.enabled = True
        schedule2.startingDeadlineSeconds = 60
        schedule2.timezone = 'America/Chicago'
        expected = [schedule1, schedule2]
        assert expected == actual


def test_get_schedule():
    fake_response = """
{
  "id": "everyminute",
  "cron": "* * * * *",
  "concurrencyPolicy": "ALLOW",
  "enabled": true,
  "startingDeadlineSeconds": 60,
  "timezone": "America/Chicago"
}
    """
    with requests_mock.mock() as m:
        m.get('http://fake_server/v1/jobs/example/schedules/everyminute', text=fake_response)
        mock_client = MetronomeClient(servers='http://fake_server')
        actual = mock_client.get_schedule(job_id='example', schedule_id='everyminute')
        expected = models.ScheduleSpec()
        expected.id = 'everyminute'
        expected.cron = '* * * * *'
        expected.concurrencyPolicy = expected.ALLOW
        expected.enabled = True
        expected.startingDeadlineSeconds = 60
        expected.timezone = 'America/Chicago'
        assert expected == actual


def test_delete_schedule():
    with requests_mock.mock() as m:
        m.delete('http://fake_server/v1/jobs/example/schedules/example2', status_code=200)
        mock_client = MetronomeClient(servers='http://fake_server')
        actual = mock_client.delete_schedule(job_id='example', schedule_id='example2').status_code
        expected = 200
        assert expected == actual


def test_run_job():
    fake_response = """
{
  "completedAt": null,
  "createdAt": "2016-07-15T13:02:59.735+0000",
  "id": "20160715130259A34HX",
  "jobId": "example",
  "status": "STARTING",
  "tasks": []
}
    """
    with requests_mock.mock() as m:
        m.post('http://fake_server/v1/jobs/example/runs', text=fake_response, status_code=201)
        mock_client = MetronomeClient(servers='http://fake_server')
        actual = mock_client.run_job(job_id='example')
        expected = models.JobRun()
        expected.createdAt = '2016-07-15T13:02:59.735+0000'
        expected.id = '20160715130259A34HX'
        expected.jobId = 'example'
        expected.status = expected.STARTING
        assert expected == actual


def test_list_runs():
    fake_response = """
[
  {
    "completedAt": null,
    "createdAt": "2016-07-15T13:02:59.735+0000",
    "id": "20160715130259A34HX",
    "jobId": "example",
    "status": "STARTING",
    "tasks": []
  },
  {
    "completedAt": null,
    "createdAt": "2016-07-12T08:11:59.966+0000",
    "id": "20160712081159ORxez",
    "jobId": "example",
    "status": "STARTING",
    "tasks": []
  }
]
    """
    with requests_mock.mock() as m:
        m.get('http://fake_server/v1/jobs/example/runs', text=fake_response)
        mock_client = MetronomeClient(servers='http://fake_server')
        actual = mock_client.list_runs(job_id='example')
        run1 = models.JobRun()
        run1.createdAt = '2016-07-15T13:02:59.735+0000'
        run1.id = '20160715130259A34HX'
        run1.jobId = 'example'
        run1.status = run1.STARTING
        run2 = models.JobRun()
        run2.createdAt = '2016-07-12T08:11:59.966+0000'
        run2.id = '20160712081159ORxez'
        run2.jobId = 'example'
        run2.status = run2.STARTING
        expected = [run1, run2]
        assert expected == actual


def test_get_run():
    fake_response = """
{
  "completedAt": null,
  "createdAt": "2016-07-15T13:02:59.735+0000",
  "id": "20160715130259A34HX",
  "jobId": "example",
  "status": "STARTING",
  "tasks": []
}
    """
    with requests_mock.mock() as m:
        m.get('http://fake_server/v1/jobs/example/runs/20160715130259A34HX', text=fake_response)
        mock_client = MetronomeClient(servers='http://fake_server')
        actual = mock_client.get_run(job_id='example', run_id='20160715130259A34HX')
        expected = models.JobRun()
        expected.createdAt = '2016-07-15T13:02:59.735+0000'
        expected.id = '20160715130259A34HX'
        expected.jobId = 'example'
        expected.status = expected.STARTING
        assert expected == actual


def test_ping():
    fake_response = 'pong'
    with requests_mock.mock() as m:
        m.get('http://fake_server/ping', text=fake_response)
        mock_client = MetronomeClient(servers='http://fake_server')
        actual = mock_client.ping()
        expected = 'pong'
        assert expected == actual
