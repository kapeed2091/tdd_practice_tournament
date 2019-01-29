def convert_value_wrt_percentage(value, percentage):
    import math

    converted_value = value * (percentage / float(100))
    return int(math.ceil(converted_value))
