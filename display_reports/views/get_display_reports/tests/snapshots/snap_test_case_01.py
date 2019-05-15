# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase01GetDisplayReportsAPITestCase::test_case status'] = 200

snapshots['TestCase01GetDisplayReportsAPITestCase::test_case body'] = {
    'display_reports': [
        {
            'payment_report_amount': 100.0,
            'payment_report_reference_no': 'Ref11',
            'sale_report_amount': 100.0,
            'sale_report_reference_no': 'Ref11',
            'status': 'MATCHED'
        },
        {
            'payment_report_amount': 100.0,
            'payment_report_reference_no': 'Ref13',
            'sale_report_amount': 100.0,
            'sale_report_reference_no': 'Ref13',
            'status': 'MATCHED'
        }
    ]
}

snapshots['TestCase01GetDisplayReportsAPITestCase::test_case header_params'] = {
    'allow': (
        'Allow',
        'POST, OPTIONS'
    ),
    'content-language': (
        'Content-Language',
        'en'
    ),
    'content-length': (
        'Content-Length',
        '323'
    ),
    'content-type': (
        'Content-Type',
        'application/json'
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
