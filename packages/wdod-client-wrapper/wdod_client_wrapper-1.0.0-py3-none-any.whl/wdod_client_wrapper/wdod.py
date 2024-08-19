import requests
from urllib.parse import urljoin


class WDODClient(requests.Session):
    def __init__(self, base_url, api_key):
        super().__init__()
        self.base_url = base_url
        self.headers.update(
            {
                "x-api-key": api_key
            }
        )

    def request(
            self,
            method,
            url,
            *args,
            **kwargs
    ):
        return super().request(method, urljoin(self.base_url, url), *args, **kwargs)

    @staticmethod
    def parse_response(response):
        if response.status_code not in [200, 201]:
            raise Exception(f"url: {response.url}, status code : {response.status_code}, {response.content}")
        return response.json()

    def get_jobs(self):
        response = self.get("api/v1/jobs")
        return self.parse_response(response)

    def get_jobs_by_id(self, job_id):
        response = self.get(f"api/v1/jobs/{job_id}")
        return self.parse_response(response)

    def start_job(self, job_id):
        response = self.put(f"api/v1/jobs/{job_id}/start")
        return self.parse_response(response)

    def stop_job(self, job_id):
        response = self.put(f"api/v1/jobs/{job_id}/stop")
        return self.parse_response(response)

    def create_job(self, payload):
        response = self.post(f"api/v1/jobs", json=payload)
        return self.parse_response(response)

    def upload_data_file(self, data_file, signed_url):
        with open(data_file, 'rb') as f:
            data = f.read()
        self.put(url=signed_url, data=data)
        return "SUCCESS"

    def get_results(self, results_file, job_id):
        results_response = self.parse_response(self.get(f"api/v1/jobs/{job_id}/results"))
        response = self.get(url=results_response['outputPresignedUrl'])
        with open(results_file, 'wb') as f:
            f.write(response.content)
        return "SUCCESS"
