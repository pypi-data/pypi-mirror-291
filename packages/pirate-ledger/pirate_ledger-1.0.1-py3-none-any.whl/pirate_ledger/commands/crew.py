import questionary
from tabulate import tabulate
from colorama import Fore, Style, init

from pirate_ledger import cli
from pirate_ledger.crew_roster.crew_roster import CrewRoster, CrewMember
from pirate_ledger.helpers import ContactsError, input_error

init()

@input_error
def add_crew_member(crew_rooster: CrewRoster):
    name = questionary.text(
        "Arrr, enter the name of the scallywag:",
        validate=cli.validators.RequiredValidator
    ).ask()
    message = Fore.LIGHTGREEN_EX + "New mate added to the crew." + Style.RESET_ALL

    contact = crew_rooster.find(name)
    if contact:
        if questionary.confirm('This pirate already sails with us! Do ye wish to update their details?').ask():
            message = Fore.LIGHTGREEN_EX + "Details of the crew member have been updated." + Style.RESET_ALL
        else:
            return Fore.LIGHTRED_EX + 'Aborting the addition of the crew member.' + Style.RESET_ALL

    contact = contact or CrewMember(name)
    crew_rooster.add_record(contact)
    form = questionary.form(
        address=questionary.text("[Optional] Where does this buccaneer call home?"),
        phone=questionary.text("[Optional] How can we reach this pirate? (Phone number)", validate=cli.validators.PhoneValidator),
        email=questionary.text("[Optional] Where do the seabirds deliver messages? (email)", validate=cli.validators.EmailValidator),
        birthday=questionary.text("[Optional] When did this pirate first see the sea? (birthday in DD.MM.YYYY)", validate=cli.validators.DateValidator),
    )
    fields = form.ask()

    for field, value in fields.items():
        if value:
            setattr(contact, field, value)

    return message


@input_error
def update_crew_member(crew_rooster: CrewRoster) -> str:
    name = cli.prompts.ask_contact_name(crew_rooster)
    record = crew_rooster.find(name)
    if record is None:
        raise ContactsError(Fore.RED + "This pirate doesn't sail with us!" + Style.RESET_ALL)

    field = questionary.autocomplete('What detail do ye wish to update, matey?', choices=CrewMember.get_fields()).ask()
    if hasattr(record, field):
        new_value = questionary.text(f"Enter the new value for {field}:",
                                     validate=cli.validators.RequiredValidator).ask()
        setattr(record, field, new_value)

        return Fore.GREEN + f"{field.capitalize()} has been updated for this salty sea dog." + Style.RESET_ALL
    else:
        raise ContactsError(Fore.RED + f"Field '{field}' doesn't exist on this pirate's record." + Style.RESET_ALL)


@input_error
def delete_crew_member(crew_rooster: CrewRoster) -> str:
    name = cli.prompts.ask_contact_name(crew_rooster)
    record = crew_rooster.find(name)

    if record is None:
        raise ContactsError(Fore.RED + "This pirate doesn't sail with us!" + Style.RESET_ALL)

    crew_rooster.delete(name)

    return Fore.GREEN + f"{name} walks the plank! This crew member has been removed from the roster." + Style.RESET_ALL


@input_error
def show_crew_member(crew_rooster: CrewRoster) -> str:
    name = questionary.autocomplete('Enter the name of the pirate ye wish to see:', choices=[*crew_rooster.keys()]).ask()
    contact = crew_rooster.find(name)

    if contact is None:
       raise ContactsError(Fore.RED + f"Arrr, it seems {name} has recently walked the plank and is no longer on the roster!" + Style.RESET_ALL)

    return str(contact)


@input_error
def all_crew_members(crew_rooster: CrewRoster) -> str:
    if not crew_rooster:
        raise ContactsError(Fore.RED + "Arrr, the crew roster be empty! Not a single pirate aboard!" + Style.RESET_ALL)

    table_data = []
    command_output = Fore.CYAN + "Here be the list of all the scallywags aboard:\n" + Style.RESET_ALL

    for name, contact in crew_rooster.items():
        name = Fore.LIGHTBLUE_EX + name + Style.RESET_ALL
        address = contact.address
        if address is None:
            address = Fore.RED + "Homeless" + Style.RESET_ALL
        else:
            address = Fore.GREEN + address + Style.RESET_ALL
        email = contact.email
        if email is None:
            email = Fore.RED + "No email" + Style.RESET_ALL
        else:
            email = Fore.GREEN + email + Style.RESET_ALL
        phone = contact.phone
        if phone is None:
            phone = Fore.RED + "No phone" + Style.RESET_ALL
        else:
            phone = Fore.GREEN + phone + Style.RESET_ALL
        birthday = contact.birthday
        if birthday is None:
            birthday = Fore.RED + "Unborn" + Style.RESET_ALL
        else:
            birthday = Fore.GREEN + birthday.strftime("%d/%m/%Y") + Style.RESET_ALL
        table_data.append([name, phone, email, address, birthday])
        headers = [Fore.LIGHTYELLOW_EX + "Pirate Name" + Style.RESET_ALL, 
                   Fore.LIGHTYELLOW_EX + "Phone" + Style.RESET_ALL,
                   Fore.LIGHTYELLOW_EX + "Email" + Style.RESET_ALL, 
                   Fore.LIGHTYELLOW_EX + "Address" + Style.RESET_ALL,
                   Fore.LIGHTYELLOW_EX + "Birthday" + Style.RESET_ALL]
        command_output = tabulate(table_data, headers=headers, tablefmt="grid")

    return command_output

@input_error
def crew_birthdays(crew_rooster: CrewRoster) -> str:


    if not crew_rooster:
        raise ContactsError(Fore.RED + "Arrr, the crew roster be empty! Not a single pirate aboard!" + Style.RESET_ALL)

    try:
        delta_days = int(questionary.text(
            "How many days ahead do ye wish to check for upcoming birthdays?",
            validate=cli.validators.NumberValidation
        ).ask())
        birthdays_list = crew_rooster.get_upcoming_birthdays(delta_days)

        if not birthdays_list:
            return Fore.RED + f"No pirate birthdays for the next {delta_days} days." + Style.RESET_ALL

        table_data = []
        for contact in birthdays_list:
            name = Fore.LIGHTBLUE_EX + contact['name'] + Style.RESET_ALL
            congrats_date = Fore.GREEN + contact['congratulation_date'] + Style.RESET_ALL
            table_data.append([name, congrats_date])

        headers = [Fore.LIGHTYELLOW_EX + "Pirate Name" + Style.RESET_ALL, 
                   Fore.LIGHTYELLOW_EX + "Birthday" + Style.RESET_ALL]

        output = tabulate(table_data, headers=headers, tablefmt="grid")
        return output

    except ValueError:
        return Fore.RED + "Arrr, that's not a proper number! Please enter an integer, matey." + Style.RESET_ALL


@input_error
def search_crew_member(crew_rooster: CrewRoster) -> str:
    if not crew_rooster:
        raise ContactsError(Fore.RED + "Arrr, the crew roster be empty! Not a single pirate aboard!" + Style.RESET_ALL)

    search_input = questionary.text(
       "What be ye searching for among the crew, matey?",
        validate=cli.validators.RequiredValidator
    ).ask()

    return crew_rooster.search_crew_members(search_input)