from mock import create_autospec

from display_reports.constants.general import DisplayReportStatus


def test_generate_display_reports_with_status_matched():
    from datetime import datetime
    from display_reports.storage.storage import Storage

    date_range = {
        "from_date": datetime(year=2019, month=03, day=10).date(),
        "to_date": datetime(year=2019, month=03, day=15).date()
    }
    franchise_ids = [1, 2, 3]

    storage_mock = create_autospec(Storage)
    storage_mock.get_sale_reports.return_value = [
        {
            "ref_no": "Ref1234",
            "amount": 100,
            "franchise_id": 1,
            "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12)
        }
    ]

    storage_mock.get_payment_reports.return_value = [
        {
            "ref_no": "Ref1234",
            "amount": 100,
            "franchise_id": 1,
            "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12)
        }
    ]

    from display_reports.interactors.display_report_interactor import DisplayReportInteractor
    display_report_interactor = DisplayReportInteractor(
        date_range=date_range, franchise_ids=franchise_ids,
        storage=storage_mock
    )

    display_report_interactor.generate_display_reports()
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
                "franchise_id": 1,
                "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12),
                "status": DisplayReportStatus.MATCHED.value
            }
        ]
    )


def test_generate_display_reports_with_status_amount_mismatch():
    from datetime import datetime
    from display_reports.storage.storage import Storage
    from display_reports.interactors.display_report_interactor import DisplayReportInteractor

    date_range = {
        "from_date": datetime(year=2019, month=03, day=10).date(),
        "to_date": datetime(year=2019, month=03, day=15).date()
    }
    franchise_ids = [1, 2, 3]

    storage_mock = create_autospec(Storage)
    storage_mock.get_sale_reports.return_value = [
        {
            "ref_no": "Ref1234",
            "amount": 150,
            "franchise_id": 1,
            "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12)
        }
    ]

    storage_mock.get_payment_reports.return_value = [
        {
            "ref_no": "Ref1234",
            "amount": 100,
            "franchise_id": 1,
            "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12)
        }
    ]

    display_report_interactor = DisplayReportInteractor(
        date_range=date_range, franchise_ids=franchise_ids,
        storage=storage_mock
    )

    display_report_interactor.generate_display_reports()

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
                "franchise_id": 1,
                "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12),
                "status": DisplayReportStatus.AMOUNT_MISMATCH.value
            }
        ]
    )


def test_generate_display_reports_with_status_Ref_no_mismatch():
    from datetime import datetime
    from display_reports.storage.storage import Storage
    from display_reports.interactors.display_report_interactor import DisplayReportInteractor

    date_range = {
        "from_date": datetime(year=2019, month=03, day=10).date(),
        "to_date": datetime(year=2019, month=03, day=15).date()
    }
    franchise_ids = [1, 2, 3]

    storage_mock = create_autospec(Storage)
    storage_mock.get_sale_reports.return_value = [
        {
            "ref_no": "Ref1234",
            "amount": 100,
            "franchise_id": 1,
            "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12)
        }
    ]

    storage_mock.get_payment_reports.return_value = [
        {
            "ref_no": "Ref2345",
            "amount": 100,
            "franchise_id": 1,
            "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12)
        }
    ]

    display_report_interactor = DisplayReportInteractor(
        date_range=date_range, franchise_ids=franchise_ids,
        storage=storage_mock
    )

    display_report_interactor.generate_display_reports()
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
                "franchise_id": 1,
                "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12),
                "status": DisplayReportStatus.REF_NO_MISMATCH.value
            }
        ]
    )


def test_generate_display_reports_with_status_extra_sale():
    from datetime import datetime
    from display_reports.storage.storage import Storage
    from display_reports.interactors.display_report_interactor import DisplayReportInteractor

    date_range = {
        "from_date": datetime(year=2019, month=03, day=10).date(),
        "to_date": datetime(year=2019, month=03, day=15).date()
    }
    franchise_ids = [1, 2, 3]

    storage_mock = create_autospec(Storage)
    storage_mock.get_sale_reports.return_value = [
        {
            "ref_no": "Ref1234",
            "amount": 100,
            "franchise_id": 1,
            "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12)
        }
    ]

    storage_mock.get_payment_reports.return_value = []

    display_report_interactor = DisplayReportInteractor(
        date_range=date_range, franchise_ids=franchise_ids,
        storage=storage_mock
    )

    display_report_interactor.generate_display_reports()

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
                "franchise_id": 1,
                "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12),
                "status": DisplayReportStatus.EXTRA_SALE.value
            }
        ]
    )


