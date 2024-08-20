This is a Python module designed for monitoring cron jobs through Starecase.io

# Installation
``` python
pip install starecase-cron-monitor==0.1.3
```

# Prerequisite
You will need to:
- Fill the form to get API Key: [URL](https://forms.gle/ZFeTSZVh6r7v9Mju6) btw it's Free to use 🎉
- Own a Starecase account
- Create a Starecase API Key

# Environment Variables
We recommend using environment variables for storing your API Key. To set values for these variables, use the following variable names:
- **STARECASE_API_KEY:** To store the API Key.

# Quick Start
### Initialise Service

Just initialise the service by:

```
from cron_monitor.initialiser import initialize_service


initialize_service("YOUR_API_KEY")
```

### Decorate methods

You need to add the @monitor decorator to your function you are using. Below is an example :

```
from cron_monitor.decorator import monitor

@monitor(job_name="test-python-job-name", job_group="python-test-group", expression="* * * * *", debug=True)
    def my_job():
```

# License

This project is licensed under the terms of the MIT license.
