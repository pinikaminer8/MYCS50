import string
from datetime import datetime

"""
This file handles Exceptions and validates all program variables
"""

class NameContainsIllegalCharacter(Exception):
    def __init__(self, letter, index):
        self._letter = letter
        self._index = index

    def __str__(self):
        return f"The name contains an illegal character {self._letter} at index {self._index}"


class NameTooShort(Exception):
    def __str__(self):
        return f"Name is too short"


class NameTooLong(Exception):
    def __str__(self):
        return f"Name is too long"


class PasswordMissingCharacter(Exception):
    def __str__(self):
        return f"Password is missing a Character"


class PasswordMissingUppercase(PasswordMissingCharacter):
    def __str__(self):
        return super().__str__() + " (Uppercase)"


class PasswordMissingLowercase(PasswordMissingCharacter):
    def __str__(self):
        return super().__str__() + " (Lowercase)"


class PasswordMissingDigit(PasswordMissingCharacter):
    def __str__(self):
        return super().__str__() + " (Digit)"


class PasswordMissingSpecial(PasswordMissingCharacter):
    def __str__(self):
        return super().__str__() + " (Special)"


class PasswordTooShort(Exception):
    def __str__(self):
        return f"password is too short"


class PasswordTooLong(Exception):
    def __str__(self):
        return f"password is too long"


class EmailTooShort(Exception):
    def __str__(self):
        return f"email is too short"


class EmailTooLong(Exception):
    def __str__(self):
        return f"Email is too long"


class EmailMissingCharacter(Exception):
    def __str__(self):
        return f"Email is missing a vital char"


class EmailIsNotValid(Exception):
    def __str__(self):
        return f"This Email address is not valid"


class PhoneNumTooShort(Exception):
    def __str__(self):
        return f"Phone number is too short"


class PhoneNumTooLong(Exception):
    def __str__(self):
        return f"Phone number is too long"


class PhoneNumNotDigits(Exception):
    def __str__(self):
        return f"Phone number must contain digits only"


class PassportLengthWrong(Exception):
    def __str__(self):
        return f"Passport should contain exactly 9 characters"


class PassportUpperCaseOrDigits(Exception):
    def __str__(self):
        return f"Passport should contain uppercase letters and digits only"


class DateNoDigits(Exception):
    def __str__(self):
        return f"Date must contain digits and '/' only "


class WrongDateFormat(Exception):
    def __str__(self):
        return f"Date format must be yyyy/mm/dd"


class DateMonthInvalid(Exception):
    def __str__(self):
        return f"Date month must be between 1-12"


class DateDayInvalid(Exception):
    def __str__(self):
        return f"Date day must be between 1-31"


class DateBeforeCurrnet(Exception):
    def __str__(self):
        return f"Date typed is before current day"


class DateAfterCurrnet(Exception):
    def __str__(self):
        return f"Date typed is after current day"


class NumNotInt(Exception):
    def __str__(self):
        return f"number of travelers is invalid"


class NumNotPositive(Exception):
    def __str__(self):
        return f"num of travelers must be positive"


class NumOutOfRange(Exception):
    def __str__(self):
        return f"Chosen number is out of range"


class CcWrongLength(Exception):
    def __str__(self):
        return f"Credit Card length inserted is wrong"


class CcNumInvalid(Exception):
    def __str__(self):
        return f"Sorry, Credit Card number is invalid"


class CvvInvalid(Exception):
    def __str__(self):
        return f"cvv is invalid"


class CcWrongDate(Exception):
    def __str__(self):
        return f"Credit Card date invalid"


def validate_name(name):
    try:
        for i in range(len(name)):
            if not name[i].isalpha() and not name[i].isdigit() and name[i] != '_':
                raise NameContainsIllegalCharacter(name[i], i)
        if len(name) < 2:
            raise NameTooShort
        elif len(name) > 16:
            raise NameTooLong
        return True

    except NameContainsIllegalCharacter as a:
        print(a)

    except NameTooShort as b:
        print(b)

    except NameTooLong as c:
        print(c)


def validate_phone_num(phone_num):
    try:
        if not all(char.isdigit() for char in phone_num):
            raise PhoneNumNotDigits
        elif len(phone_num) < 8:
            raise PhoneNumTooShort
        elif len(phone_num) > 14:
            raise PhoneNumTooLong

        return True
    except PhoneNumTooShort as a:
        print(a)
    except PhoneNumTooLong as b:
        print(b)
    except PhoneNumNotDigits as c:
        print(c)


def validate_password(password):
    try:
        if len(password) < 8:
            raise PasswordTooShort
        elif len(password) > 20:
            raise PasswordTooLong
        elif not any(char.isupper() for char in password):
            raise PasswordMissingUppercase
        elif not any(char.islower() for char in password):
            raise PasswordMissingLowercase
        elif not any(char.isdigit() for char in password):
            raise PasswordMissingDigit
        elif not any(char in string.punctuation for char in password):
            raise PasswordMissingSpecial
        return True

    except PasswordMissingUppercase as d:
        print(d)

    except PasswordMissingLowercase as e:
        print(e)

    except PasswordMissingDigit as f:
        print(f)

    except PasswordMissingSpecial as g:
        print(g)

    except PasswordTooLong as h:
        print(h)

    except PasswordTooShort as i:
        print(i)


