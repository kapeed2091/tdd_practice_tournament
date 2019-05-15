from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    # ---------MOCK IMPLEMENTATION---------
    try:
        from display_reports.views.send_display_reports_to_franchise_team.tests.test_case_01 \
            import TEST_CASE as test_case
    except ImportError:
        from display_reports.views.send_display_reports_to_franchise_team.tests.test_case_01 \
            import test_case

    from django_swagger_utils.drf_server.utils.server_gen.mock_response \
        import mock_response
    try:
        from display_reports.views.send_display_reports_to_franchise_team.request_response_mocks \
            import RESPONSE_200_JSON
    except ImportError:
        RESPONSE_200_JSON = ''
    response_tuple = mock_response(
        app_name="display_reports", test_case=test_case,
        operation_name="send_display_reports_to_franchise_team",
        kwargs=kwargs, default_response_body=RESPONSE_200_JSON)
    return response_tuple[1]

