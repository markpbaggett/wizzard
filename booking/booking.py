from libcal.libcal import RoomBookings
import arrow
from uuid import uuid4


class Room:
    """
    A class used to represent a Room described by LibCal.

    Attributes:
        room_name (str): The value that identifies a RoomWizard in its config and the room_name value of a booking
            described in the room_bookings_nickname API.

    Methods:
        get_bookings(date="today"): Gets bookings related to a particular room on a specific date. date param is not
            currently implemented.

    """
    def __init__(self, room_name):
        self.room_name = room_name

    def get_bookings(self, date="today"):
        """Get the bookings of a particular RoomWizard on a specific date.

        Date param is not currently used.

        Parameters:
            date (str): The date you are requesting. Defaults to today.

        Returns:
            list: A list of bookings (dicts) related to the particular room.

        Examples:
            >>> Room('220D').get_bookings()
            [{'start_date': '20220725', 'end_date': '20220725', 'start_time': '120000', 'end_time': '130000',
            'purpose': 'Lindsey', 'notes': 'Booking created 07 25, 2022 at 12:32:39.', 'booking_id':
            UUID('af0179f1-e872-484a-a612-2ce6937f7a59'), 'confidential': 'no', 'password_protected': 'no'},
            {'start_date': '20220725', 'end_date': '20220725', 'start_time': '130000', 'end_time': '140000', 'purpose':
            'Lindsey', 'notes': 'Booking created 07 25, 2022 at 12:32:39.', 'booking_id': UUID('9be77f9b-d4b5-4dff-8eb5-c3343a0db14e'),
            'confidential': 'no', 'password_protected': 'no'}]

        """
        # TODO: Use date instead of utcnow()
        all_bookings = RoomBookings('10024', arrow.utcnow().format('YYYYMMDD')).get_bookings()
        return [Booking(booking).response for booking in all_bookings['bookings']['timeslots'] if self.room_name == booking['room_name']]


class Booking:
    """
        A class used to represent a Booking described by LibCal.

        Attributes:
            start_date (str): The starting date of the Booking formatted as 'YYYYMMDD'.
            end_date (str): The end date of the Booking formatted as 'YYYYMMDD'.
            start_time (str): The starting time of the Booking formatted as 'HHmmss'.
            end_time (str): The ending time of the Booking formatted as 'HHmmss'.
            purpose (str): The Room Booking Nickname value submitted by the user that will be used as the title of the booking.
            notes (str): A string stating when the booking request was made.
            response (dict): The formatted value of a booking transformed for XML creation.

        Private Methods:
            __convert(): Converts the booking to the value of the response attribute.

        """
    def __init__(self, data):
        self.start_date = arrow.get(data['booking_start']).format('YYYYMMDD')
        self.end_date = arrow.get(data['booking_end']).format('YYYYMMDD')
        self.start_time = arrow.get(data['booking_start']).format('HHmmss')
        self.end_time = arrow.get(data['booking_end']).format('HHmmss')
        self.purpose = data['booking_label']
        self.notes = f"Booking created {arrow.get(data['booking_created']).format('MM DD, YYYY')} at {arrow.get(data['booking_created']).format('HH:mm:ss')}."
        self.response = self.__convert()

    def __convert(self):
        return {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'purpose': self.purpose,
            'notes': self.notes,
            'booking_id': str(uuid4()),
            'confidential': 'no',
            'password_protected': 'no',
        }
