from collections import UserDict
import re
from collections import deque
from datetime import datetime, timedelta
from copy import deepcopy
contact = None
ab = None

info = "Привіт, це твій особистий помічник\nДоступні команди за запитом 'команди'"

def info_command():
    print("Доступні команди: 'записати', 'email', 'номер', 'перегляд', 'знайти', 'дні', 'редагувати', 'видалити'")

def check_empty_ab(func):
    def wrapper(self, *args, **kwargs):
        if not self.data:
            print("Адресна книга порожня. Додайте контактні картки до неї")
        else:
            return func(self, *args, **kwargs)
    return wrapper


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, record):
        if record["Ім'я"] not in self.data.keys():
            self.data[record["Ім'я"]] = record
            print("Новий контакт успішно додано до телефонної книги")
        else:
            print("Контакт вже існує")

    @check_empty_ab
    def view(self):
        [last_key] = deque(self.data, maxlen=1)
        print("------------------------------------")
        for key, el in self.data.items():
            print("{:<18} {:<10}".format("Ім'я:", el["Ім'я"]))
            print("{:<18} {:<10}".format("Адреса:", el["Адреса"]))
            print("{:<18} {:<10}".format("Номери телефону:", ", ".join(el["Телефон"])))
            print("{:<18} {:<10}".format("Поштові скриньки:", ", ".join(el["Email"])))
            print("{:<18} {}".format("Birthdate:", el["Birthdate"]))
            if len(self.data) > 1 and key != last_key:
                print("************************************")
        print("------------------------------------")

    @check_empty_ab
    def add_phone(self):
        contact_enter = input("Введіть контакт, якому хочете додати номер: ")
        if contact_enter in self.data.keys():
            added = input("Введіть додатковий номер телефону: ")
            if re.match(Contact._PATTERN_FOR_PHONE, added):
                self.data[contact_enter]["Телефон"].append(added)
                print(f"Додатковий номер до контакту {contact_enter} успішно додано")
        else:
            print("Зазначеного контакту не існує. Створіть його")

    @check_empty_ab
    def add_email(self):
        contact_enter = input("Введіть контакт, якому хочете додати поштову скриньку: ")
        if contact_enter in self.data.keys():
            added = input("Введіть запасну поштову скриньку: ")
            if re.match(Contact._PATTERN_FOR_EMAIL, added):
                self.data[contact_enter]["Email"].append(added)
                print(f"Додатковий email до контакту {contact_enter} успішно додано")
            else:
                print("Зазначеного контакту не існує. Створіть його")
        else:
            print("Адресна книга порожня. Додайте контактні картки до неї")

    @check_empty_ab
    def coming_birthdays(self):
        current_bd = dict()
        bd_actual = dict()
        period = int(input("Введіть кінцевий період (кількість днів) для пошуку найближчих святкувань: "))
        start_period = datetime.now().date()
        end_period = start_period + timedelta(days=period)
        for contact_name, contact_data in self.data.items():  # ключ - название контакта, значение - контакт
            for key, value in contact_data.items():           # Birthdate : datetime
                if key == "Birthdate" and value:
                    current_bd.update({contact_name: value.replace(year=datetime.now().year)})
        for name, date in current_bd.items():
            if date < start_period:
                bd_actual.update({name: date.replace(year=start_period.year+1)})
            else:
                bd_actual.update({name: date})
        bd_dict = {name: date for name, date in bd_actual.items() if end_period >= date >= start_period}
        bd_dict = dict(sorted(bd_dict.items(), key=lambda item: item[1]))
        if bd_dict:
            result_string = f"Сьогодні {start_period}"
            for name, date in bd_dict.items():
                result_string += f", через днів: {(date - start_period).days} привітати {name} ({date})"
        else:
            result_string = "За вказаним періодом немає святкувань"
        print(result_string)

    @check_empty_ab
    def find(self):
        print(self.data)
        search_str = str(input("Введіть номер або ім'я : ")).lower()
        print("!" * 40)
        contact_find = False
        for name, phone in self.data.items():
            name_lower = name.lower()
            if search_str in name_lower or search_str in str([phone["Телефон"]]):
                if contact_find:
                    print("*" * 40)
                print("{:<18} {:<10}".format("Ім'я:", phone["Ім'я"]))
                print("{:<18} {:<10}".format("Адреса:", phone["Адреса"]))
                print("{:<18} {:<10}".format("Номери телефону:", ", ".join(phone["Телефон"])))
                print("{:<18} {:<10}".format("Поштові скриньки:", ", ".join(phone["Email"])))
                print("{:<18} {}".format("Birthdate:", phone["Birthdate"]))
                contact_find = True
            else:
                continue
        if not contact_find:
            print("Не знайдено контактів за вашим запитом")
        print("!" * 40)

    @check_empty_ab
    def remove_contact(self):
        index = input("Введіть контакт, що бажаєте видалити: ")
        if index in self.data:
            self.data.pop(index)
            print(f"Контакт {index} було успішно видалено із телефонної книги")
        else:
            print("Видалення неможливе. Зазначеного контакту не існує")

    @check_empty_ab
    def edit_contact(self):
        enter = input("Введіть ім'я контакту, що бажаєте відредагувати: ")
        new_dict = {}
        contacts_for_delete = []
        for name, record in self.data.items():
            if enter == name:
                attribute = input("Введіть розділ, щол потрібно відредагувати: ")
                if attribute in ["name", "person", "subject"]:
                    new_value = input("Введіть нові дані name: ")
                    if re.match(Contact._PATTERN_FOR_NAME, new_value) and new_value != name:
                        record["Ім'я"] = new_value
                        new_dict.update({new_value: record})
                        contacts_for_delete.append(name)
                        print(f"Ім'я контакту {name} було успішно змінено на {new_value}")
                    else:
                        print("Ім'я записано некоректно. Воно має бути з великої літери")
                elif attribute in ["email", "edit email", "email address"]:
                    new_value = input("Введіть нові дані Email: ")
                    if re.match(Contact._PATTERN_FOR_EMAIL, new_value):
                        record["Email"] = [new_value]
                        print(f"Email контакту {name} було успішно змінено на {new_value}")
                    else:
                        print("Email записано некоректно.")
                elif attribute in ["phone", "edit phone", "phonenumber", "number"]:
                    new_value = input("Введіть нові дані PhoneNumber: ")
                    if re.match(Contact._PATTERN_FOR_PHONE, new_value):
                        record["Телефон"] = [new_value]
                        print(f"Телефон контакту {name} було успішно змінено на {new_value}")
                    else:
                        print("Телефон записано некоректно.")
                elif attribute in ["date", "birthdate", "birthday", "birth"]:
                    new_value = input("Введіть нові дані Birthdate: ")
                    if new_value:
                        chars = "/ ,-"
                        for char in chars:
                            new_value = new_value.replace(char, ".")
                        true_value = datetime.strptime(new_value, "%d.%m.%Y").date()
                        record["Birthdate"] = true_value
                        print(f"Birthdate контакту {name} було успішно змінено на {true_value}")
                    else:
                        print("Birthdate записано некоректно.")
                elif attribute in ["address", "home address", "home"]:
                    new_value = input("Введіть нові дані Address: ")
                    if re.match(Contact._PATTERN_FOR_ADRESS, new_value):
                        record["Адреса"] = new_value
                        print(f"Адреса контакту {name} було успішно змінено на {new_value}")
                    else:
                        print("Адреса записано некоректно.")
                else:
                    print("Зазначеного атрибуту немає")
        if contacts_for_delete:
            for el in contacts_for_delete:
                self.data.pop(el)
                del contacts_for_delete
            self.data.update(new_dict)
        sorted_dict = dict(sorted(self.data.items()))
        self.data = deepcopy(sorted_dict)


