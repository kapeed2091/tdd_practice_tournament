from ib_common.models import AbstractDateTimeModel
from django.db import models


class DisplayReport(AbstractDateTimeModel):
    sale_report_reference_no = models.CharField(
        max_length=125, null=True, blank=True)
    payment_report_reference_no = models.CharField(
        max_length=125, null=True, blank=True)
    sale_report_amount = models.FloatField(
        null=True, blank=True)
    payment_report_amount = models.FloatField(
        null=True, blank=True)
    franchise_id = models.PositiveIntegerField()
    transaction_datetime = models.DateTimeField()
    status = models.CharField(max_length=125)
