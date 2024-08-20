"""
Validation constants module.
"""

from .values import (
    NAME_MIN_LENGTH,
    NAME_MAX_LENGTH,
    PHONE_LENGTH,
    ADDRESS_MIN_LENGTH,
    ADDRESS_MAX_LENGTH,
    TITLE_MIN_LENGTH,
    TITLE_MAX_LENGTH,
    TAG_MIN_LENGTH,
    TAG_MAX_LENGTH,
    TEXT_MAX_LENGTH,
)

validation_errors_en = {
    "invalid_name": (
        f"Name must consist of {NAME_MIN_LENGTH} "
        f"to {NAME_MAX_LENGTH} characters."
    ),
    "duplicate_name": "Name \"{}\" already exists.",
    "name_not_found": "Name \"{}\" not found.",
    "invalid_phone": f"Phone number must consist of {PHONE_LENGTH} digits.",
    "duplicate_phone": "Phone number \"{}\" already exists.",
    "phone_not_found": "Phone number \"{}\" not found.",
    "future_birthday": "Birthday cannot be in the future.",
    "invalid_email": "Invalid email address.",
    "invalid_address": (
        f"Address must consist of {ADDRESS_MIN_LENGTH} "
        f"to {ADDRESS_MAX_LENGTH} characters."
    ),
    "invalid_title": (
        f"Title must consist of {TITLE_MIN_LENGTH} "
        f"to {TITLE_MAX_LENGTH} characters."
    ),
    "duplicate_title": "Title \"{}\" already exists.",
    "title_not_found": "Title \"{}\" not found.",
    "invalid_tag": (
        f"Tag must consist of {TAG_MIN_LENGTH} "
        f"to {TAG_MAX_LENGTH} characters."
    ),
    "tag_not_found": "Tag \"{}\" not found.",
    "invalid_text": f"Text must consist of 1 to {TEXT_MAX_LENGTH} characters.",
    "invalid_reminder": "Reminder date must be in the future.",
    "invalid_date": "Invalid date format. Use {}.",
    "invalid_number": "Please enter a valid number.",
    "invalid_language": "Language must be one of: {}",
    "invalid_date_format": "Date format must be one of: {}",
}

validation_errors_ua = {
    "invalid_name": (f"Ім'я має складатися з {NAME_MIN_LENGTH} до "
                     f"{NAME_MAX_LENGTH} символів."),
    "duplicate_name": "Ім'я \"{}\" вже існує.",
    "name_not_found": "Ім'я \"{}\" не знайдено.",
    "invalid_phone": f"Номер телефону має складатися з {PHONE_LENGTH} цифр.",
    "duplicate_phone": "Номер телефону \"{}\" вже існує.",
    "phone_not_found": "Номер телефону \"{}\" не знайдено.",
    "future_birthday": "День народження не може бути в майбутньому.",
    "invalid_email": "Невірна адреса електронної пошти.",
    "invalid_address": (
        f"Адреса має складатися з {ADDRESS_MIN_LENGTH} до "
        f"{ADDRESS_MAX_LENGTH} символів."
    ),
    "invalid_title": (
        f"Назва має складатися з {TITLE_MIN_LENGTH} до"
        f"{TITLE_MAX_LENGTH} символів."
    ),
    "duplicate_title": "Назва \"{}\" вже існує.",
    "title_not_found": "Назву \"{}\" не знайдено.",
    "invalid_tag": (
        f"Тег має складатися з {TAG_MIN_LENGTH} до "
        f"{TAG_MAX_LENGTH} символів."
    ),
    "tag_not_found": "Тег \"{}\" не знайдено.",
    "invalid_text": f"Текст має складатися з 1 до {TEXT_MAX_LENGTH} символів.",
    "invalid_reminder": "Дата нагадування має бути в майбутньому.",
    "invalid_date": "Невірний формат дати. Використовуйте {}.",
    "invalid_number": "Будь ласка, введіть ціле число.",
}
