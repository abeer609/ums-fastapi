import gzip
import os
from validators.exceptions import ValidationError


class MinimumLengthValidator:
    """
    Validate whether the password is of a minimum length.
    """

    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password: str) -> None:
        if len(password) < self.min_length:
            raise ValidationError(
                f"This password is too short. It must contain at least {self.min_length} character.",
            )


class CommonPasswordValidator:
    """
    Validate whether the password is a common password.

    The password is rejected if it occurs in a provided list, which may be gzipped.
    The list contains 1000 common passwords, created by Mark Burnett:
    https://xato.net/passwords/more-top-worst-passwords/
    """

    DEFAULT_PASSWORD_LIST_PATH = os.path.join("validators", "common-passwords.txt.gz")

    def __init__(self, password_list_path=DEFAULT_PASSWORD_LIST_PATH):
        try:
            with gzip.open(password_list_path) as f:
                common_passwords_lines = f.read().decode().splitlines()
        except IOError:
            with open(password_list_path) as f:
                common_passwords_lines = f.readlines()

        self.passwords = {p.strip() for p in common_passwords_lines}

    def validate(self, password: str) -> None:
        if password.lower().strip() in self.passwords:
            raise ValidationError("This password is too common.")


class NumericPasswordValidator:
    """
    Validate whether the password is alphanumeric.
    """

    def validate(self, password: str) -> None:
        if password.isdigit():
            raise ValidationError("This password is entirely numeric.")


def validate_password(password: str) -> None:
    default_validators = [
        MinimumLengthValidator(),
        CommonPasswordValidator(),
        NumericPasswordValidator(),
    ]

    errors = []
    for validator in default_validators:
        try:
            validator.validate(password)
        except ValidationError as err:
            errors.append(err.detail)

    if errors:
        raise ValidationError(errors)
