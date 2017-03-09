# dcos-metronome-python

[![Build Status](https://circleci.com/gh/tsukaby/dcos-metronome-python.svg?style=shield&circle-token=449ff532f9d0943476a054e97a29cb62b001442e)](https://circleci.com/gh/tsukaby/dcos-metronome-python)

Python client library for DC/OS Metronome.
This library inspired by [thefactory/marathon-python](https://github.com/thefactory/marathon-python).

#### Compatibility

* For Metronome 0.2.0, use at least dcos-metronome-python 0.3.0

#### Future works

* Run integration tests on CircleCI with docker-compose
* Create schedules at the same time when call `create_job`.

## Installation

```bash
pip install dcos-metronome
```

## Documentation

TODO

## Basic Usage

Create a `MetronomeClient()` instance pointing at your Metronome server(s):
```python
>>> from metronome import MetronomeClient
>>> c = MetronomeClient('http://localhost:8080')

>>> # or multiple servers:
>>> c = MetronomeClient(['http://host1:8080', 'http://host2:8080'])
```

Then try calling some methods:
```python
>>> c.list_jobs()
[id: "example"
description: "Example Job"
labels {
  key: "location"
  value: "olympus"
}
...
]
```

Create job

```python
>>> from google.protobuf.json_format import Parse
>>> from metronome.models import JobSpec
>>> json_text = """{"description":"desc","id":"example","labels":{},"run":{"artifacts":[],"cmd":"example","cpus":0.1,"disk":0,"env":{},"maxLaunchDelay":3600,"mem":32,"restart":{"activeDeadlineSeconds":120,"policy":"NEVER"},"volumes":[]}}"""
>>> job = Parse(json_text, JobSpec())
>>> c.create_job(job)
id: "example"
description: "desc"
run {
  cpus: 0.1
  mem: 32.0
  cmd: "example"
  placement {
  }
  maxLaunchDelay: 3600
  restart {
    policy: NEVER
    activeDeadlineSeconds: 120
  }
}
```

***Other methods***

- create_job
- list_jobs
- get_job
- update_job
- delete_job
- create_schedule
- list_schedules
- get_schedule
- update_schedule
- delete_schedule
- run_job
- list_runs
- get_run
- stop_run
- ping

See following code for details.

[client.py](metronome/client.py)

***Not implemented (TODO)***

- /v1/metrics (GET)
- /v0/scheduled-jobs (POST)
- /v0/scheduled-jobs/{jobId} (PUT)

## Development

### Setup

```bash
brew install protobuf
# protoc --version
# libprotoc 3.2.0

pip install -r requirements.txt
pip install tox
```

### Testing

#### Unit tests

```bash
make tests
```

#### Integration tests

```bash
make itests
```

### Create/Update models by Protocol buffer

```
# edit protobuf/metronome.proto
make codegen
```

### Package

```bash
make package
```

### Publish (for owner only)

```bash
make publish
```

# License

Open source under the MIT License. See [LICENSE](LICENSE).
