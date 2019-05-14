from mock import create_autospec

from display_reports.constants.general import DisplayReportStatus


def test_generate_display_reports_with_status_matched():
    from datetime import datetime
    from display_reports.storage.storage import Storage
    from display_reports.utils.display_report_utils import DisplayReportUtils

    date_range = {
        "from_date": datetime(year=2019, month=03, day=10).date(),
        "to_date": datetime(year=2019, month=03, day=15).date()
    }
    franchise_ids = [1, 2, 3]

    display_report_utils = DisplayReportUtils()
    storage_mock = create_autospec(Storage)
    storage_mock.get_sale_reports.return_value = [
        {
            "ref_no": "Ref1234",
            "amount": 100
        }
    ]

    storage_mock.get_payment_reports.return_value = [
        {
            "ref_no": "Ref1234",
            "amount": 100
        }
    ]

    display_report_utils.generate_display_reports(
        date_range=date_range, franchise_ids=franchise_ids,
        storage=storage_mock
    )

    storage_mock.get_sale_reports.assert_called_once_with(
        date_range=date_range, franchise_ids=franchise_ids
    )
    storage_mock.get_payment_reports.assert_called_once_with(
        date_range=date_range, franchise_ids=franchise_ids
    )
    storage_mock.create_display_reports.assert_called_once_with(
        display_reports=[
            {
                "sale_report_ref_no": "Ref1234",
                "payment_report_ref_no": "Ref1234",
                "sale_report_amount": 100,
                "payment_report_amount": 100,
                "status": DisplayReportStatus.MATCHED.value
            }
        ]
    )


def test_generate_display_reports_with_status_amount_mismatch():
    from datetime import datetime
    from display_reports.storage.storage import Storage
    from display_reports.utils.display_report_utils import DisplayReportUtils

    date_range = {
        "from_date": datetime(year=2019, month=03, day=10).date(),
        "to_date": datetime(year=2019, month=03, day=15).date()
    }
    franchise_ids = [1, 2, 3]

    display_report_utils = DisplayReportUtils()
    storage_mock = create_autospec(Storage)
    storage_mock.get_sale_reports.return_value = [
        {
            "ref_no": "Ref1234",
            "amount": 150
        }
    ]

    storage_mock.get_payment_reports.return_value = [
        {
            "ref_no": "Ref1234",
            "amount": 100
        }
    ]

    display_report_utils.generate_display_reports(
        date_range=date_range, franchise_ids=franchise_ids,
        storage=storage_mock
    )

    storage_mock.get_sale_reports.assert_called_once_with(
        date_range=date_range, franchise_ids=franchise_ids
    )
    storage_mock.get_payment_reports.assert_called_once_with(
        date_range=date_range, franchise_ids=franchise_ids
    )
    storage_mock.create_display_reports.assert_called_once_with(
        display_reports=[
            {
                "sale_report_ref_no": "Ref1234",
                "payment_report_ref_no": "Ref1234",
                "sale_report_amount": 150,
                "payment_report_amount": 100,
                "status": DisplayReportStatus.AMOUNT_MISMATCH.value
            }
        ]
    )

def test_generate_display_reports_with_status_Ref_no_mismatch():
    from datetime import datetime
    from display_reports.storage.storage import Storage
    from display_reports.utils.display_report_utils import DisplayReportUtils

    date_range = {
        "from_date": datetime(year=2019, month=03, day=10).date(),
        "to_date": datetime(year=2019, month=03, day=15).date()
    }
    franchise_ids = [1, 2, 3]

    display_report_utils = DisplayReportUtils()
    storage_mock = create_autospec(Storage)
    storage_mock.get_sale_reports.return_value = [
        {
            "ref_no": "Ref1234",
            "amount": 100
        }
    ]

    storage_mock.get_payment_reports.return_value = [
        {
            "ref_no": "Ref2345",
            "amount": 100
        }
    ]

    display_report_utils.generate_display_reports(
        date_range=date_range, franchise_ids=franchise_ids,
        storage=storage_mock
    )

    storage_mock.get_sale_reports.assert_called_once_with(
        date_range=date_range, franchise_ids=franchise_ids
    )
    storage_mock.get_payment_reports.assert_called_once_with(
        date_range=date_range, franchise_ids=franchise_ids
    )
    storage_mock.create_display_reports.assert_called_once_with(
        display_reports=[
            {
                "sale_report_ref_no": "Ref1234",
                "payment_report_ref_no": "Ref2345",
                "sale_report_amount": 100,
                "payment_report_amount": 100,
                "status": DisplayReportStatus.REF_NO_MISMATCH.value
            }
        ]
    )

