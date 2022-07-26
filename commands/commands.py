import arrow
from lxml.builder import ElementMaker
from lxml import etree
from booking.booking import Room


class GetResponse:
    """
    A class that interfaces with the controller and directs routes to the appropriate Class based on HTTP parameters.

    Parameters:
        request_body (Request): The content, status code, headers, etc. associated with the incoming HTTP request.

    Attributes:
        command (str): the API associated with the request (about_connector, get_bookings)
        response (bytes): the XML response of the associated request

    Private Methods:
        __get_command(request_body): gets XML response as bytes from the appropriate class.

    """
    def __init__(self, request_body):
        self.command = request_body.args.get('command', default='about_connector')
        self.response = self.__get_command(request_body)

    def __get_command(self, request_body):
        commands = {
            'about_connector': AboutConnector(request_body),
            'get_bookings': GetBookings(request_body),
        }
        return commands[self.command].response


class RoomWizardCommand:
    """
        The base class for all RoomWizard APIs.  Handles request_bodies and defines inheritable attributes.

        Parameters:
            request_body (Request): The content, status code, headers, etc. associated with the incoming HTTP request.

        Attributes:
            tz (str): The timezone from HTTP parameters specified in the request (defaults to 'US/Eastern')
            date (str): The current date on server formatted as YYYYMMDD
            time (str): The current time on server formatted as HHmmss
            version (str): The version of the connector. (see TODO)

        Private Methods:
            __get_command(request_body): gets XML response as bytes from the appropriate class.

    """
    def __init__(self, request_body):
        self.tz = request_body.args.get('time_zone', default='US/Eastern')
        self.date = arrow.utcnow().to(self.tz).format('YYYYMMDD')
        self.time = arrow.utcnow().to(self.tz).format('HHmmss')
        self.version = '0.1'
        # TODO: version should be set elsewhere.
        self.kwe = self.__build_namespace("http://www.appliancestudio.com/kwe/1.0/", 'kwe')
        self.rb = self.__build_namespace("http://www.appliancestudio.com/rb/1.0/", 'rb')

    @staticmethod
    def __build_namespace(uri, short):
        return ElementMaker(
            namespace=uri,
            nsmap={
                short: uri,
            }
        )


class AboutConnector(RoomWizardCommand):
    """
    The class to represent a RoomWizards about_connector request.

    Parameters:
        request_body (Request): The content, status code, headers, etc. associated with the incoming HTTP request.

    Attributes:
        connector_name (str): The name of the connector (see TODO)
        response (bytes): Information about the connector as XML

    Private Methods:
        __build_response(): Returns and pretty prints XML for about_connector as bytes
        __build_xml(): Returns XML for about_connector as an lxml.etree.Element

    """
    def __init__(self, request_body):
        super().__init__(request_body)
        # TODO: Make connector_name more easily mutable.
        self.connector_name = "Mark's Fabulous Room Wizard Connector"
        self.response = self.__build_response().strip()

    def __build_response(self):
        return etree.tostring(
            self.__build_xml(),
            pretty_print=True
        )

    def __build_xml(self):
        return self.kwe.result(
            self.kwe.date(self.date),
            self.kwe.time(self.time),
            self.kwe.result_code('0'),
            self.kwe.connector(
                self.kwe.name(self.connector_name),
                self.kwe.version('0.1'),
                self.kwe.short('Mark connector'),
                self.kwe.api(
                    name="Room Booking API",
                    version="1.0"
                )
            )
        )


class GetBookings(RoomWizardCommand):
    """
    The class to represent a RoomWizards get_bookings request.

    Parameters:
        request_body (Request): The content, status code, headers, etc. associated with the incoming HTTP request.

    Attributes:
        room_id (str): The room id of the Room Wizard that is being requested
        range_start_date (str): The starting date for a get_bookings request
        range_start_time (str): The starting time for a get_bookings request
        range_end_date (str): The ending date for a get_bookings request
        range_end_time (str): The ending time for a get_bookings request
        response (bytes): Information about the connector as XML

    Private Methods:
        __build_response(): Returns and pretty prints XML for get_bookings as bytes
        __build_xml(): Returns XML for get_bookings as an lxml.etree.Element

    """
    def __init__(self, request_body):
        super().__init__(request_body)
        self.room_id = request_body.args.get('room_id', default='LIB_605')
        self.range_start_date = request_body.args.get('range_start_date', default="today")
        self.range_start_time = request_body.args.get('range_start_time', default="now")
        self.range_end_date = request_body.args.get(
            'range_end_date', default=arrow.utcnow().to(self.tz).shift(days=+1).format('YYYYMMDD')
        )
        self.range_end_time = request_body.args.get(
            'range_end_time', default=arrow.utcnow().to(self.tz).shift(days=+1).format('HHmmss')
        )
        self.response = self.__build_response().strip()

    def __build_response(self):
        return etree.tostring(
            self.__build_xml(),
            pretty_print=True
        )

    def __build_xml(self):
        return self.kwe.result(
            self.kwe.date(self.date),
            self.kwe.time(self.time),
            self.kwe.result_code('0'),
            self.__get_bookings_for_room()
        )

    def __get_bookings_for_room(self):
        bookings = Room(self.room_id).get_bookings()
        response = self.rb.bookings(room_id=self.room_id)
        for booking in bookings:
            response.append(
                self.rb.booking(
                    self.rb.start_date(
                        booking['start_date']
                    ),
                    self.rb.end_date(
                        booking['end_date']
                    ),
                    self.rb.start_time(
                        booking['start_time']
                    ),
                    self.rb.end_time(
                        booking['end_time']
                    ),
                    self.rb.purpose(
                        booking['purpose']
                    ),
                    self.rb.notes(
                        booking['notes']
                    ),
                    booking_id=booking['booking_id'],
                    confidential="no",
                    password_protected="no"
                )
            )
        return response
