from libcal.libcal import RoomBookings
import arrow
from uuid import uuid4


class RoomWizard:
    def __init__(self, room_name):
        self.room_name = room_name

    def get_bookings(self, date="today"):
        """Get the Bookings of a particular RoomWizard on a specific date."""
        all_bookings = RoomBookings('10024', arrow.utcnow().format('YYYYMMDD')).get_bookings()
        return [Booking(booking).response for booking in all_bookings['bookings']['timeslots'] if self.room_name == booking['room_name']]


class Booking:
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
