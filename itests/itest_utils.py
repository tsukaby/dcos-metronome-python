import errno
from functools import wraps
import os
import signal
import time

import requests
import compose.cli.command


class TimeoutError(Exception):
    pass


def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator


@timeout(30)
def wait_for_metronome():
    """Blocks until metronome is up"""
    metronome_service = get_metronome_connection_string()
    while True:
        print('Connecting to metronome on %s' % metronome_service)
        try:
            response = requests.get(
                'http://%s/ping' % metronome_service, timeout=2)
        except (
            # requests.exceptions.ConnectTimeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
        ):
            time.sleep(2)
            continue
        if response.status_code == 200:
            print("Metronome is up and running!")
            break


def get_compose_service(service_name):
    """Returns a compose object for the service"""
    project = compose.cli.command.get_project(os.path.dirname(os.path.realpath(__file__)))
    return project.get_service(service_name)


def get_metronome_connection_string():
    # only reliable way I can detect travis..
    # if '/travis/' in os.environ.get('PATH'):
    #     return 'localhost:8080'
    # else:
    #     service_port = get_service_internal_port('metronome')
    #     local_port = get_compose_service('metronome').get_container().get_local_port(service_port)
    #     return local_port
    return os.environ.get('DOCKER_IP') + ':8081'


def get_service_internal_port(service_name):
    """Gets the exposed port for service_name from docker-compose.yml. If there are
    multiple ports. It returns the first one."""
    return get_compose_service(service_name).options['ports'][0]
