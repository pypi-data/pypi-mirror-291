import requests


class HttpClient:
    @staticmethod
    def get(url, headers=None, **kwargs):
        if headers is None:
            headers = {}
        kwargs['headers'] = headers

        try:
            response = requests.get(url, **kwargs)
            return response.json()
        except Exception as e:
            return e

    @staticmethod
    def post(url, data=None, json=None, headers=None, **kwargs):
        if headers is None:
            headers = {}
        kwargs['headers'] = headers

        try:
            response = requests.post(url, data=data, json=json, **kwargs)
            return response.json()
        except Exception as e:
            return e
