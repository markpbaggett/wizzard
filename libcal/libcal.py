import requests
from dotenv import load_dotenv
import os

load_dotenv()


class GenerateToken:
    def __init__(self, id, secret):
        self.endpoint = "https://libcal.utk.edu/1.1/oauth/token"
        self.payload = self.__build_payload(id, secret)
        self.token = {"Authorization": f"Bearer {self.__request_token()}"}

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


class RoomBookings:
    def __init__(self, group_id, date):
        self.group_id = group_id
        self.date = date
        self.endpoint = f"https://libcal.utk.edu/1.1/room_bookings_nickname?group_id={group_id}&date={date}"
        self.headers = {"Content-Type": "application/json; charset=utf-8"}

    def get_bookings(self):
        headers = GenerateToken(os.getenv('id'), os.getenv('secret')).token
        r = requests.get(self.endpoint, headers=headers)
        return r.json()


