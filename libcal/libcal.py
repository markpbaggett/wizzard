import requests
from dotenv import load_dotenv
import os
import arrow

# TODO: Move load_dotenv() to controller.
load_dotenv()


class GenerateToken:
    """
    A class to represent a request for generating a token for LibCal authentication.

    Attributes:
        payload (dict): A payload that LibCal authorization expects that includes the client_id and secret.
        token (dict): The actual token to be used in all future LibCal requests (valid for 3600 seconds).

    Private methods:
        __build_payload(client_id=None, secret=None): Builds the payload to be posted
        __request_token(): Posts payload and returns token to token attribute for future requests.

    """
    def __init__(self, client_id, secret):
        self.payload = self.__build_payload(client_id, secret)
        self.token = {"Authorization": f"Bearer {self.__request_token()}"}

    @staticmethod
    def __build_payload(client_id, secret):
        return {
            "client_id": client_id,
            "client_secret": secret,
            "grant_type": "client_credentials"
        }

    def __request_token(self):
        r = requests.post("https://libcal.utk.edu/1.1/oauth/token", json=self.payload)
        return r.json()['access_token']


class RoomBookings:
    """
        A class to represent a room bookings nickname request in LibCal.

        Parameters:
            group_id (str): The group_id value that you are requesting from LibCal.
            date (str): The date of RoomBookings you are requesting from Libcal.

        Attributes:
            group_id (str): The group_id value that you are requesting from LibCal.
            date (str): The date of RoomBookings you are requesting from Libcal.
            endpoint (str): The entire request URI for the API request.
            headers (dict): The headers value needed for the request.

        Methods:
            get_bookings(): Gets all Bookings from LibCal based on group_id and date.

        """
    def __init__(self, group_id, date):
        self.group_id = group_id
        self.date = date
        self.endpoint = f"https://libcal.utk.edu/1.1/room_bookings_nickname?group_id={group_id}&date={date}"
        self.headers = {"Content-Type": "application/json; charset=utf-8"}

    def get_bookings(self):
        """
        Gets all Bookings from LibCal based on group_id and date.

        Returns:
            dict: A dict of all bookings from LibCal.  The bookings are described in the timeslots lists as dicts.

        Examples:
            >>> RoomBookings('10024', '2022-07-25').get_bookings()
            {'bookings': {'group_id': 10024, 'name': 'Hodges Library Study Rooms', 'url':
            'https://libcal.utk.edu/booking/studyrooms', 'timeslots': [{'room_id': 53176, 'room_name': '220C',
            'booking_label': 'Lindsey', 'booking_start': '2022-07-25T12:00:00-04:00', 'booking_end':
            '2022-07-25T13:00:00-04:00', 'booking_created': '2022-07-25T12:32:39-04:00'}, {'room_id': 31772,
            'room_name': '220D', 'booking_label': "Alex's Research Meeting", 'booking_start': '2022-07-25T13:00:00-04:00',
            'booking_end': '2022-07-25T14:00:00-04:00', 'booking_created': '2022-07-25T12:09:26-04:00'}, {'room_id':
            53176, 'room_name': '220C', 'booking_label': 'Lindsey', 'booking_start': '2022-07-25T13:00:00-04:00',
            'booking_end': '2022-07-25T14:00:00-04:00', 'booking_created': '2022-07-25T12:32:39-04:00'}, {'room_id':
            31772, 'room_name': '220D', 'booking_label': "Alex's Research Meeting", 'booking_start':
            '2022-07-25T14:00:00-04:00', 'booking_end': '2022-07-25T15:00:00-04:00', 'booking_created': '
            2022-07-25T12:09:26-04:00'}, {'room_id': 31776, 'room_name': '235M', 'booking_label': "Mark's Test",
            'booking_start': '2022-07-25T15:00:00-04:00', 'booking_end': '2022-07-25T16:00:00-04:00',
            'booking_created': '2022-07-25T14:22:04-04:00'}, {'room_id': 31772, 'room_name': '220D',
            'booking_label': 'Study time', 'booking_start': '2022-07-25T16:00:00-04:00', 'booking_end':
            '2022-07-25T17:00:00-04:00', 'booking_created': '2022-07-25T15:57:47-04:00'}, {'room_id': 31772,
            'room_name': '220D', 'booking_label': 'Study time', 'booking_start': '2022-07-25T17:00:00-04:00',
            'booking_end': '2022-07-25T18:00:00-04:00', 'booking_created': '2022-07-25T15:57:47-04:00'}, {'room_id':
            31774, 'room_name': '235K', 'booking_label': 'Class', 'booking_start': '2022-07-25T18:00:00-04:00',
            'booking_end': '2022-07-25T19:00:00-04:00', 'booking_created': '2022-07-25T17:28:15-04:00'}, {'room_id':
            31774, 'room_name': '235K', 'booking_label': 'Class', 'booking_start': '2022-07-25T19:00:00-04:00',
            'booking_end': '2022-07-25T20:00:00-04:00', 'booking_created': '2022-07-25T17:28:15-04:00'}],
            'last_updated': '2022-07-25T18:34:29-04:00'}}

        """
        # TODO: Break out .env expectations from method.
        headers = GenerateToken(os.getenv('client_id'), os.getenv('secret')).token
        r = requests.get(self.endpoint, headers=headers)
        print(f'\t * Room Bookings request made to LibCal at {arrow.utcnow()}. Responded with {r.status_code} response.')
        return r.json()


class Spaces:
    def __init__(self, date):
        self.date = date
        self.endpoint = f" https://libcal.utk.edu/1.1/space/nickname/30611?date={date}"
        self.headers = {"Content-Type": "application/json; charset=utf-8"}

    def get_bookings(self):
        headers = GenerateToken(os.getenv('client_id'), os.getenv('secret')).token
        r = requests.get(self.endpoint, headers=headers)
        print(
            f'\t * Room Bookings request made to LibCal at {arrow.utcnow()}. Responded with {r.status_code} response.')
        return r.json()


if __name__ == "__main__":
    x = Spaces('2022-08-10').get_bookings()
    print(x)