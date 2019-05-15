from django_swagger_utils.drf_server.exceptions import BadRequest
from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import ValidatorAbstractClass

from display_reports.constants import exception_messages


class ValidatorClass(ValidatorAbstractClass):
    def __init__(self, *args, **kwargs):
        self.request_data = kwargs['request_data']
        self.user = kwargs['user']
        self.access_token = kwargs['access_token']

    def validate_date_range(self):
        date_range = self.request_data['date_range']
        if date_range['from_date'] > date_range['to_date']:
            raise BadRequest(*exception_messages.FROM_DATE_CAN_NOT_BE_GREATER_THAN_TO_DATE)

    def validate(self):
        self.validate_date_range()
