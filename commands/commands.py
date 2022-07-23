import arrow
from lxml.builder import ElementMaker
from lxml import etree


class GetResponse:
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
    def __init__(self, request_body):
        self.tz = request_body.args.get('time_zone', default='US/Eastern')
        self.date = arrow.utcnow().to(self.tz).format('YYYYMMDD')
        self.time = arrow.utcnow().to(self.tz).format('HHmmss')
        self.version = '0.1'
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
    def __init__(self, request_body):
        super().__init__(request_body)
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
    def __init__(self, request_body):
        super().__init__(request_body)
        self.room_id = request_body.args.get('room_id', default='LIB_605')
        self.range_start_date = request_body.args.get('range_start_date', default="today")
        self.range_start_time = request_body.args.get('range_start_time', default="now")
        self.range_end_date = request_body.args.get('range_end_date', default=arrow.utcnow().to(self.tz).shift(days=+1).format('YYYYMMDD'))
        self.range_end_time = request_body.args.get('range_end_time', default=arrow.utcnow().to(self.tz).shift(days=+1).format('HHmmss'))
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
            self.rb.bookings(
                self.rb.booking(
                    self.rb.start_date(
                        self.range_start_date
                    ),
                    self.rb.end_date(
                        self.range_end_date
                    ),
                    self.rb.start_time('220000'),
                    self.rb.end_time('230000'),
                    self.rb.purpose("Mark's Meeting"),
                    self.rb.notes("Mark rules!"),
                    booking_id="mark123abc",
                    confidential="no",
                    password_protected="no"
                ),
                room_id=self.room_id,
            )
        )
