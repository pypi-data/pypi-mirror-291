import re
from datetime import datetime


def validate_phone(phone):
    """Validate that the phone number consists of exactly 10 digits."""
    return phone.isdigit() and len(phone) == 10


def validate_name(name):
    """Validate that the name contains only letters and spaces."""
    return re.match("^[A-Za-z\s]+$", name) is not None


def validate_email(email):
    """Validate that the email has a valid format."""
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) is not None


def validate_birthday(birthday):
    """Validate that the birthday is in the format DD.MM.YYYY."""
    try:
        datetime.strptime(birthday, "%d.%m.%Y")
        return True
    except ValueError:
        return False
    
    
def validate_address(address):
    """Validate that the address is not empty and contains only valid characters."""
    return bool(address) and re.match("^[A-Za-z0-9\s,.-]+$", address) is not None