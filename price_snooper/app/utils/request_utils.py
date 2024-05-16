import requests

class RequestError(Exception):
    pass

class RequestUtils:
    @staticmethod
    def get(url, params=None, headers=None):
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response
        except requests.exceptions.RequestException as e:
            raise RequestError(f"Error making GET request: {e}")

    @staticmethod
    def post(url, data=None, json=None, headers=None):
        try:
            response = requests.post(url, data=data, json=json, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response
        except requests.exceptions.RequestException as e:
            raise RequestError(f"Error making POST request: {e}")
