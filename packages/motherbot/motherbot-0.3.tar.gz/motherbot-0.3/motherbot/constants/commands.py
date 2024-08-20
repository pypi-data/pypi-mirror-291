"""
Commands constants module.
"""

command_names_en = {
    "help": "help",
    "settings": "settings",
    "add_contact": "add-contact",
    "change_contact": "change-contact",
    "main_menu": "main-menu",
    "add_phones": "add-phones",
    "remove_phone": "remove-phone",
    "add_birthday": "add-birthday",
    "remove_birthday": "remove-birthday",
    "edit_birthday": "edit-birthday",
    "add_address": "add-address",
    "remove_address": "remove-address",
    "edit_address": "edit-address",
    "add_email": "add-email",
    "remove_email": "remove-email",
    "edit_email": "edit-email",
    "delete_contact": "delete-contact",
    "all_contacts": "all-contacts",
    "birthdays": "birthdays",
    "search_contacts": "search-contacts",
    "fake_contacts": "fake-contacts",
    "smart_search": "smart-search",
    "add_note": "add-note",
    "change_note": "change-note",
    "add_tags": "add-tags",
    "remove_tag": "remove-tag",
    "add_text": "add-text",
    "remove_text": "remove-text",
    "edit_text": "edit-text",
    "add_reminder": "add-reminder",
    "remove_reminder": "remove-reminder",
    "edit_reminder": "edit-reminder",
    "delete_note": "delete-note",
    "all_notes": "all-notes",
    "reminders": "reminders",
    "search_notes": "search-notes",
    "fake_notes": "fake-notes",
    "close": "close",
    "exit": "exit",
}

command_descriptions_en = {
    "help": {
        "description": "Shows this help message.",
        "subcommands": {}
    },
    "settings": {
        "description": ("Opens the settings menu to change language or date "
                        "format."),
        "subcommands": {}
    },
    "add_contact": {
        "description": ("Starts the process of adding a new contact. "
                        "Will ask for name, phones, birthday, email, and "
                        "address."),
        "subcommands": {}
    },
    "change_contact": {
        "description": "Opens a submenu with commands to change a contact:",
        "subcommands": {
            "main_menu": "Returns to the main menu.",
            "add_phones": "Adds a new phones.",
            "remove_phone": "Removes phone",
            "add_birthday": "Adds a birthday.",
            "remove_birthday": "Removes the birthday.",
            "edit_birthday": "Edits the birthday.",
            "add_address": "Adds an address.",
            "remove_address": "Removes the address.",
            "edit_address": "Edits the address.",
            "add_email": "Adds an email address.",
            "remove_email": "Removes the email address.",
            "edit_email": "Edits the email address.",
        }
    },
    "delete_contact": {
        "description": "Deletes a contact by name.",
        "subcommands": {}
    },
    "all_contacts": {
        "description": "Shows all contacts with their phone numbers.",
        "subcommands": {}
    },
    "birthdays": {
        "description": ("Shows upcoming birthdays within the specified number"
                        " of days."),
        "subcommands": {}
    },
    "search_contacts": {
        "description": ("Allows you to search for contacts by name or phone"
                        " number."),
        "subcommands": {}
    },
    "fake_contacts": {
        "description": ("Generates a specified number of fake contacts and "
                        "adds them to an address book."),
        "subcommands": {}
    },
    "add_note": {
        "description": ("Starts the process of adding a new note to the "
                        "notebook. Will ask for text, tag(s), reminder."),
        "subcommands": {}
    },
    "change_note": {
        "description": ("Opens a submenu with commands to change the note: "
                        "edit-text, add-tags, remove-tag, add-reminder."),
        "subcommands": {
            "main_menu": "Returns to the main menu.",
            "add_tags": "Adds a tags.",
            "remove_tag": "Removes the tag.",
            "add_text": "Adds text.",
            "remove_text": "Removes the text.",
            "edit_text": "Edits the text.",
            "add_reminder": "Adds a reminder.",
            "remove_reminder": "Removes the reminder.",
            "edit_reminder": "Edits the reminder.",
        }
    },
    "delete_note": {
        "description": "Deletes a note from the notebook by title.",
        "subcommands": {}
    },
    "all_notes": {
        "description": "Shows all notes in the notebook.",
        "subcommands": {}
    },
    "reminders": {
        "description": "Shows reminders within the specified number of days.",
        "subcommands": {}
    },
    "search_notes": {
        "description": "Allows you to search for notes by title or tag.",
        "subcommands": {}
    },
    "fake_notes": {
        "description": ("Generates a specified number of fake notes and "
                        "adds them to the notebook."),
        "subcommands": {}
    },
    "close": {
        "description": "Exits the program.",
        "subcommands": {}
    },
    "exit": {
        "description": "Exits the program.",
        "subcommands": {}
    },
}

