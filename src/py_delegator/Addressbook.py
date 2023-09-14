import pickle
import re
from collections import UserDict
from collections import deque
from datetime import datetime, timedelta
from copy import deepcopy

contact = None
ab = None
was_saved = False

info = "Hello, this is your Addressbook! Commands available by request 'commands'"


def info_command():
    print("Available commands: 'record', 'view', 'add number', 'add email', 'upcoming', 'find', 'remove', 'edit', 'save', 'open'")


def check_empty_ab(func):
    def wrapper(self, *args, **kwargs):
        if not self.data:
            print("Addressbook is empty. Add contacts and try again!")
        else:
            return func(self, *args, **kwargs)

    return wrapper


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, record):
        if record["Name"] not in self.data.keys():
            self.data[record["Name"]] = record
            print("New contact was successfully added to addressbook")
        else:
            print(f"Contact {record['Name']} is already exists")

    @check_empty_ab
    def view(self):
        [last_key] = deque(self.data, maxlen=1)
        print("------------------------------------")
        for key, el in self.data.items():
            print("{:<18} {:<10}".format("Name:", el["Name"]))
            print("{:<18} {:<10}".format("Address: ", el["Address"]))
            print("{:<18} {:<10}".format("Phone number(s):", ", ".join(el["Number"])))
            print("{:<18} {:<10}".format("Email address(es):", ", ".join(el["Email"])))
            print("{:<18} {}".format("Birthdate:", el["Birthdate"]))
            if len(self.data) > 1 and key != last_key:
                print("************************************")
        print("------------------------------------")

    @check_empty_ab
    def add_phone(self):
        contact_enter = input("Choose contact for adding phonenumber: ")
        if contact_enter in self.data.keys():
            added = input("Enter additional phonenumber: ")
            if re.match(Contact._PATTERN_FOR_PHONE, added):
                self.data[contact_enter]["Number"].append(added)
                print(f"Additional phonenumber to contact {contact_enter} was successfully added")
            else:
                print("Invalid phone number. Try again next time!")
        else:
            print(f"Contact {contact_enter} isn't exist. Select one of your existing contacts!")

    @check_empty_ab
    def add_email(self):
        contact_enter = input("Choose contact for adding email address: ")
        if contact_enter in self.data.keys():
            added = input("Enter a backup email address: ")
            if re.match(Contact._PATTERN_FOR_EMAIL, added):
                self.data[contact_enter]["Email"].append(added)
                print(f"Backup email address to contact {contact_enter} was successfully added")
            else:
                print("Invalid email address. should be 'examples@com.ua'")
        else:
            print(f"Contact {contact_enter} isn't exist. Check the correctness of the data and try again!")

    @check_empty_ab
    def coming_birthdays(self):
        current_bd = dict()
        bd_actual = dict()
        period = int(input("Enter the end period (number of days) to search for upcoming celebrations: "))
        start_period = datetime.now().date()
        end_period = start_period + timedelta(days=period)
        for contact_name, contact_data in self.data.items():
            for key, value in contact_data.items():
                if key == "Birthdate" and value:
                    current_bd.update({contact_name: value.replace(year=datetime.now().year)})
        for name, date in current_bd.items():
            if date < start_period:
                bd_actual.update({name: date.replace(year=start_period.year + 1)})
            else:
                bd_actual.update({name: date})
        bd_dict = {name: date for name, date in bd_actual.items() if end_period >= date >= start_period}
        bd_dict = dict(sorted(bd_dict.items(), key=lambda item: item[1]))
        if bd_dict:
            result_string = f"Today is {start_period}"
            for name, date in bd_dict.items():
                result_string += f", celebrate {name} in {(date - start_period).days} day(s) ({date})"
        else:
            result_string = "There are no celebrations for this period"
        print(result_string)

    @check_empty_ab
    def find(self):
        search_str = str(input("Enter name or phonenumber for search (include partly): ")).lower()
        print("!" * 40)
        contact_find = False
        for name, phone in self.data.items():
            name_lower = name.lower()
            if search_str in name_lower or search_str in str([phone["Number"]]):
                if contact_find:
                    print("*" * 40)
                print("{:<18} {:<10}".format("Name:", phone["Name"]))
                print("{:<18} {:<10}".format("Address:", phone["Address"]))
                print("{:<18} {:<10}".format("Phone number(s):", ", ".join(phone["Number"])))
                print("{:<18} {:<10}".format("Email address(es):", ", ".join(phone["Email"])))
                print("{:<18} {}".format("Birthdate:", phone["Birthdate"]))
                contact_find = True
            else:
                continue
        if not contact_find:
            print("Unfortunately, there aren't exist contacts by your request")
        print("!" * 40)

    @check_empty_ab
    def remove_contact(self):
        index = input("Enter the name of contact for removing: ")
        if index in self.data:
            self.data.pop(index)
            print(f"Contact {index} was successfully removed from your addressbook")
        else:
            print("Removing is impossible. The specified contact does not exist")

    @check_empty_ab
    def edit_contact(self):
        enter = input("Enter the name of contact for editing: ")
        new_dict = {}
        contacts_for_delete = []
        for name, record in self.data.items():
            if enter == name:
                attribute = input("Select a section to edit: ")
                if attribute.lower() in ["name", "person", "subject"]:
                    new_value = input("Enter the new name: ")
                    if re.match(Contact._PATTERN_FOR_NAME, new_value) and new_value != name:
                        record["Name"] = new_value
                        new_dict.update({new_value: record})
                        contacts_for_delete.append(name)
                        print(f"Contact name {name} was successfully edited to {new_value}")
                    else:
                        print("Invalid name. Should starts with upper case and consists real name")
                elif attribute.lower() in ["email", "edit email", "email address"]:
                    new_value = input("Enter the new email address: ")
                    if re.match(Contact._PATTERN_FOR_EMAIL, new_value):
                        record["Email"] = [new_value]
                        print(f"{name}'s email address was successfully edited to {new_value}")
                    else:
                        print("Invalid email address. should be 'examples@com.ua'")
                elif attribute in ["phone", "edit phone", "phonenumber", "number"]:
                    new_value = input("Enter the new phone number: ")
                    if re.match(Contact._PATTERN_FOR_PHONE, new_value):
                        record["Number"] = [new_value]
                        print(f"{name}'s phone number was successfully edited to {new_value}")
                    else:
                        print("Invalid phone number. Try again!")
                elif attribute in ["date", "birthdate", "birthday", "birth"]:
                    new_value = input("Enter the new birthdate: ")
                    if new_value:
                        chars = "/ ,-"
                        for char in chars:
                            new_value = new_value.replace(char, ".")
                        true_value = datetime.strptime(new_value, "%d.%m.%Y").date()
                        record["Birthdate"] = true_value
                        print(f"{name}'s birthdate  was successfully edited to {true_value}")
                    else:
                        print("Invalid birthdate. Enter correct data next time!")
                elif attribute in ["address", "home address", "home"]:
                    new_value = input("Enter the new street address: ")
                    if re.match(Contact._PATTERN_FOR_ADRESS, new_value):
                        record["Address"] = new_value
                        print(f"{name}'s street address was successfully edited to {new_value}")
                    else:
                        print("Invalid address. Should be like 'Avengers St. 22/123'")
                else:
                    print(f"Section {attribute} doesn't exist")
        if contacts_for_delete:
            for el in contacts_for_delete:
                self.data.pop(el)
                del contacts_for_delete
            self.data.update(new_dict)
        sorted_dict = dict(sorted(self.data.items()))
        self.data = deepcopy(sorted_dict)

    @check_empty_ab
    def load(self):
        global was_saved
        file_name = input("Write name of file that should be created in format 'name.file_extension': ")
        if re.match(r"[\w\d]+\.\w+", file_name):
            with open(file_name, "wb") as file:
                pickle.dump(self.data, file)
                print("Data was successfully saved")
                was_saved = True
        else:
            print("Wrong filename format. Should be like 'example.extension'")

    def ab_cont(self):
        while True:
            file_name = input("Write name of file from where should be imported data in format 'name.file extension': ")
            if re.match(r"[\w\d]+\.\w+", file_name):
                try:
                    with open(file_name, "rb") as file:
                        self.data = pickle.load(file)
                        print("Data was opened")
                        break
                except FileNotFoundError:
                    print("There's no exist. Enter true filename!")
            else:
                print("Wrong filename format. Should be like 'example.extension'")

