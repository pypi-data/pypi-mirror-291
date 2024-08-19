import questionary
from colorama import Fore, Style

from pirate_ledger import cli
from pirate_ledger.helpers import input_error, NotesError
from pirate_ledger.sea_notes.note import NoteRecord
from pirate_ledger.sea_notes.sea_notes import SeaNotes
from pirate_ledger.sea_notes.search_options import SearchBy, SortBy, SortOrder

@input_error
def add_note(notes_list: SeaNotes):
    while True:
        title = questionary.text(
            "Arrr, what be the title of yer new note?",
            validate=cli.validators.RequiredValidator
        ).ask()

        if notes_list.find(title):
            print(Fore.RED + f"Avast! A note with the title '{title}' already exists. Choose a different title, matey." + Style.RESET_ALL)
        else:
            break

    content = questionary.text(
        "What be the content of yer note?",
        validate=cli.validators.RequiredValidator
    ).ask()

    record = NoteRecord(title, content)
    notes_list.add_record(record)

    return Fore.GREEN + f"Note titled '{title}' added to the ship's log."  + Style.RESET_ALL


@input_error
def delete_note(notes_list: SeaNotes):
    if notes_list.is_empty():
        raise NotesError(Fore.RED + "No notes found." + Style.RESET_ALL)

    title = questionary.autocomplete(
        "What be the title of the note ye wish to delete?",
        choices=[*notes_list.keys()],
        validate=cli.validators.RequiredValidator
    ).ask()

    record = notes_list.find(title)

    if not record:
        return NotesError(Fore.RED + f"Note titled '{title}' not found in the ship's log." + Style.RESET_ALL)

    notes_list.delete(title)
    return Fore.RED + f"Note titled '{title}' has been cast into the deep sea." + Style.RESET_ALL


@input_error
def update_note(notes_list: SeaNotes):
    if notes_list.is_empty():
        raise NotesError(Fore.RED + "Arrr, no notes be found in the captain's log!" + Style.RESET_ALL)

    title = questionary.autocomplete(
        "What be the title of the note ye wish to update?",
        choices=[*notes_list.keys()],
        validate=cli.validators.RequiredValidator
    ).ask()
    record = notes_list.find(title)

    if not record:
        return NotesError(Fore.RED + f"Note titled '{title}' not found in the ship's log." + Style.RESET_ALL)

    new_title = questionary.text(
        f"Enter the new title (current: {record.note.title}):",
        default=record.note.title,
        validate=cli.validators.RequiredValidator
    ).ask()

    new_content = questionary.text(
        f"Enter the new content (current: {record.note.content}):",
        default=record.note.content,
        validate=cli.validators.RequiredValidator
    ).ask()

    record.note.edit(new_title, new_content)

    return Fore.GREEN + f"Note titled '{title}' has been updated in the ship's log." + Style.RESET_ALL


@input_error
def search_notes(notes_list: SeaNotes):
    if notes_list.is_empty():
        raise NotesError(Fore.RED + "Arrr, no notes be found in the captain's log!" + Style.RESET_ALL)

    search_by = questionary.select(
        "Please specify a search type:",
        choices=[search.value for search in SearchBy],
    ).ask()

    if search_by == SearchBy.TITLE.value:
        query = questionary.autocomplete(
            "Please enter the note title:",
            choices=[*notes_list.keys()],
            validate=cli.validators.RequiredValidator
        ).ask()

        return notes_list.list_notes(query)
    else:
        query = questionary.text(
            "Please enter the tag name:",
            validate=cli.validators.RequiredValidator
        ).ask()

        return notes_list.list_notes(query, by_tags=True)


@input_error
def show_notes(notes_list: SeaNotes):
    if notes_list.is_empty():
        raise NotesError(Fore.RED + "Arrr, no notes be found in the captain's log!" + Style.RESET_ALL)

    return notes_list.list_notes()

@input_error
def sort_notes(notes_list: SeaNotes):
    if notes_list.is_empty():
        raise NotesError(Fore.RED + "Arrr, no notes be found in the captain's log!" + Style.RESET_ALL)

    sort_by = questionary.select(
        "Please specify a sort type:",
        choices=[sort.value for sort in SortBy],
    ).ask()

    sort_order = None

    if sort_by is not SortBy.TAGS.value:
        sort_order = questionary.select(
            "Please specify a sort order:",
            choices=[sort.value for sort in SortOrder],
        ).ask()

    return notes_list.sort_notes(sort_by, sort_order)

@input_error
def add_tag(notes_list: SeaNotes):
    if notes_list.is_empty():
        raise NotesError(Fore.RED + "Arrr, no notes be found in the captain's log!" + Style.RESET_ALL)

    title = questionary.autocomplete(
        "Please enter the note title:",
        choices=[*notes_list.keys()],
        validate=cli.validators.RequiredValidator
    ).ask()

    record = notes_list.find(title)

    if not record:
        raise NotesError(Fore.RED + f"Note titled '{title}' not found." + Style.RESET_ALL)

    while True:
        new_tag = questionary.text(
            f"Enter a new tag:",
            validate=cli.validators.RequiredValidator
        ).ask()

        if record.has_tag(new_tag):
            print(Fore.RED + f"A tag '{new_tag}' already exists. Please choose a different tag." + Style.RESET_ALL)
        else:
            break

    record.add_tag(new_tag)

    return Fore.GREEN + f"Tag '{new_tag}' was added to '{title}' note." + Style.RESET_ALL

