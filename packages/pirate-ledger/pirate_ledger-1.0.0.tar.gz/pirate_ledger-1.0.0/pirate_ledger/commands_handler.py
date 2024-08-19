from enum import Enum
from colorama import Fore, Style

from .commands import *

class Commands(Enum):
    EXIT = "exit"
    HELP = "help"
    CLOSE = "close"
    HELLO = "hello"

    ADD_CREW_MEMBER = "crew:add"
    SHOW_CREW_MEMBER = "crew:show"
    ALL_CREW_MEMBERS = "crew:all"
    BIRTHDAYS = "crew:birthdays"
    UPDATE_CREW_MEMBER = "crew:update"
    DELETE_CREW_MEMBER = "crew:delete"
    SEARCH_CREW_MEBERS = 'crew:search'

    ADD_NOTE = 'note:add'
    DELETE_NOTE = 'note:delete'
    UPDATE_NOTE = 'note:update'
    ALL_NOTES = 'note:all'
    SEARCH_NOTES = 'note:search'
    ADD_NOTE_TAG = "note:add:tag"
    SORT_NOTE = "note:sort"

    def __eq__(self, value: object) -> bool:
        return self.value == value
    

def listen_commands(book: CrewRoster, notes: SeaNotes, on_exit: callable):
    try:
        print(Fore.CYAN + "Ahoy, matey! Welcome aboard the Pirate Ledger!" + Style.RESET_ALL)
        commands = [e.value for e in Commands]
        while True:
            command = questionary.autocomplete(
                "What be yer command, captain?", choices=commands).ask()

            if command in (Commands.EXIT, Commands.CLOSE):
                on_exit(book, notes)
                print(Fore.CYAN + "Fair winds and following seas! Farewell!" + Style.RESET_ALL)
                break

            elif command == Commands.HELLO:
                print(Fore.CYAN + "What be yer orders, captain?" + Style.RESET_ALL)

            elif command == Commands.HELP:
                print("\n- ".join([Fore.CYAN + "Here be the commands ye can give:" + Style.RESET_ALL, *commands]))

            elif command == Commands.ADD_CREW_MEMBER:
                print(add_crew_member(book))

            elif command == Commands.SHOW_CREW_MEMBER:
                print(show_crew_member(book))

            elif command == Commands.ALL_CREW_MEMBERS:
                print(all_crew_members(book))

            elif command == Commands.BIRTHDAYS:
                print(crew_birthdays(book))

            elif command == Commands.UPDATE_CREW_MEMBER:
                print(update_crew_member(book))

            elif command == Commands.DELETE_CREW_MEMBER:
                print(delete_crew_member(book))

            elif command == Commands.SEARCH_CREW_MEBERS:
                print(search_crew_member(book))

            elif command == Commands.ADD_NOTE:
                print(add_note(notes))

            elif command == Commands.UPDATE_NOTE:
                print(update_note(notes))

            elif command == Commands.DELETE_NOTE:
                print(delete_note(notes))

            elif command == Commands.ALL_NOTES:
                print(show_notes(notes))

            elif command == Commands.SEARCH_NOTES:
                print(search_notes(notes))

            elif command == Commands.SORT_NOTE:
                print(sort_notes(notes))

            elif command == Commands.ADD_NOTE_TAG:
                print(add_tag(notes))

            else:
                print(Fore.RED + "Arrr, that be an invalid command, matey! Try again." + Style.RESET_ALL)
    except KeyboardInterrupt:
        on_exit(book, notes)
