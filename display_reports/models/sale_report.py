from ib_common.models import AbstractDateTimeModel
from django.db import models


class SaleReport(AbstractDateTimeModel):
    reference_no = models.CharField(max_length=125)
    amount = models.FloatField()
    transaction_datetime = models.DateTimeField()
    franchise_id = models.PositiveIntegerField()
