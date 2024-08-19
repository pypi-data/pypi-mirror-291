import questionary

from pirate_ledger import CrewRoster


def ask_contact_name(book: CrewRoster) -> str:
    return questionary.autocomplete('Enter a contact name:', choices=[*book.keys()]).ask()
