# dcos-metronome-python

![Build Status](https://circleci.com/gh/tsukaby/dcos-metronome-python.svg?style=shield&circle-token=449ff532f9d0943476a054e97a29cb62b001442e)

Python client library for DC/OS Metronome.
This library inspired by [thefactory/marathon-python](https://github.com/thefactory/marathon-python).

#### Compatibility

* For Metronome 0.2.0, use at lease dcos-metronome-python 0.1.0

## Installation

TODO

## Testing 

### Running The Tests

```bash
make itests
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
TODO
```

TODO other methods

## Development

### Create/Update models by Protocol buffer

```
brew install protobuf
# protoc --version
# libprotoc 3.2.0

# edit protobuf/metronome.proto
make codegen
```

TODO

# License

Open source under the MIT License. See [LICENSE](LICENSE).
