"""
Validation constants module.
"""

NAME_MIN_LENGTH = 1
NAME_MAX_LENGTH = 30
PHONE_LENGTH = 10
PHONE_PATTERN = r"^\d{10}$"
DATE_FORMAT = "%d.%m.%Y"
DATE_STR_FORMAT = "DD.MM.YYYY"
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
ADDRESS_MIN_LENGTH = 5
ADDRESS_MAX_LENGTH = 100

validation_errors = {
    "invalid_name": (
        f"Name must consist of {NAME_MIN_LENGTH} "
        f"to {NAME_MAX_LENGTH} characters."
    ),
    "duplicate_name": "Name {} already exists.",
    "name_not_found": "Name {} not found.",
    "invalid_phone": f"Phone number must consist of {PHONE_LENGTH} digits.",
    "duplicate_phone": "Phone number {} already exists.",
    "phone_not_found": "Phone number {} not found.",
    "invalid_birthday": f"Invalid date format. Use {DATE_STR_FORMAT}.",
    "future_birthday": "Birthday cannot be in the future.",
    "invalid_email": "Invalid email address.",
    "invalid_address": (
        f"Address must consist of {ADDRESS_MIN_LENGTH} "
        f"to {ADDRESS_MAX_LENGTH} characters."
    ),
    "duplicate_title": "Title {} already exists.",
    "invalid_number": "Please enter a valid number.",
}
