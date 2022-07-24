import requests


class GenerateToken:
    def __init__(self, id, secret):
        self.endpoint = "https://libcal.utk.edu/1.1/oauth/token"
        self.payload = self.__build_payload(id, secret)
        self.token = self.__request_token()

    @staticmethod
    def __build_payload(client_id, secret):
        return {
            "client_id": client_id,
            "client_secret": secret,
            "grant_type": "client_credentials"
        }

    def __request_token(self):
        r = requests.post(self.endpoint, json=self.payload)
        return r.json()['access_token']
