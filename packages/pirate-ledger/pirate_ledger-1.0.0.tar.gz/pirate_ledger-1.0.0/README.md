# Pirate Ledger

Arrr, welcome to **Pirate Ledger** - the captain's logbook for managing your crew and sea notes!

## Introduction

**Pirate Ledger** is a Python module designed to keep track of your pirate crew members and their details, along with any sea notes that you might need to jot down during your adventures on the high seas.

## Features

- **Crew Roster**: Manage your crew members, including adding, updating, and deleting records.
- **Sea Notes**: Keep detailed notes with easy searching capabilities.
- **Pirate-themed Experience**: Enjoy a fully immersive pirate experience while managing your records.


## Development 
 Start local - python -m pirate_ledger.main


To work on the Pirate Ledger and push new versions to PyPI, follow these steps:
1. **Update the Version**
   Before pushing a new version, ensure you update the version number in the `setup.py` file. This is crucial for PyPI to recognize the new version. For example:

   version='1.0.1'

2. **New build**
    python setup.py sdist bdist_wheel
3. **Upload to PyPI**
    pip install twine
    twine upload dist/*



## Commands
Inside the assistant bot, you can use the following commands:

- `crew:add` - Add a new crew member.
- `crew:show` - Show a specific crew member's details.
- `crew:all` - Display all crew members.
- `crew:birthdays` - Show upcoming birthdays of crew members.
- `crew:update` - Update a crew member's details.
- `crew:delete` - Walk the plank (delete) a crew member.
- `crew:search` - Search for crew members by name or details.
- `note:add` - Add a new sea note.
- `note:delete` - Delete a sea note.
- `note:update` - Update a sea note.
- `note:all` - Show all sea notes.
- `note:search` - Search for sea notes by title or content.


## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Installation
To install the Pirate Ledger module, use the following command:

```bash
pip install pirate-ledger