ab = AddressBook()


class Contact(UserDict):
    _PATTERN_FOR_NAME = r"^[A-ZА-ЩЬЮ-ЯІҐЄ][a-zа-щью-яґіїє`]+(?:[-][A-ZА-ЩЬЮ-ЯІҐЄ][a-zа-щью-яґіїє`^]+)?(?:[ -][A-ZА-ЩЬЮ-ЯІҐЄ][a-zа-щью-яґїіє`^]+)?(?:[ ][A-ZА-ЩЬЮ-ЯІҐЄ][a-zа-щью-яґіїє`^]+)?(?:[-][A-ZА-ЩЬЮ-ЯІҐЄ][a-zа-щью-яґіїє`^]+)?\b"
    _PATTERN_FOR_PHONE = r'^\+?\d{11,16}$|^\d{10,12}$|^\+?\d{0,4}\(\d{3}\)\d{7,9}$|^\+?\d{0,4}\(\d{3}\)\d{1,3}-\d{1,3}-\d{1,3}$|^\(\d{3}\)\d{1,3}-\d{1,3}-\d{1,3}\|^\d{3}-\d{1,3}-\d{1,3}-\d{1,3}$'
    _PATTERN_FOR_ADRESS = r"вул\. (?:[a-щь-яА-ЩЬ-ЯїЇіІ'єЄҐґ]+[\s-]){1,}\d+\/\d+"
    _PATTERN_FOR_EMAIL = r"[a-z\d_-]+@[a-z]+\.[a-z]+(?:\.[a-z]+)?"

    """
    Клас, що формує контактну книгу (всю інформацію про один певний контакт)
    """

    def __init__(self, name=None, adress=None, phonenumber=None, email=None, birthdate=None):
        super().__init__()
        self.__name = None
        self.name = name
        self.data["Ім'я"] = self.name
        self.__address = None
        self.adress = adress
        self.data["Адреса"] = self.adress
        self.__phonenumber = []
        self.phonenumber = phonenumber
        self.data["Телефон"] = self.phonenumber
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
            print("Ім'я записано некоректно. Потрібно записати з великої літери")

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
                    "Адреса записана невірно. Формат адреси: 'вул. Михайла Коцубинського 23/422'. Адреса також може містити тире")

    @property
    def phonenumber(self):
        return self.__phonenumber

    @phonenumber.setter
    def phonenumber(self, value):
        if value:
            if re.match(self._PATTERN_FOR_PHONE, value):
                self.__phonenumber = [value]
            else:
                print("Телефон записан невірно")

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if value:
            if re.match(self._PATTERN_FOR_EMAIL, value):
                self.__email = [value]
            else:
                print("Електронна адреса записана невірно. Формат email: 'name@example.com' або 'name@example.com.ua' ")

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
            print("Невірний формат дати. Потрібно 'DD.MM.YYYY'. Розділовими знаками можуть бути ' ,-/'")