command_names_ua = {
    "help": "довідка",
    "settings": "налаштування",
    "add_contact": "додати-контакт",
    "change_contact": "редагувати-контакт",
    "main_menu": "головне-меню",
    "add_phones": "додати-телефон",
    "remove_phone": "видалити-телефон",
    "add_birthday": "додати-день-народження",
    "remove_birthday": "видалити-день-народження",
    "edit_birthday": "редагувати-день-народження",
    "add_address": "додати-адресу",
    "remove_address": "видалити-адресу",
    "edit_address": "редагувати-адресу",
    "add_email": "додати-електронну-пошту",
    "remove_email": "видалити-електронну-пошту",
    "edit_email": "редагувати-електронну-пошту",
    "delete_contact": "видалити-контакт",
    "all_contacts": "всі-контакти",
    "birthdays": "дні-народження",
    "search_contacts": "пошук-контактів",
    "fake_contacts": "генерувати-контакти",
    "add_note": "додати-нотатку",
    "change_note": "редагувати-нотатку",
    "add_tags": "додати-теги",
    "remove_tag": "видалити-тег",
    "add_text": "додати-текст",
    "remove_text": "видалити-текст",
    "edit_text": "редагувати-текст",
    "add_reminder": "додати-нагадування",
    "remove_reminder": "видалити-нагадування",
    "edit_reminder": "редагувати-нагадування",
    "delete_note": "видалити-нотатку",
    "all_notes": "всі-нотатки",
    "reminders": "нагадування",
    "search_notes": "пошук-нотаток",
    "fake_notes": "генерувати-нотатки",
    "close": "закрити",
    "exit": "вихід",
}

command_descriptions_ua = {
    "help": {
        "description": "Відкривати цю довідку.",
        "subcommands": {}
    },
    "settings": {
        "description": ("Відкрити меню налаштувань для зміни мови або формату "
                        "дати."),
        "subcommands": {}
    },
    "add_contact": {
        "description": ("Почати процес додавання нового контакту. Буде "
                        "запитано ім'я, телефон, день народження, електронну "
                        "пошту та адресу."),
        "subcommands": {}
    },
    "change_contact": {
        "description": "Відкрити діалог для редагування контакту за іменем:",
        "subcommands": {
            "main_menu": "Повернутися до головного меню.",
            "add_phones": "Додати телефон.",
            "remove_phone": "Видалити телефон.",
            "add_birthday": "Додати день народження.",
            "remove_birthday": "Видалити день народження.",
            "edit_birthday": "Редагувати день народження.",
            "add_address": "Додати адресу.",
            "remove_address": "Видалити адресу.",
            "edit_address": "Редагувати адресу.",
            "add_email": "Додати електронну пошту.",
            "remove_email": "Видалити електронну пошту.",
            "edit_email": "Редагувати електронну пошту.",
        }
    },
    "delete_contact": {
        "description": "Видалити контакт за іменем.",
        "subcommands": {}
    },
    "all_contacts": {
        "description": "Показати всі контакти в адресній книзі.",
        "subcommands": {}
    },
    "birthdays": {
        "description": "Показати дні народження за вказаною кількістю днів.",
        "subcommands": {}
    },
    "search_contacts": {
        "description": "Пошук контакту за іменем чи номером телефону.",
        "subcommands": {}
    },
    "fake_contacts": {
        "description": ("Генерувати вказану кількість демо-контактів. Всі "
                        "контакти будуть додані в адресну книгу."),
        "subcommands": {}
    },
    "add_note": {
        "description": ("Почати процес додавання нової нотатки. Буде запитано "
                        "назву нотатки, текст, теги та нагадування."),
        "subcommands": {}
    },
    "change_note": {
        "description": "Відкрити діалог для редагування нотатки за назвою:",
        "subcommands": {
            "main_menu": "Повернутися до головного меню.",
            "add_tags": "Додати теги.",
            "remove_tag": "Видалити тег.",
            "add_text": "Додати текст.",
            "remove_text": "Видалити текст.",
            "edit_text": "Редагувати текст.",
            "add_reminder": "Додати нагадування.",
            "remove_reminder": "Видалити нагадування.",
            "edit_reminder": "Редагувати нагадування.",
        }
    },
    "delete_note": {
        "description": "Видалити нотатку за назвою.",
        "subcommands": {}
    },
    "all_notes": {
        "description": "Показати всі нотатки в книзі.",
        "subcommands": {}
    },
    "reminders": {
        "description": "Показати нагадування за вказаною кількістю днів.",
        "subcommands": {}
    },
    "search_notes": {
        "description": "Пошук нотатки за назвою чи тегом.",
        "subcommands": {}
    },
    "fake_notes": {
        "description": ("Генерувати вказану кількість демо-нотаток. Всі "
                        "нотатки будуть додані в книгу."),
        "subcommands": {}
    },
    "close": {
        "description": "Закрити програму.",
        "subcommands": {}
    },
    "exit": {
        "description": "Закрити програму.",
        "subcommands": {}
    },
}
