
try:
    import json
except ImportError:
    import simplejson as json

import requests
import requests.exceptions

import metronome
from .models import JobSpec, ScheduleSpec, JobRun
from .exceptions import MetronomeError, MetronomeHttpError, NotFoundError, InternalServerError
from google.protobuf.json_format import Parse, MessageToJson


class MetronomeClient(object):

    """Client interface for the Metronome REST API."""

    def __init__(self, servers, username=None, password=None, timeout=10, session=None,
                 auth_token=None, verify=True):
        if session is None:
            self.session = requests.Session()
        else:
            self.session = session
        self.servers = servers if isinstance(servers, list) else [servers]
        self.auth = (username, password) if username and password else None
        self.verify = verify
        self.timeout = timeout

        self.auth_token = auth_token
        if self.auth and self.auth_token:
            raise ValueError("Can't specify both auth token and username/password. Must select "
                             "one type of authentication.")

    def __repr__(self):
        return 'Connection:%s' % self.servers

    @staticmethod
    def _parse_response(response, clazz, is_list=False, resource_name=None):
        """Parse a Marathon response into an object or list of objects."""
        target = response.json()[
            resource_name] if resource_name else response.json()
        if is_list:
            return [Parse(json.dumps(resource), clazz()) for resource in target]
        else:
            return Parse(json.dumps(target), clazz())

    def _do_request(self, method, path, params=None, data=None):
        """Query Metronome server."""
        headers = {
            'Accept': 'application/json'
        }

        if data is not None:
            headers['Content-Type'] = 'application/json'

        if self.auth_token:
            headers['Authorization'] = "token={}".format(self.auth_token)

        response = None
        servers = list(self.servers)
        while servers and response is None:
            server = servers.pop(0)
            url = ''.join([server.rstrip('/'), path])
            try:
                response = self.session.request(
                    method, url, params=params, data=data, headers=headers,
                    auth=self.auth, timeout=self.timeout, verify=self.verify)
                metronome.log.info('Got response from %s', server)
            except requests.exceptions.RequestException as e:
                metronome.log.error(
                    'Error while calling %s: %s', url, str(e))

        if response is None:
            raise MetronomeError('No remaining Metronome servers to try')

        if response.status_code >= 500:
            metronome.log.error('Got HTTP {code}: {body}'.format(
                code=response.status_code, body=response.text))
            raise InternalServerError(response)
        elif response.status_code >= 400:
            metronome.log.error('Got HTTP {code}: {body}'.format(
                code=response.status_code, body=response.text))
            if response.status_code == 404:
                raise NotFoundError(response)
            else:
                raise MetronomeHttpError(response)
        elif response.status_code >= 300:
            metronome.log.warn('Got HTTP {code}: {body}'.format(
                code=response.status_code, body=response.text))
        else:
            metronome.log.debug('Got HTTP {code}: {body}'.format(
                code=response.status_code, body=response.text))

        return response

    def create_job(self, job):
        data = MessageToJson(job, preserving_proto_field_name=True)
        response = self._do_request('POST', '/v1/jobs', data=data)
        if response.status_code == 201:
            return self._parse_response(response, JobSpec)
        else:
            return False

    def list_jobs(self, active_runs=False, schedules=False, history=False, history_summary=False):
        params = {
            'activeRuns': str(active_runs).lower(),
            'schedules': str(schedules).lower(),
            'history': str(history).lower(),
            'historySummary': str(history_summary).lower()
        }
        response = self._do_request('GET', '/v1/jobs', params=params)
        jobs = self._parse_response(
            response, JobSpec, is_list=True)
        return jobs

    def get_job(self, job_id, active_runs=False, schedules=False, history_summary=False):
        params = {
            'activeRuns': str(active_runs).lower(),
            'schedules': str(schedules).lower(),
            'historySummary': str(history_summary).lower()
        }
        response = self._do_request('GET', '/v1/jobs/{job_id}'.format(job_id=job_id), params=params)
        return self._parse_response(response, JobSpec)

    def update_job(self, job_id, job):
        jsonAsJob = json.loads(MessageToJson(job, preserving_proto_field_name=True))
        # Workaround. Please fix
        if 'placement' in jsonAsJob['run'] and 'constraints' not in jsonAsJob['run']['placement']:
            del jsonAsJob['run']['placement']
        response = self._do_request('PUT', '/v1/jobs/{job_id}'.format(job_id=job_id), data=json.dumps(jsonAsJob))
        if response.status_code == 200:
            return self._parse_response(response, JobSpec)
        else:
            return False

    def delete_job(self, job_id, stop_current_job_runs=False):
        params = {
            'stopCurrentJobRuns': str(stop_current_job_runs).lower()
        }
        response = self._do_request('DELETE', '/v1/jobs/{job_id}'.format(job_id=job_id), params=params)
        return response

    def create_schedule(self, job_id, schedule):
        data = MessageToJson(schedule, preserving_proto_field_name=True)
        response = self._do_request('POST', '/v1/jobs/{job_id}/schedules'.format(job_id=job_id), data=data)
        if response.status_code == 201:
            return self._parse_response(response, ScheduleSpec)
        else:
            return False

    def list_schedules(self, job_id):
        response = self._do_request('GET', '/v1/jobs/{job_id}/schedules'.format(job_id=job_id))
        schedules = self._parse_response(
            response, ScheduleSpec, is_list=True)
        return schedules

    def get_schedule(self, job_id, schedule_id):
        response = self._do_request(
            'GET',
            '/v1/jobs/{job_id}/schedules/{schedule_id}'.format(job_id=job_id, schedule_id=schedule_id)
        )
        return self._parse_response(response, ScheduleSpec)

    def update_schedule(self, job_id, schedule_id, schedule):
        data = MessageToJson(schedule, preserving_proto_field_name=True)
        response = self._do_request(
            'PUT', '/v1/jobs/{job_id}/schedules/{schedule_id}'.format(job_id=job_id, schedule_id=schedule_id), data=data
        )
        if response.status_code == 200:
            return self._parse_response(response, ScheduleSpec)
        else:
            return False

    def delete_schedule(self, job_id, schedule_id):
        response = self._do_request(
            'DELETE', '/v1/jobs/{job_id}/schedules/{schedule_id}'.format(job_id=job_id, schedule_id=schedule_id)
        )
        return response

    def run_job(self, job_id):
        response = self._do_request('POST', '/v1/jobs/{job_id}/runs'.format(job_id=job_id))
        if response.status_code == 201:
            return self._parse_response(response, JobRun)
        else:
            return False

    def list_runs(self, job_id):
        response = self._do_request('GET', '/v1/jobs/{job_id}/runs'.format(job_id=job_id))
        return self._parse_response(response, JobRun, is_list=True)

    def get_run(self, job_id, run_id):
        response = self._do_request('GET', '/v1/jobs/{job_id}/runs/{run_id}'.format(job_id=job_id, run_id=run_id))
        return self._parse_response(response, JobRun)

    def stop_run(self, job_id, run_id):
        response = self._do_request(
            'POST', '/v1/jobs/{job_id}/runs/{run_id}/actions/stop'.format(job_id=job_id, run_id=run_id)
        )
        return response

    def ping(self):
        response = self._do_request('GET', '/ping')
        return response.text