def write_contact():
    """
    Проміжна команда, яка створює контактну картку й одразу проходить всі валідації. Якщо все ок - записую в адрессбук
    """
    global contact
    print("Для заповнення контактної картки потрібно ввести наступні дані:")
    while True:
        name = input("Імя: ")
        if Contact(name).name:
            if Contact(name).name in ab.data.keys():
                print("Введений контакт вже існує. Введіть унікальне ім'я.")
                continue
            break
    while True:
        address = input("Адреса: ")
        if Contact(name, address).adress:
            break
    while True:
        phonenumber = input("Номер телефону: ")
        if Contact(name, address, phonenumber).phonenumber:
            break
    while True:
        email = input("Email: ")
        if Contact(name, address, phonenumber, email).email:
            break
    while True:
        birthdate = input("Birthdate: ")
        if Contact(name, address, phonenumber, email, birthdate).birthdate:
            break
    contact = Contact(name, address, phonenumber, email, birthdate)
    if contact.name and contact.adress and contact.phonenumber and contact.email and contact.birthdate:
        ab.add_record(contact)
    else:
        print("Відсутня контактна картка для додавання")


commands = {
    write_contact: "записати",   # Команда, яка формує контактну картку і записує її одразу в адрессбук
    ab.view: "перегляд",         # Перегляд одразу всього адрессбуку
    ab.add_phone: "номер",              # Команда, яка додає номер до існуючого контакту
    info_command: "команди",     # Інфо-команда, яка виводе список всіх доступних команд
    ab.add_email: "email",              # Команда, яка додає email до існуючого контакту
    ab.coming_birthdays: "дні",  # Команда, яка в залежності від заданої кількості днів виводить дні народження записаних контактів в періоді від сьогодні до заданої кількості днів
    ab.find: "знайти",           # Команда, яка знаходить контактів за номером або ім'ям
    ab.remove_contact: "видалити",  # Команда, яка видаляє зазначений контакт
    ab.edit_contact: "редагувати"   # Команда, яка редагує атрибути зазначеного контакту
}


def start():  # точка входу

    """
    Це програма, яка працює у нескінченному циклі, поки користувач не введе "вихід", "бувай", "закрити",
    або сповіщає користувача, що команди зі словника commands не існує
    """

    print(info)
    while True:
        command = input("Введіть команду --> ").lower()
        if command in commands.values():
            for key, value in commands.items():
                if command == value:
                    key()
        elif command in ["вихід", "бувай", "закрити"]:
            print("Good bye! Your personal helper will see you later :)")
            break
        else:
            print("Недоступна команда. Введіть одну із доступних команд!\n(перегляд команд за запитом 'команди')")


start()  # запускається помічник тут
