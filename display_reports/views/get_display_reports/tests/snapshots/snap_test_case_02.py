# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase02GetDisplayReportsAPITestCase::test_case status'] = 400

snapshots['TestCase02GetDisplayReportsAPITestCase::test_case body'] = {
    'http_status_code': 400,
    'res_status': 'FROM_DATE_CAN_NOT_BE_GREATER_THAN_TO_DATE',
    'response': 'From date can not be greater than To date'
}

snapshots['TestCase02GetDisplayReportsAPITestCase::test_case header_params'] = {
    'content-language': (
        'Content-Language',
        'en'
    ),
    'content-length': (
        'Content-Length',
        '141'
    ),
    'content-type': (
        'Content-Type',
        'text/html; charset=utf-8'
    ),
    'vary': (
        'Vary',
        'Accept-Language, Origin, Cookie'
    ),
    'x-frame-options': (
        'X-Frame-Options',
        'SAMEORIGIN'
    )
}
