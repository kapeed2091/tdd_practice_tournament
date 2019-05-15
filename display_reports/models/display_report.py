from ib_common.models import AbstractDateTimeModel
from django.db import models


class DisplayReport(AbstractDateTimeModel):
    sale_report_reference_no = models.CharField(max_length=125)
    payment_report_reference_no = models.CharField(max_length=125)
    sale_report_amount = models.FloatField()
    payment_report_amount = models.FloatField()
    franchise_id = models.PositiveIntegerField()
    status = models.CharField(max_length=125)
