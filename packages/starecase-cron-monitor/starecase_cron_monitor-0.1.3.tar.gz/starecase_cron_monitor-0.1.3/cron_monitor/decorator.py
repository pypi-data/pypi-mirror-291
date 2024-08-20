from cron_monitor.cron_monitor_sdk import CronMonitor
from cron_monitor.logger import CustomLogger
import traceback


def monitor(job_name, job_group, expression, debug):
    logger = CustomLogger(options={'debug': debug})

    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.log(f'{job_name} with group {job_group}, job is running...')
            job_details = CronMonitor.handle_on_demand_intent(register_cron_payload={
                'expression': expression,
                'job_group': job_group,
                'job_name': job_name,
            })
            logger.log(f'Job details : {job_details}')
            global result
            try:
                result = func(*args, **kwargs)
                if job_details['_id']:
                    return CronMonitor.handle_end_intent(job_details['_id'])
                logger.log(f'{job_name} with group {job_group} job is completed...')
            except Exception as e:
                logger.log(f'{job_name} with group {job_group} threw an error don`t worry this will be reported..')
                if job_details['_id']:
                    error_trace = traceback.format_exc()
                    return CronMonitor.handle_error_intent(job_details['_id'], error_trace)

        return wrapper

    return decorator
