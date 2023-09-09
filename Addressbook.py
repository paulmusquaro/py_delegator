from collections import UserDict
import re
from collections import deque
from datetime import datetime, timedelta

contact = None
ab = None

info = "Привіт, це твій особистий помічник\nДоступні команди за запитом 'команди'"


def info_command():
    print("Доступні команди: 'записати', 'email', 'номер', 'команди', 'перегляд', 'знайти', 'дні'")


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, record):
        if record["Ім'я"] not in self.data.keys():
            self.data[record["Ім'я"]] = record
            print("Новий контакт успішно додано до телефонної книги")
        else:
            print("Контакт вже існує")

    def view(self):
        try:
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
        except ValueError:
            print("Відсутні контактні картки")

    def add_phone(self):
        contact_enter = input("Введіть контакт, якому хочете додати номер: ")
        pattern_for_phone = r'^\+?\d{11,16}$|^\d{10,12}$|^\+?\d{0,4}\(\d{3}\)\d{7,9}$|^\+?\d{0,4}\(\d{3}\)\d{1,3}-\d{1,3}-\d{1,3}$|^\(\d{3}\)\d{1,3}-\d{1,3}-\d{1,3}\|^\d{3}-\d{1,3}-\d{1,3}-\d{1,3}$'
        if contact_enter in self.data.keys():
            added = input("Введіть додатковий номер телефону: ")
            if re.match(pattern_for_phone, added):
                self.data[contact_enter]["Телефон"].append(added)
                print(f"Додатковий номер до контакту {contact_enter} успішно додано")
        else:
            print("Зазначеного контакту не існує. Створіть його")

    def add_email(self):
        contact_enter = input("Введіть контакт, якому хочете додати поштову скриньку: ")
        pattern_for_email = r"[a-z\d]+@[a-z]+\.[a-z]+(?:\.[a-z]+)?"
        if contact_enter in self.data.keys():
            added = input("Введіть запасну поштову скриньку: ")
            if re.match(pattern_for_email, added):
                self.data[contact_enter]["Email"].append(added)
                print(f"Додатковий email до контакту {contact_enter} успішно додано")
        else:
            print("Зазначеного контакту не існує. Створіть його")

    def coming_birthdays(self):
        current_bd = dict()
        period = int(input("Введіть кінцевий період (кількість днів) для пошуку найближчих святкувань: "))
        start_period = datetime.now().date()
        end_period = start_period + timedelta(days=period)
        for contact_name, contact_data in self.data.items():
            for key, value in contact_data.items():
                if key == "Birthdate":
                    current_bd.update({contact_name: value.replace(year=datetime.now().year)})
        bd_dict = {name: date for name, date in current_bd.items() if end_period >= date >= start_period}
        bd_dict = dict(sorted(bd_dict.items(), key=lambda item: item[1]))
        if bd_dict:
            result_string = f"Сьогодні {start_period}"
            for name, date in bd_dict.items():
                result_string += f", через днів: {(date - start_period).days} привітати {name} ({date})"
        else:
            result_string = "За вказаним періодом немає святкувань"
        print(result_string)

    def find(self):
        if self.data:
            search_str = str(input("Введіть номер або ім'я : ")).lower()
            print("!" * 40)
            contact_find = False
            for name, phone in self.data.items():
                name_lower = name.lower()
                if search_str in name_lower or search_str in phone["Телефон"]:
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
        else:
            print("Відсутні контакти у телефонній книзі")


ab = AddressBook()


class Contact(UserDict):

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
        if value.istitle():  # Тут проста перевірка, щоб користувач з великої літери вводив ім'я. Можливо ще додам регулярку, щоб тільки букви були без спецсимволів
            self.__name = value
        else:
            print("Ім'я записано некоректно. Потрібно записати з великої літери")

    @property
    def adress(self):
        return self.__address

    @adress.setter
    def adress(self, value):
        if value:
            pattern_for_adress = r"вул\. (?:[a-щь-яА-ЩЬ-ЯїЇіІ'єЄҐґ]+[\s-]){1,}\d+\/\d+"  # Валідація адреси
            if re.match(pattern_for_adress, value):
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
            pattern_for_phone = r'^\+?\d{11,16}$|^\d{10,12}$|^\+?\d{0,4}\(\d{3}\)\d{7,9}$|^\+?\d{0,4}\(\d{3}\)\d{1,3}-\d{1,3}-\d{1,3}$|^\(\d{3}\)\d{1,3}-\d{1,3}-\d{1,3}\|^\d{3}-\d{1,3}-\d{1,3}-\d{1,3}$'  # Валідація номера телефона
            if re.match(pattern_for_phone, value):
                self.__phonenumber = [value]
            else:
                print("Телефон записан невірно")

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if value:
            pattern_for_email = r"[a-z\d_-]+@[a-z]+\.[a-z]+(?:\.[a-z]+)?"  # Валідація email
            if re.match(pattern_for_email, value):
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


def add_p():
    if ab:
        ab.add_phone()
    else:
        print("Адресна книга порожня. Додайте контактні картки до неї")


def add_e():
    if ab:
        ab.add_email()
    else:
        print("Адресна книга порожня. Додайте контактні картки до неї")


commands = {
    write_contact: "записати",   # Команда, яка формує контактну картку і записує її одразу в адрессбук
    ab.view: "перегляд",         # Перегляд одразу всього адрессбуку
    add_p: "номер",              # Команда, яка додає номер до існуючого контакту
    info_command: "команди",     # Інфо-команда, яка виводе список всіх доступних команд
    add_e: "email",              # Команда, яка додає email до існуючого контакту
    ab.coming_birthdays: "дні",  # Команда, яка в залежності від заданої кількості днів виводить дні народження записаних контактів в періоді від сьогодні до заданої кількості днів
    ab.find: "знайти"            # Команда, яка знаходить контактів за номером або ім'ям
}


def start():  # точка входу

    """
    Це програма, яка працює у нескінченному циклі, поки користувач не введе "вихід", "бувай", "закрити",
    або сповіщає користувача, що команди зі словника commands не існує
    """

    print(info)
    while True:
        command = input("Введіть команду --> ").lower()
        if not command:
            continue
        elif command in commands.values():
            for key, value in commands.items():
                if command == value:
                    key()
        elif command in ["вихід", "бувай", "закрити"]:
            break
        else:
            print("Недоступна команда. Перегляд команд за запитом 'команди'")


start()  # запускається помічник тут
