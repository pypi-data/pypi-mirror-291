from wdod_client_wrapper.wdod import WDODClient


class WDODJob:
    job_id = None

    def __init__(self, api_url, api_key, job_type, process_source, email, search_engine, result_limit=None,
                 cache_lookback=None, query_retry=None, query_timeout=None):
        self.api_url = api_url
        self.api_key = api_key
        self.job_type = job_type
        self.process_source = process_source
        self.email = email
        self.search_engine = search_engine
        self.result_limit = result_limit
        self.cache_lookback = cache_lookback
        self.query_retry = query_retry
        self.query_timeout = query_timeout
        self.client = WDODClient(api_url, api_key)

    @classmethod
    def from_job_id(cls, api_url, api_key, job_id):
        job_obj = cls(api_url, api_key, None, None, None, None)
        job_obj.job_id = job_id
        return job_obj

    def submit(self, data_file):
        if self.job_id:
            raise Exception("Cannot create new job, this is already existing job")
        payload = {
            "email": self.email,
            "searchEngine": self.search_engine,
            "jobType": self.job_type,
            "processSource": self.process_source
        }
        if self.result_limit:
            payload['resultLimit'] = self.result_limit
        if self.cache_lookback:
            payload['cacheLookback'] = self.cache_lookback
        if self.query_retry:
            payload['queryRetry'] = self.query_retry
        if self.result_limit:
            payload['queryTimeout'] = self.query_timeout
        try:
            job_create_response = self.client.create_job(payload=payload)
            self.job_id = job_create_response['jobId']
            signed_url = job_create_response['inputPresignedUrl']
            self.client.upload_data_file(data_file, signed_url)
            self.client.start_job(self.job_id)
        except Exception as e:
            print("Job submission failed")
            raise Exception(e)
        return self.job_id

    def status(self):
        try:
            job_by_id_response = self.client.get_jobs_by_id(self.job_id)
        except Exception as e:
            print("Job status retrieval failed")
            raise Exception(e)
        return job_by_id_response['jobStatus']

    def results(self, result_file):
        return self.client.get_results(result_file, self.job_id)

    def stop(self):
        try:
            job_stop_response = self.client.stop_job(self.job_id)
        except Exception as e:
            print("Job stop failed")
            raise Exception(e)
        return job_stop_response['message']