ab = AddressBook()


class Contact(UserDict):
    _PATTERN_FOR_NAME = r"^[A-Z][a-z]+(?:[-][A-Z][a-z]+)?(?:[ -][A-Z][a-z]+)?(?:[ ][A-Z][a-z]+)?(?:[-][A-Z][a-z]+)?\b"
    _PATTERN_FOR_PHONE = r'^\+?\d{11,16}$|^\d{10,12}$|^\+?\d{0,4}\(\d{3}\)\d{7,9}$|^\+?\d{0,4}\(\d{3}\)\d{1,3}-\d{1,3}-\d{1,3}$|^\(\d{3}\)\d{1,3}-\d{1,3}-\d{1,3}\|^\d{3}-\d{1,3}-\d{1,3}-\d{1,3}$'
    _PATTERN_FOR_ADRESS = r"(?:[a-zA-Z]+[\s-]){1,}St. \d+\/\d+"
    _PATTERN_FOR_EMAIL = r"[a-z\d_-]+@[a-z]+\.[a-z]+(?:\.[a-z]+)?"

    """
    Клас, що формує контактну книгу (всю інформацію про один певний контакт)
    """

    def __init__(self, name=None, adress=None, phonenumber=None, email=None, birthdate=None):
        super().__init__()
        self.__name = None
        self.name = name
        self.data["Name"] = self.name
        self.__address = None
        self.adress = adress
        self.data["Address"] = self.adress
        self.__phonenumber = []
        self.phonenumber = phonenumber
        self.data["Number"] = self.phonenumber
        self.__email = []
        self.email = email
        self.data["Email"] = self.email
        self.__birthdate = None
        self.birthdate = birthdate
        self.data["Birthdate"] = self.birthdate

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if re.match(self._PATTERN_FOR_NAME, value):
            self.__name = value
        else:
            print(
                "Invalid name. Should starts with upper case and consists real name with/without patronymic and surname")

    @property
    def adress(self):
        return self.__address

    @adress.setter
    def adress(self, value):
        if value:
            if re.match(self._PATTERN_FOR_ADRESS, value):
                self.__address = value
            else:
                print(
                    "Invalid street address. Address format: 'Mykhaylo Kandinsky St. 23/422'. The address can also contain dashes")

    @property
    def phonenumber(self):
        return self.__phonenumber

    @phonenumber.setter
    def phonenumber(self, value):
        if value:
            if re.match(self._PATTERN_FOR_PHONE, value):
                self.__phonenumber = [value]
            else:
                print("Invalid phone number")

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if value:
            if re.match(self._PATTERN_FOR_EMAIL, value):
                self.__email = [value]
            else:
                print("Wrong email address: Format: 'name@example.com' or 'name@example.com.ua' ")

    @property
    def birthdate(self):
        return self.__birthdate

    @birthdate.setter
    def birthdate(self, value):
        try:
            if value:
                chars = "/ ,-"
                for char in chars:
                    value = value.replace(char, ".")
                self.__birthdate = datetime.strptime(value, "%d.%m.%Y").date()  # Валідація дати народження
        except ValueError:
            print("Invalid birtdate. Expecting 'DD.MM.YYYY', with punctuation (' ,-/'")


