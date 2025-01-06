from django.utils.dateparse import parse_datetime

class DateTimeConverter:
    regex = r'[\w\-:T.]+'

    def to_python(self, value):
        # Convert the string to a datetime object
        return parse_datetime(value)

    def to_url(self, value):
        # Convert the datetime object to an ISO 8601 string
        return value.isoformat()