def test_generate_display_reports_with_status_unbilled():
    from datetime import datetime
    from display_reports.storage.storage import Storage
    from display_reports.interactors.display_report_interactor import DisplayReportInteractor

    date_range = {
        "from_date": datetime(year=2019, month=03, day=10).date(),
        "to_date": datetime(year=2019, month=03, day=15).date()
    }
    franchise_ids = [1, 2, 3]

    storage_mock = create_autospec(Storage)
    storage_mock.get_sale_reports.return_value = []

    storage_mock.get_payment_reports.return_value = [
        {
            "ref_no": "Ref1234",
            "amount": 100,
            "franchise_id": 1,
            "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12)
        }
    ]

    display_report_interactor = DisplayReportInteractor(
        date_range=date_range, franchise_ids=franchise_ids,
        storage=storage_mock
    )

    display_report_interactor.generate_display_reports()

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
                "franchise_id": 1,
                "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12),
                "status": DisplayReportStatus.UN_BILLED.value
            }
        ]
    )


def test_generate_display_reports_payment_report_should_be_mapped_to_only_one_sale_report():
    from datetime import datetime
    from display_reports.storage.storage import Storage
    from display_reports.interactors.display_report_interactor import DisplayReportInteractor

    date_range = {
        "from_date": datetime(year=2019, month=03, day=10).date(),
        "to_date": datetime(year=2019, month=03, day=15).date()
    }
    franchise_ids = [1, 2, 3]

    storage_mock = create_autospec(Storage)
    storage_mock.get_sale_reports.return_value = [
        {
            "ref_no": "Ref1234",
            "amount": 100,
            "franchise_id": 1,
            "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12)
        },
        {
            "ref_no": "Ref23",
            "amount": 100,
            "franchise_id": 1,
            "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12)
        }
    ]

    storage_mock.get_payment_reports.return_value = [
        {
            "ref_no": "Ref1234",
            "amount": 100,
            "franchise_id": 1,
            "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12)
        }
    ]

    display_report_interactor = DisplayReportInteractor(
        date_range=date_range, franchise_ids=franchise_ids, storage=storage_mock
    )

    display_report_interactor.generate_display_reports()
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
                "franchise_id": 1,
                "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12),
                "status": DisplayReportStatus.MATCHED.value
            },
            {
                "sale_report_ref_no": "Ref23",
                "payment_report_ref_no": None,
                "sale_report_amount": 100,
                "payment_report_amount": None,
                "franchise_id": 1,
                "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12),
                "status": DisplayReportStatus.EXTRA_SALE.value
            }
        ]
    )


def test_generate_display_reports_with_order_of_generation_matched_and_amount_mismatch_and_ref_no_mismatch():
    from datetime import datetime
    from display_reports.storage.storage import Storage
    from display_reports.interactors.display_report_interactor import DisplayReportInteractor

    date_range = {
        "from_date": datetime(year=2019, month=03, day=10).date(),
        "to_date": datetime(year=2019, month=03, day=15).date()
    }
    franchise_ids = [1, 2, 3]

    storage_mock = create_autospec(Storage)
    storage_mock.get_sale_reports.return_value = [
        {
            "ref_no": "Ref1234",
            "amount": 100,
            "franchise_id": 1,
            "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12)
        },
        {
            "ref_no": "Ref234",
            "amount": 150,
            "franchise_id": 1,
            "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12)
        },
        {
            "ref_no": "Ref24",
            "amount": 150,
            "franchise_id": 1,
            "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12)
        }
    ]

    storage_mock.get_payment_reports.return_value = [
        {
            "ref_no": "Ref23",
            "amount": 150,
            "franchise_id": 1,
            "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12)
        },
        {
            "ref_no": "Ref234",
            "amount": 100,
            "franchise_id": 1,
            "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12)
        },
        {
            "ref_no": "Ref1234",
            "amount": 100,
            "franchise_id": 1,
            "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12)
        }
    ]

    display_report_interactor = DisplayReportInteractor(
        date_range=date_range, franchise_ids=franchise_ids,
        storage=storage_mock
    )

    display_report_interactor.generate_display_reports()
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
                "franchise_id": 1,
                "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12),
                "status": DisplayReportStatus.MATCHED.value
            },
            {
                "sale_report_ref_no": "Ref234",
                "payment_report_ref_no": "Ref234",
                "sale_report_amount": 150,
                "payment_report_amount": 100,
                "franchise_id": 1,
                "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12),
                "status": DisplayReportStatus.AMOUNT_MISMATCH.value
            },
            {
                "sale_report_ref_no": "Ref24",
                "payment_report_ref_no": "Ref23",
                "sale_report_amount": 150,
                "payment_report_amount": 150,
                "franchise_id": 1,
                "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12),
                "status": DisplayReportStatus.REF_NO_MISMATCH.value
            }
        ]
    )


