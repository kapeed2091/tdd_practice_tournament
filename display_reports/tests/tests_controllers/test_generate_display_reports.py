import pytest
from django_swagger_utils.drf_server.exceptions import BadRequest


def test_invalid_date_range():
    from datetime import datetime
    from display_reports.views.generate_display_reports.api_wrapper import api_wrapper

    request_data = {
        "date_range": {
            "from_date": datetime(year=2018, month=03, day=15).date(),
            "to_date": datetime(year=2018, month=03, day=10).date()
        },
        "franchise_ids": [1, 2]
    }

    with pytest.raises(BadRequest):
        api_wrapper(request_data=request_data, access_token=None, user=None)
