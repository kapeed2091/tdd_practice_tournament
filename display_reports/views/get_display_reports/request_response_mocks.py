

REQUEST_BODY_JSON = """
{
    "date_range": {
        "from_date": "2099-12-31", 
        "to_date": "2099-12-31"
    }, 
    "franchise_ids": [
        1
    ]
}
"""


RESPONSE_200_JSON = """
{
    "display_reports": [
        {
            "status": "string", 
            "payment_report_reference_no": "string", 
            "payment_report_amount": 1.1, 
            "sale_report_reference_no": "string", 
            "sale_report_amount": 1.1
        }
    ]
}
"""

