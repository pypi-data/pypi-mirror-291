#    See the NOTICE file distributed with this work for additional information
#    regarding copyright ownership.
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#        http://www.apache.org/licenses/LICENSE-2.0
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import logging
import requests
from ensembl.production.core.server_utils import assert_http_uri
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class RestClient(object):
    """
    Base client for interacting with a standard production REST service where the URIs meet a common standard.
    Most methods are stubs for overriding or decoration by classes that extend this for specific services
    """

    jobs = '{}jobs'
    jobs_id = '{}jobs/{}'


    def __init__(self, uri):
        assert_http_uri(uri)
        self.uri = uri
        self._http_adapter = self._make_HTTPAdapter()

    def _make_HTTPAdapter(self):
        retries = Retry(total=3, backoff_factor=1,
                        status_forcelist=[429, 500, 502, 503, 504],
                        allowed_methods=["GET", "PUT", "POST", "DELETE"])
        adapter = HTTPAdapter(max_retries=retries)
        return adapter

    def _session(self, use_ssl=False):
        http = requests.Session()
        if use_ssl:
            http.mount("https://", self._http_adapter)
        else:
            http.mount("http://", self._http_adapter)
        http.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        return http

    def submit_job(self, payload):
        """
        Submit a job using the supplied dict as payload. No checking is carried out on the payload
        Arguments:
          payload : job input as dict
        """
        logging.info("Submitting job")
        logging.debug(payload)
        with self._session() as session:
            r = session.post(self.jobs.format(self.uri), json=payload)
        if r.status_code != 201:
            logging.error("failed to submit because: %s", r.text)
        r.raise_for_status()
        return r.json()['job_id']

    def delete_job(self, job_id, kill=False):
        """
        Delete job
        Arguments:
          job_id - ID of job to kill
          kill - if True, job process should be killed
        """
        delete_uri = self.jobs_id.format(self.uri, str(job_id))
        if kill:
            params = {'kill': '1'}
        else:
            params = {}
        with self._session() as session:
            r = session.delete(delete_uri, params=params)
        if r.status_code != 204:
            logging.error("failed to delete job because: %s", r.text)
        r.raise_for_status()
        return True

    def list_jobs(self):
        """
        Find all current jobs
        """
        logging.info("Listing")
        with self._session() as session:
            r = session.get(self.jobs.format(self.uri))
        if r.status_code != 200:
            logging.error("failed to list jobs because: %s", r.text)
        r.raise_for_status()
        return r.json()

    def retrieve_job_failure(self, job_id):
        """
        Retrieve information on a job using the special format "failure" which renders failures from the supplied job.
        The service will respond if it supports this format.
        Arguments:
          job_id - ID of job to retrieve
        """
        logging.info("Retrieving job failure for job %s", job_id)
        with self._session() as session:
            r = session.get(self.jobs_id.format(self.uri, str(job_id)), params={'format': 'failures'})
        if r.status_code != 200:
            logging.error("failed to retrieve job failures because: %s", r.text)
        r.raise_for_status()
        failure_msg = r.json()
        return failure_msg

    def retrieve_job_email(self, job_id):
        """
        Retrieve information on a job using the special format "email" which renders the supplied job in a format suitable
        for sending by email.
        The service will respond if it supports this format.
        Arguments:
          job_id - ID of job to retrieve
        """
        logging.info("Retrieving job as email for job %s", job_id)
        with self._session() as session:
            r = session.get(self.jobs_id.format(self.uri, str(job_id)), params={'format': 'email'})
        r.raise_for_status()
        return r.json()

    def retrieve_job(self, job_id):
        """
        Retrieve information on a job.
        Arguments:
          job_id - ID of job to retrieve
        """
        logging.info("Retrieving results for job %s", job_id)
        with self._session() as session:
            r = session.get(self.jobs_id.format(self.uri, str(job_id)))
        if r.status_code != 200:
            logging.error("failed to retrieve job because: %s", r.text)
        r.raise_for_status()
        job = r.json()
        return job

    def print_job(self, job, **kwargs):
        """
        Stub utility to print job to logging
        Arguments:
          job - job object
          print_results - ignored
          print_input - ignored
        """
        logging.info(job)

    def write_output(self, r, output_file):
        """
        Utility to write response.
        Arguments:
          job - response object
          output_file - output file handle
        """
        if output_file is not None:
            with output_file as f:
                f.write(r.text)

