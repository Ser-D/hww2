import re
from collections import UserDict
from datetime import datetime
import pickle
from abstract import InterfaceForBooks


class Field:
    """Клас Field використовується як базовий клас для інших полів, що містять дані (адреса, електронна пошта, телефон тощо)"""

    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

    def __str__(self):
        return str(self.value)


class Address(Field):
    """Клас Address що успадковується від Field та розширює його функціонал"""
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if value:
            self.__value = value.title()
        else:
            self.__value = None


class Email(Field):
    """Клас Email що успадковується від Field та розширює його функціонал"""
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        """метод перевірки введення електронної пошти"""
        if value:
            result = None
            get_email = re.findall(r'\b[a-zA-Z][\w\.]+@[a-zA-Z]+\.[a-zA-Z]{2,}', value)
            for i in get_email:
                result = i
            if result is None:
                raise AttributeError(f" Email is not correct {value}")
            self.__value = result
        else:
            self.__value = None


class Name(Field):
    """Клас Name що успадковується від Field та розширює його функціонал"""
    pass


class Phone(Field):
    """Клас Phone що успадковується від Field та розширює його функціонал"""
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value: str):
        """метод перевірки на правильність формату номера телефону"""
        if len(new_value) == 10 and new_value.isdigit():
            self.__value = new_value
        else:
            raise ValueError("invalid phone number")

    def __str__(self):
        return self.value


class Birthday(Field):
    """Клас Address що успадковується від Field та розширює його функціонал"""
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, date_birthday: str):
        if date_birthday:
            self.__value = date_birthday

    @classmethod
    def is_valid_value(cls, date_birthday):
        """метод перевірки на правильність формату дати народження"""
        try:
            datetime.strptime(date_birthday, '%d.%m.%Y')
            return True
        except ValueError:
            return False


class Record:
    """Клас Record представляє контакт із інформацією про ім'я, телефон, день народження, електронну пошту та адресу"""
    def __init__(self, name, phone=None, birthday=None, email=None, address=None):
        self.name = Name(name)
        if phone:
            self.phones = []
            self.phones.append(Phone(phone))
        else:
            self.phones = []
        self.birthday = Birthday(birthday)
        self.email = Email(email)
        self.address = Address(address)

    def add_phone(self, phone):
        """метод додавання номеру телефону контакту"""
        if phone not in (str(ph) for ph in self.phones):
            self.phones.append(Phone(phone))
            return f'Number {phone} already exist in contact {self.name.value}'
        return f'Number {phone} is already available in contact {self.name.value}'

    def add_email(self, email):
        """метод додавання номеру електронної пошти контакту"""
        self.email = Email(email)

    def add_address(self, address):
        """метод додавання адреси контакту"""
        self.address = Address(address)

    def add_birthday(self, birthday):
        """метод додавання дня народження контакту"""
        if Birthday.is_valid_value(birthday):
            self.birthday = Birthday(birthday)
        else:
            raise ValueError("format must be dd.mm.yyyy")

    def find_phone(self, phone_number):
        """метод пошуку за номером телефону"""
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def remove_phone(self, phone_number):
        """метод видалення номеру телефону"""
        phone_object = self.find_phone(phone_number)
        if phone_object:
            self.phones.remove(phone_object)

    def edit_phone(self, phone_old_number, phone_new_number):
        """метод заміни номеру телефону"""
        phone_object = self.find_phone(phone_old_number)
        if phone_object:
            phone_object.value = phone_new_number
        else:
            raise ValueError

    def __str__(self):
        return (f"Contact name: {self.name.value}\n"
                f"Phones: {'; '.join(p.value for p in self.phones)}\n"
                f"Birthday: {self.birthday.value if self.birthday else 'no'}\n"
                f"Email: {self.email.value if self.email else 'no'}\n"
                f"Address: {self.address.value if self.address else 'no'}\n")


class AddressBook(UserDict, InterfaceForBooks):
    """Клас використовується для управління адресною книгою, яка містить контакти (Record)."""
    def __init__(self):
        super().__init__()
        self.file_name = "addressBook.bin"

    def iterator(self, n: int = 2):
        result = f"{'-' * 50}\n"
        count = 0
        id_ = 0
        for name, record in self.data.items():
            result += f"{id_}: {record}\n"
            id_ += 1
            count += 1
            if count >= n:
                yield result
                count = 0
                result = f"{'-' * 50}\n"
        yield result

    def add_record(self, record_: Record):
        """метод додавання запису контакту"""
        self.data[record_.name.value] = record_

    def find_record(self, name_):
        """метод пошуку контакту за ім'ям"""
        return self.data.get(name_)

    def delete(self, record):
        """метод видалення запису контакту"""
        if record in self.data:
            del self.data[record]

    def save_to_file(self, file):
        """метод збереження запису контакту у файл"""
        with open(file, "wb") as fh:
            pickle.dump(self.data, fh)
            # print(type(fh))

    def load_from_file(self, file):
        """метод завантаження адресної книги з файлу"""
        try:
            with open(file, "rb") as fh:
                self.data = pickle.load(fh)
        except FileNotFoundError:
            print("File not found")

    def search_informathion(self, info: str) -> str:
        """метод пошуку контактів за інформацією"""
        correct_info = ""
        for name_, record_ in self.data.items():
            if info.lower() in name_.lower():
                correct_info += str(record_) + "\n"
            else:
                for phone in record_.phones:
                    if info.lower() in phone.value.lower():
                        correct_info += str(record_) + "\n"
                        break
        return correct_info
    def show_all(self):
        if len(self.data) != 0:
            for data_ in self.data:
                print(self.data[data_])
        print('Nothing to show')

    def find_birthdays_in_days(self, days: int):
        """метод знаходження контактів, чий день народження наближається у визначений кількість днів"""
        today = datetime.now()
        result = []
        for record_ in self.data.values():
            if record_.birthday.value:
                birthday_date = datetime.strptime(record_.birthday.value, '%d.%m.%Y')
                if today > birthday_date.replace(year=today.year):
                    next_birthday_date = birthday_date.replace(year=today.year + 1)
                else:
                    next_birthday_date = birthday_date.replace(year=today.year)

                days_until_birthday = (next_birthday_date - today).days

                if 0 <= days_until_birthday <= days:
                    result.append((record_, days_until_birthday))
        return result
