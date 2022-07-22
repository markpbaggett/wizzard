import arrow


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


class AboutConnector(RoomWizardCommand):
    def __init__(self, request_body):
        super().__init__(request_body)
        self.connector_name = "Mark's Fabulous Room Wizard Connector"
        self.response = self.__build_response().strip()

    def __build_response(self):
        return f"""
        <?xml version="1.0"?>
        <kwe:result
            xmlns:kwe="http://www.appliancestudio.com/kwe/1.0"
            xmlns:rb="http://www.appliancestudio.com/rb/1.0"
        >
            <kwe:date>{self.date}</kwe:date>
            <kwe:time>{self.time}</kwe:time>
            <kwe:result_code>0</kwe:result_code>
            <kwe:connector>
                <kwe:name>{self.connector_name}</kwe:name>
                <kwe:version>0.1</kwe:version>
                <kwe:short>Mark connector</kwe:short>
                <kwe:api name="Room Booking API" version="1.0"/>
            </kwe:connector>
        </kwe:result>
        """


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
        return f"""
        <?xml version="1.0"?>
        <kwe:result
            xmlns:kwe="http://www.appliancestudio.com/kwe/1.0"
            xmlns:rb="http://www.appliancestudio.com/rb/1.0"
        >
            <kwe:date>{self.date}</kwe:date>
            <kwe:time>{self.time}</kwe:time>
            <kwe:result_code>0</kwe:result_code>
            <kwe:connector>
                <kwe:version>3.1</kwe:version>
                <kwe:api name="Room Booking API" version="1.0"></kwe:api>
                <kwe:api name="Room Booking API" version="1.1"></kwe:api>
                <rb:bookings room_id="{self.room_id}">
                    <rb:booking booking_id="mark123abc" confidential="no" password_protected="no">
                        <rb:start_date>
                            {self.range_start_date}
                        </rb:start_date>
                        <rb:end_date>
                            {self.range_start_date}
                        </rb:end_date>
                        <rb:start_time>
                            220000
                        </rb:start_time>
                        <rb:end_time>
                            230000
                        </rb:end_time>
                        <rb:purpose>
                            Mark's Meeting
                        </rb:purpose>
                        <rb:notes>
                            Mark rules!
                        </rb:notes>
                    </rb:booking>
                </rb:bookings>
            </kwe:connector>
        </kwe:result>
        """


class AddBooking(RoomWizardCommand):
    def __init__(self, request_body):
        super().__init__(request_body)
        self.room_id = request_body.args.get('room_id', default='LIB_605')
        self.range_start_date = request_body.args.get('range_start_date', default="today")
        self.range_start_time = request_body.args.get('range_start_time', default="now")
        self.range_end_date = request_body.args.get('range_end_date',
                                                    default=arrow.utcnow().to(self.tz).shift(days=+1).format(
                                                        'YYYYMMDD'))
        self.range_end_time = request_body.args.get('range_end_time',
                                                    default=arrow.utcnow().to(self.tz).shift(days=+1).format('HHmmss'))
