from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    request_data = kwargs['request_data']
    date_range = request_data['date_range']
    franchise_ids = request_data['franchise_ids']

    from display_reports.interactors.display_report_interactor import DisplayReportInteractor
    from display_reports.storage.storage_impl import StorageImplementation
    from display_reports.presenters.preseenter_csv_impl import PresenterCsvImpl

    storage = StorageImplementation()
    presenter = PresenterCsvImpl()
    display_report_interactor = DisplayReportInteractor(
        date_range=date_range, franchise_ids=franchise_ids, storage=storage
    )
    file_path = display_report_interactor.get_display_reports(presenter)
    return {
        "file_path": file_path
    }
