from datetime import datetime
from cron_monitor.http_client import HttpClient
from cron_monitor import constants
import time


class CronMonitor:
    @staticmethod
    def register_event(register_cron):
        from cron_monitor.initialiser import STARECASE_API_KEY
        url = f"{constants.api_base_url}/{constants.routes['CRON_REGISTRAR']}"
        registered_cron = HttpClient.post(url=url, json=register_cron, headers={'x-api-key': STARECASE_API_KEY})
        request_id = registered_cron['message']['data']['responseId']
        return request_id

    @staticmethod
    def get_job_details_by_req_id(request_id, number_of_request):
        from cron_monitor.initialiser import STARECASE_API_KEY
        url = f"{constants.api_base_url}/{constants.routes['CRON_REGISTRAR']}/{request_id}"
        job_details = HttpClient.get(url=url, headers={'x-api-key': STARECASE_API_KEY})
        if job_details['status'] == "failure":
            return None
        elif number_of_request > 5:
            return None
        elif job_details['message']['data'] is None:
            time.sleep(1.5)
            return CronMonitor.get_job_details_by_req_id(request_id, number_of_request + 1)
        return job_details['message']['data']

    @staticmethod
    def handle_on_demand_intent(register_cron_payload):
        current_datetime = datetime.utcnow()
        request_id = CronMonitor.register_event({
            'events': [
                {
                    'intent': 'START',
                    'expression': register_cron_payload['expression'],
                    'startTime': current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    'group': register_cron_payload['job_group'],
                    'jobName': register_cron_payload['job_name'],
                }
            ]
        })
        return CronMonitor.get_job_details_by_req_id(request_id, 0)

    @staticmethod
    def handle_end_intent(job_id):
        current_datetime = datetime.utcnow()
        return CronMonitor.register_event({
            'events': [
                {
                    'intent': 'END',
                    'endTime': current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    'jobId': job_id
                }
            ]
        })

    @staticmethod
    def handle_error_intent(job_id, error_trace):
        current_datetime = datetime.utcnow()
        return CronMonitor.register_event({
            'events': [
                {
                    'intent': 'ERROR',
                    'endTime': current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    'jobId': job_id,
                    'errorTrace': error_trace
                }
            ]
        })
