from cron_monitor.logger import CustomLogger

STARECASE_API_KEY = ""


def initialize_service(api_key):
    global STARECASE_API_KEY
    logger = CustomLogger(options={'debug': True})
    logger.log(f"Initialising starecase and validating API Key {api_key}")
    STARECASE_API_KEY = api_key
    logger.log("starecase service initialised...")
    # return STARECASE_API_KEY
