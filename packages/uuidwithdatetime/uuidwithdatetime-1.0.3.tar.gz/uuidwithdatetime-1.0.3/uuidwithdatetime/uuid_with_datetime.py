import uuid
from datetime import datetime


def generate_uuid_with_datetime(format_24h=True):
    """
    Generate a random UUID with the current date and time.

    :param format_24h: Boolean to specify if the time should be in 24-hour format (True) or 12-hour format (False).
    :return: String containing the UUID and current date and time.
    """
    current_time = datetime.now()
    if format_24h:
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    else:
        formatted_time = current_time.strftime("%Y-%m-%d %I:%M:%S %p")

    return f"{uuid.uuid4()}{formatted_time.replace(" ","")}"



