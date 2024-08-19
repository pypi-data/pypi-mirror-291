from prompt_toolkit.document import Document
from questionary import Validator, ValidationError

from pirate_ledger.crew_roster.crew_roster import Phone, Email, Birthday


class RequiredValidator(Validator):
    def validate(self, document: Document):
        if not document.text.strip():
            raise ValidationError(
                message="Please enter a value",
                cursor_position=len(document.text),
            )

class NumberValidation(Validator):
    def validate(self, document: Document):
        if not document.text.isnumeric():
            raise ValidationError(
                message="Arrr, that's not a proper number! Please enter an integer, matey.",
                cursor_position=len(document.text),
            )

class PhoneValidator(Validator):
    def validate(self, document: Document):
        if document.text and not Phone.is_valid(document.text):
            raise ValidationError(
                message="Please enter a 10-digit phone number",
                cursor_position=len(document.text),
            )

class EmailValidator(Validator):
    def validate(self, document: Document):
        if document.text and not Email.is_valid(document.text):
            raise ValidationError(
                message="Please enter a valid email, e.g. example@example.com",
                cursor_position=len(document.text)
            )

class DateValidator(Validator):
    def validate(self, document: Document):
        if document.text and not Birthday.is_valid(document.text):
            raise ValidationError(
                message="Please enter a valid date in DD.MM.YY format, and it cannot be in the future",
                cursor_position=len(document.text)
            )
