"""
Generate data module.
"""

from random import randint, random, choice, choices
from datetime import datetime, timedelta
from faker import Faker


def generate_random_contact() -> dict:
    """
    Generates a dictionary of random contact data.

    Returns:
        dict: A dictionary containing random contact data, including name,
        phones, birthday, email, and address.
    """
    fake = Faker()

    data = {
        "name": choice([fake.name(), fake.first_name()]),
        "phones": (
            ["".join(choices("0123456789", k=10)) for _ in range(randint(0, 4))]
        ),
        "birthday": (
            fake.date_of_birth().strftime("%d.%m.%Y") if random() < 0.7 else ""
        ),
        "email": (fake.email() if random() < 0.7 else ""),
        "address": (
            f"{fake.street_address()}, {fake.city()}, {fake.state()}"
            if random() < 0.7
            else ""
        ),
    }

    return data


def generate_random_note() -> dict:
    """
    Generates a dictionary of random note data.

    Returns:
        dict: A dictionary containing random note data, including title,
        text, tags, and reminder.
    """
    fake = Faker()

    data = {
        "title": " ".join(
            choices(fake.words(), k=randint(2, min(5, len(fake.words()))))
        ),
        "text": (fake.text(max_nb_chars=randint(4, 200)) if random() >= 0.3 else ""),
        "tags": [fake.word() for _ in range(randint(0, 5))],
        "reminder": generate_future_date() if random() >= 0.3 else "",
    }

    return data


def generate_future_date():
    """
    Generates a random future date within a specified range.

    Returns:
        str: A string representing the future date in the format DD.MM.YYYY.
    """
    start_date = datetime.today()
    random_days = randint(1, 30)
    return (start_date + timedelta(days=random_days)).strftime("%d.%m.%Y")