def write_contact():
    """
    Проміжна команда, яка створює контактну картку й одразу проходить всі валідації. Якщо все ок - записую в адрессбук
    """
    global contact
    print("Enter the following data to fill out the contact card:")
    while True:
        name = input(
            "Name (should starts with upper case and consists real name with/without patronymic and surname): ")
        if Contact(name).name:
            if Contact(name).name in ab.data.keys():
                print("The entered contact already exists. Enter a unique name.")
                continue
            break
    while True:
        address = input("Address (for example, 'Mykhaylo Kandinsky St. 23/422'):  ")
        if Contact(name, address).adress:
            break
    while True:
        phonenumber = input("Phone number: ")
        if Contact(name, address, phonenumber).phonenumber:
            break
    while True:
        email = input("Email (for example, 'name@example.com' or 'name@example.com.ua'): ")
        if Contact(name, address, phonenumber, email).email:
            break
    while True:
        birthdate = input("Birthdate (in format 'DD.MM.YYYY'): ")
        if Contact(name, address, phonenumber, email, birthdate).birthdate:
            break
    contact = Contact(name, address, phonenumber, email, birthdate)
    if contact.name and contact.adress and contact.phonenumber and contact.email and contact.birthdate:
        ab.add_record(contact)
    else:
        print("Відсутня контактна картка для додавання")


commands = {
    write_contact: "record",  # Команда, яка формує контактну картку і записує її одразу в адрессбук
    ab.view: "view",  # Перегляд одразу всього адрессбуку
    ab.add_phone: "add number",  # Команда, яка додає номер до існуючого контакту
    info_command: "commands",  # Інфо-команда, яка виводе список всіх доступних команд
    ab.add_email: "add email",  # Команда, яка додає email до існуючого контакту
    ab.coming_birthdays: "upcoming",
    # Команда, яка в залежності від заданої кількості днів виводить дні народження записаних контактів в періоді від сьогодні до заданої кількості днів
    ab.find: "find",  # Команда, яка знаходить контактів за номером або ім'ям
    ab.remove_contact: "remove",  # Команда, яка видаляє зазначений контакт
    ab.edit_contact: "edit",  # Команда, яка редагує атрибути зазначеного контакту
    ab.load: "save",  # Команда, яка зберігає файл
    ab.ab_cont: "open"  # Команда, що відкриває файл
}


def start():  # точка входу
    print(info)
    cont_data = input("Would you like to continue use previous data? (Y/n) ")
    while True:
        if cont_data == ("Y" or "y"):
           ab.ab_cont()
           break
        elif cont_data == ("n" or "n"):
            print("So, we will launch in first origin mode")
            break
        else:
            print("Try again!")
            cont_data = input("(Y/n): ")
    while True:
        command = input("Enter command --> ").lower()
        if command in commands.values():
            for key, value in commands.items():
                if command == value:
                    key()
        elif command in ["quit", "close", "bye", "exit"]:
            if ab.data and not was_saved:
                closing = input("Do you want to save data before exiting? (Y/n) ")
                if closing == ("Y" or "y"):
                    ab.load()
            print("Good bye! Your AddressBook helper will see you later :)")
            break
        else:
            print("Wrong command! Choose one of available commands!\n(Review available commands - 'commands')")


# start()  # запускається помічник тут
