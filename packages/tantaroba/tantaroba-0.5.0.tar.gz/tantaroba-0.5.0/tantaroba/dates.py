import datetime


def now2str() -> str:
    """
    Get current datetime and transform it to string with the format yyyymmdd_hhmmss

    Returns:
        str: foramtted string of datetime.
    """
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def today2str() -> str:
    """
    Get current datetime and transform it to string with the format yyyymmdd

    Returns:
        str: foramtted string of datetime.
    """
    return datetime.date.today().strftime("%Y%m%d")
