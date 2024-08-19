import requests
from requests.exceptions import HTTPError
from .const import API_URL, USER_AGENT
from .exceptions import GlueAuthenticationError

class GlueAuth:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def issue_api_key(self):
        try:
            response = requests.post(
                f'{API_URL}/v1/api-keys',
                json={
                    'name': 'gluehome-python',
                    'scopes': ['locks.write', 'locks.read', 'events.read']
                },
                auth=(self.username, self.password),
                headers={'User-Agent': USER_AGENT}
            )
            response.raise_for_status()
            return response.json()['apiKey']
        except HTTPError as http_err:
            if http_err.response.status_code == 401:
                raise GlueAuthenticationError("Authentication failed. Please check your username and password.") from http_err
            else:
                raise  # Re-raise the original HTTPError for other status codes
        except Exception as err:
            raise Exception(f"An error occurred while issuing the API key: {err}") from err