def test_generate_display_reports_only_same_franchise_reports_should_be_mapped():
    from datetime import datetime
    from display_reports.storage.storage import Storage
    from display_reports.interactors.display_report_interactor import DisplayReportInteractor

    date_range = {
        "from_date": datetime(year=2019, month=03, day=10).date(),
        "to_date": datetime(year=2019, month=03, day=15).date()
    }
    franchise_ids = [1, 2, 3]

    storage_mock = create_autospec(Storage)
    storage_mock.get_sale_reports.return_value = [
        {
            "ref_no": "Ref1234",
            "amount": 100,
            "franchise_id": 1,
            "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12)
        },
        {
            "ref_no": "Ref234",
            "amount": 100,
            "franchise_id": 2,
            "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12)
        }
    ]

    storage_mock.get_payment_reports.return_value = [
        {
            "ref_no": "Ref234",
            "amount": 100,
            "franchise_id": 2,
            "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12)
        },
        {
            "ref_no": "Ref1234",
            "amount": 100,
            "franchise_id": 1,
            "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12)
        }
    ]

    display_report_interactor = DisplayReportInteractor(
        date_range=date_range, franchise_ids=franchise_ids,
        storage=storage_mock
    )

    display_report_interactor.generate_display_reports()
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
                "franchise_id": 1,
                "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12),
                "status": DisplayReportStatus.MATCHED.value
            },
            {
                "sale_report_ref_no": "Ref234",
                "payment_report_ref_no": "Ref234",
                "sale_report_amount": 100,
                "payment_report_amount": 100,
                "franchise_id": 2,
                "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12),
                "status": DisplayReportStatus.MATCHED.value
            }
        ]
    )


def test_generate_display_reports_transaction_datetime_is_considered_from_sale_report_if_exists_else_of_payment_report():
    from datetime import datetime
    from display_reports.storage.storage import Storage
    from display_reports.interactors.display_report_interactor import DisplayReportInteractor

    date_range = {
        "from_date": datetime(year=2019, month=03, day=10).date(),
        "to_date": datetime(year=2019, month=03, day=15).date()
    }
    franchise_ids = [1, 2, 3]

    storage_mock = create_autospec(Storage)
    storage_mock.get_sale_reports.return_value = [
        {
            "ref_no": "Ref1234",
            "amount": 100,
            "franchise_id": 1,
            "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12)
        }
    ]

    storage_mock.get_payment_reports.return_value = [
        {
            "ref_no": "Ref1234",
            "amount": 100,
            "franchise_id": 1,
            "transaction_datetime": datetime(year=2019, month=03, day=12, hour=13)
        },
        {
            "ref_no": "Ref234",
            "amount": 100,
            "franchise_id": 1,
            "transaction_datetime": datetime(year=2019, month=03, day=13, hour=12)
        }
    ]

    display_report_interactor = DisplayReportInteractor(
        date_range=date_range, franchise_ids=franchise_ids, storage=storage_mock
    )

    display_report_interactor.generate_display_reports()
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
                "franchise_id": 1,
                "transaction_datetime": datetime(year=2019, month=03, day=12, hour=12),
                "status": DisplayReportStatus.MATCHED.value
            },
            {
                "sale_report_ref_no": None,
                "payment_report_ref_no": "Ref234",
                "sale_report_amount": None,
                "payment_report_amount": 100,
                "franchise_id": 1,
                "transaction_datetime": datetime(year=2019, month=03, day=13, hour=12),
                "status": DisplayReportStatus.UN_BILLED.value
            }
        ]
    )
