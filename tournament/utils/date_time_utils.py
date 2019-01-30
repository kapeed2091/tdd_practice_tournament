def get_current_date_time():
    from django.utils import timezone
    from django.conf import settings
    use_tz = getattr(settings, 'USE_TZ', False)

    if use_tz:
        local_datetime = timezone.localtime()
    else:
        local_datetime = timezone.now()
    return local_datetime