def validate_email(email):
    try:
        if len(email) < 4:
            raise EmailTooShort
        elif len(email) > 30:
            raise EmailTooLong
        elif '@' not in email or '.' not in email:
            raise EmailMissingCharacter
        elif email.startswith('@') or email.endswith('@') or ' ' in email:
            raise EmailIsNotValid
        return True

    except EmailTooShort as a:
        print(a)
    except EmailTooLong as b:
        print(b)
    except EmailMissingCharacter as c:
        print(c)
    except EmailIsNotValid as d:
        print(d)


def validate_passport(passport):
    try:
        if len(passport) != 9:
            raise PassportLengthWrong
        # Check if the passport number contains only uppercase letters and digits
        if not passport.isalnum():
            raise PassportUpperCaseOrDigits

    except PassportLengthWrong as a:
        print(a)
    except PassportUpperCaseOrDigits as b:
        print(b)
    return True


def validate_date_format(date_str):
    if len(date_str) != 10:
        return False

    if date_str[4] != '/' or date_str[7] != '/':
        return False

    for i in range(len(date_str)):
        if i in [4, 7]:
            continue

        if not date_str[i].isdigit():
            return False

    return True


def validate_date(date_str):
    # Check if all characters are numbers except for slashes
    try:
        if not date_str.replace('/', '').isdigit():
            raise DateNoDigits

        # Check if date is in the right format
        if not validate_date_format(date_str):
            raise WrongDateFormat

        # Convert
        date_month = int(date_str[5:7])
        # Check if month is not greater than 12
        if date_month > 12 or date_month < 1:
            raise DateMonthInvalid

        date_day = int(date_str[8:10])
        # Check if day is not greater than 31
        if date_day > 31 or date_day < 1:
            raise DateDayInvalid
        # All checks passed, date is valid
        return True

    except DateNoDigits as a:
        print(a)
    except WrongDateFormat as b:
        print(b)
    except DateMonthInvalid as c:
        print(c)
    except DateDayInvalid as d:
        print(d)


def validate_flight_date(date):
    if validate_date(date):
        # Get the current date
        current_date = datetime.now().date()
        date = datetime.strptime(date, "%Y/%m/%d").date()
        # Convert the input date string to a datetime object
        try:
            if date < current_date:
                raise DateBeforeCurrnet
            return True
        except DateBeforeCurrnet as a:
            print(a)


def validate_dob_date(date):
    if validate_date(date):
        # Get the current date
        current_date = datetime.now().date()
        try:
            date = datetime.strptime(date, "%Y/%m/%d").date()
            valid_day = True
        except ValueError:
            valid_day = False
            print("Invalid day")
        if valid_day:
            try:
                if date > current_date:
                    raise DateAfterCurrnet
                return True
            except DateAfterCurrnet as a:
                print(a)


def is_int(num):
    try:
        if not num.isdigit():
            raise NumNotInt
        elif int(num) == 0:
            raise NumNotPositive
        return True
    except NumNotInt as a:
        print(a)
    except NumNotPositive as b:
        print(b)


def validate_choice(num, list_len):
    if is_int(str(num)):
        try:
            if int(num) > list_len:
                raise NumOutOfRange
            return True
        except NumOutOfRange as a:
            print(a)


def validate_cc(cc_num):
    # Remove spaces and dashes from the card number
    card_number = cc_num.replace(' ', '').replace('-', '')
    if is_int(card_number):
        try:
            # Check the length of the card number
            if len(card_number) not in [13, 15, 16]:
                raise CcWrongLength
            # Multiply every other digit by 2, starting from the second-to-last digit
            digits = [int(digit) for digit in card_number]
            doubled_digits = [(2 * digit) if index % 2 == len(card_number) % 2 else digit for index, digit in
                              enumerate(digits)]
            # Sum up the digits, accounting for digits greater than 9
            summed_digits = [digit - 9 if digit > 9 else digit for digit in doubled_digits]
            # Calculate the total sum
            total_sum = sum(summed_digits)
            # Check if the total sum's last digit is 0
            if total_sum % 10 != 0:
                raise CcNumInvalid
            return True
        except CcWrongLength as a:
            print(a)
        except CcNumInvalid as b:
            print(b)


def validate_cc_date(cc_date):
    expiration_date = datetime.strptime(cc_date, '%m/%y')
    # Get the current date
    current_date = datetime.now()
    # Check if expiration_date is not in the past
    try:
        if expiration_date < current_date:
            raise CcWrongDate
        # Optionally, check if expiration_date is not too far in the future
        max_future_years = 10
        max_future_date = current_date.replace(year=current_date.year + max_future_years)
        if expiration_date > max_future_date:
            return CcWrongDate
        return True
    except CcWrongDate as a:
        print(a)


def validate_cvv(cvv, issuer):
    if is_int(cvv):
        try:
            if issuer == 'American Express':
                if len(cvv) != 4:
                    raise CvvInvalid
            else:
                if len(cvv) != 3:
                    return CvvInvalid
            return True
        except CvvInvalid as a:
            print(a)