def test_generate_display_reports_with_status_extra_sale():
    from datetime import datetime
    from display_reports.storage.storage import Storage
    from display_reports.utils.display_report_utils import DisplayReportUtils

    date_range = {
        "from_date": datetime(year=2019, month=03, day=10).date(),
        "to_date": datetime(year=2019, month=03, day=15).date()
    }
    franchise_ids = [1, 2, 3]

    display_report_utils = DisplayReportUtils()
    storage_mock = create_autospec(Storage)
    storage_mock.get_sale_reports.return_value = [
        {
            "ref_no": "Ref1234",
            "amount": 100
        }
    ]

    storage_mock.get_payment_reports.return_value = []

    display_report_utils.generate_display_reports(
        date_range=date_range, franchise_ids=franchise_ids,
        storage=storage_mock
    )

    storage_mock.get_sale_reports.assert_called_once_with(
        date_range=date_range, franchise_ids=franchise_ids
    )
    storage_mock.get_payment_reports.assert_called_once_with(
        date_range=date_range, franchise_ids=franchise_ids
    )
    storage_mock.create_display_reports.assert_called_once_with(
        display_reports=[
            {
                "sale_report_ref_no": "Ref1234",
                "payment_report_ref_no": None,
                "sale_report_amount": 100,
                "payment_report_amount": None,
                "status": DisplayReportStatus.EXTRA_SALE.value
            }
        ]
    )

def test_generate_display_reports_with_status_unbilled():
    from datetime import datetime
    from display_reports.storage.storage import Storage
    from display_reports.utils.display_report_utils import DisplayReportUtils

    date_range = {
        "from_date": datetime(year=2019, month=03, day=10).date(),
        "to_date": datetime(year=2019, month=03, day=15).date()
    }
    franchise_ids = [1, 2, 3]

    display_report_utils = DisplayReportUtils()
    storage_mock = create_autospec(Storage)
    storage_mock.get_sale_reports.return_value = []

    storage_mock.get_payment_reports.return_value = [
        {
            "ref_no": "Ref1234",
            "amount": 100
        }
    ]

    display_report_utils.generate_display_reports(
        date_range=date_range, franchise_ids=franchise_ids,
        storage=storage_mock
    )

    storage_mock.get_sale_reports.assert_called_once_with(
        date_range=date_range, franchise_ids=franchise_ids
    )
    storage_mock.get_payment_reports.assert_called_once_with(
        date_range=date_range, franchise_ids=franchise_ids
    )
    storage_mock.create_display_reports.assert_called_once_with(
        display_reports=[
            {
                "sale_report_ref_no": None,
                "payment_report_ref_no": "Ref1234",
                "sale_report_amount": None,
                "payment_report_amount": 100,
                "status": DisplayReportStatus.UN_BILLED.value
            }
        ]
    )

