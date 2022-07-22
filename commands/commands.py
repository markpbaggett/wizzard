from datetime import datetime


class AboutConnector:
    def __init__(self, tz):
        self.tz = tz
        self.response = self.__build_response()

    def __build_response(self):
        return f"""
        <?xml version="1.0"?>
        <kwe:result
            xmlns:kwe="http://www.appliancestudio.com/kwe/1.0"
            xmlns:rb="http://www.appliancestudio.com/rb/1.0"
        >
            <kwe:date>{datetime.now()}</kwe:date>
            <kwe:time>{datetime.now()}</kwe:time>
            <kwe:result_code>0</kwe:result_code>
            <kwe:connector>
                <kwe:name>Mark's Fabulous Room Wizard Connector</kwe:name>
                <kwe:version>3.1</kwe:version>
                <kwe:api name="Room Booking API" version="1.0"></kwe:api>
                <kwe:api name="Room Booking API" version="1.1"></kwe:api>
            </kwe:connector>
        </kwe:result>
        """.strip()
