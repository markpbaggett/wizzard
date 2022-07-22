import arrow
from flask import request


class GetResponse:
    def __init__(self, request_body):
        self.command = request_body.args.get('command', default='about_connector')
        self.response = self.__get_command(request_body)

    def __get_command(self, request_body):
        commands = {
            'about_connector': AboutConnector(request_body.args.get('time_zone', default='US/Eastern'))
        }
        return commands[self.command].response


class RoomWizardCommand:
    def __init__(self, tz):
        self.tz = tz
        self.date = arrow.utcnow().to(tz).format('YYYYMMDD')
        self.time = arrow.utcnow().to(tz).format('HHmmss')


class AboutConnector(RoomWizardCommand):
    def __init__(self, tz):
        super().__init__(tz)
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
                <kwe:version>3.1</kwe:version>
                <kwe:api name="Room Booking API" version="1.0"></kwe:api>
                <kwe:api name="Room Booking API" version="1.1"></kwe:api>
            </kwe:connector>
        </kwe:result>
        """