def test_generate_display_reports_payment_report_should_be_mapped_to_only_one_sale_report():
    from datetime import datetime
    from display_reports.storage.storage import Storage
    from display_reports.utils.display_report_utils import DisplayReportUtils

    date_range = {
        "from_date": datetime(year=2019, month=03, day=10).date(),
        "to_date": datetime(year=2019, month=03, day=15).date()
    }
    franchise_ids = [1, 2, 3]

    display_report_utils = DisplayReportUtils()
    storage_mock = create_autospec(Storage)
    storage_mock.get_sale_reports.return_value = [
        {
            "ref_no": "Ref1234",
            "amount": 100
        },
        {
            "ref_no": "Ref23",
            "amount": 100
        }
    ]

    storage_mock.get_payment_reports.return_value = [
        {
            "ref_no": "Ref1234",
            "amount": 100
        }
    ]

    display_report_utils.generate_display_reports(
        date_range=date_range, franchise_ids=franchise_ids,
        storage=storage_mock
    )

    storage_mock.get_sale_reports.assert_called_once_with(
        date_range=date_range, franchise_ids=franchise_ids
    )
    storage_mock.get_payment_reports.assert_called_once_with(
        date_range=date_range, franchise_ids=franchise_ids
    )
    storage_mock.create_display_reports.assert_called_once_with(
        display_reports=[
            {
                "sale_report_ref_no": "Ref1234",
                "payment_report_ref_no": "Ref1234",
                "sale_report_amount": 100,
                "payment_report_amount": 100,
                "status": DisplayReportStatus.MATCHED.value
            },
            {
                "sale_report_ref_no": "Ref23",
                "payment_report_ref_no": None,
                "sale_report_amount": 100,
                "payment_report_amount": None,
                "status": DisplayReportStatus.EXTRA_SALE.value
            }
        ]
    )

def test_generate_display_reports_with_order_of_generation_matched_and_amount_mismatch_and_ref_no_mismatch():
    from datetime import datetime
    from display_reports.storage.storage import Storage
    from display_reports.utils.display_report_utils import DisplayReportUtils

    date_range = {
        "from_date": datetime(year=2019, month=03, day=10).date(),
        "to_date": datetime(year=2019, month=03, day=15).date()
    }
    franchise_ids = [1, 2, 3]

    display_report_utils = DisplayReportUtils()
    storage_mock = create_autospec(Storage)
    storage_mock.get_sale_reports.return_value = [
        {
            "ref_no": "Ref1234",
            "amount": 100
        },
        {
            "ref_no": "Ref234",
            "amount": 150
        },
        {
            "ref_no": "Ref24",
            "amount": 150
        }
    ]

    storage_mock.get_payment_reports.return_value = [
        {
            "ref_no": "Ref23",
            "amount": 150
        },
        {
            "ref_no": "Ref234",
            "amount": 100
        },
        {
            "ref_no": "Ref1234",
            "amount": 100
        }
    ]

    display_report_utils.generate_display_reports(
        date_range=date_range, franchise_ids=franchise_ids,
        storage=storage_mock
    )

    storage_mock.get_sale_reports.assert_called_once_with(
        date_range=date_range, franchise_ids=franchise_ids
    )
    storage_mock.get_payment_reports.assert_called_once_with(
        date_range=date_range, franchise_ids=franchise_ids
    )
    storage_mock.create_display_reports.assert_called_once_with(
        display_reports=[
            {
                "sale_report_ref_no": "Ref1234",
                "payment_report_ref_no": "Ref1234",
                "sale_report_amount": 100,
                "payment_report_amount": 100,
                "status": DisplayReportStatus.MATCHED.value
            },
            {
                "sale_report_ref_no": "Ref234",
                "payment_report_ref_no": "Ref234",
                "sale_report_amount": 150,
                "payment_report_amount": 100,
                "status": DisplayReportStatus.AMOUNT_MISMATCH.value
            },
            {
                "sale_report_ref_no": "Ref24",
                "payment_report_ref_no": "Ref23",
                "sale_report_amount": 150,
                "payment_report_amount": 150,
                "status": DisplayReportStatus.REF_NO_MISMATCH.value
            }
        ]
    )
