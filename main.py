# Пояснення:
# 1.	Базовий клас UserInterface описує методи для відображення контактів, команд і введення даних.
# 2.	Конкретна реалізація ConsoleUserInterface реалізує ці методи для роботи з консольним інтерфейсом.
# 3.	Клас Bot тепер використовує інтерфейс для взаємодії з користувачем, що дозволяє легко змінювати
#       спосіб взаємодії (якщо, наприклад, ви захочете додати графічний інтерфейс або вебінтерфейс, треба
#       буде лише створити новий клас, що успадковує UserInterface).
# Це дозволяє вам розширювати або змінювати інтерфейс без значних змін в основній логіці програми.


from datetime import date, datetime
import re
from abc import ABC, abstractmethod
from Address_book import *
from Notebook import *
from sorting import *

class UserInterface(ABC):
    """
    Абстрактний базовий клас для користувальницьких уявлень.
    Визначає загальні методи для виведення інформації.
    """

    @abstractmethod
    def display_contact_card(self, contact):
        """
        Вивести картку контакту.
        """
        pass

    @abstractmethod
    def display_commands(self, commands):
        """
        Вивести список доступних команд.
        """
        pass

    @abstractmethod
    def get_input(self, prompt):
        """
        Взяти ввід від користувача.
        """
        pass

class ConsoleUserInterface(UserInterface):
    """
    Реалізація користувальницького інтерфейсу для консольного додатка.
    """

    def display_contact_card(self, contact):
        """
        Вивести картку контакту в консоль.
        """
        print(contact)
        # print(f"Контакт: {contact.name}")
        # print(f"Телефони: {', '.join(contact.phones)}")
        # print(f"Адреса: {contact.address}")
        # print(f"Дата народження: {contact.birthday.strftime('%d/%m/%Y') if contact.birthday else 'Не вказано'}")
        # print(f"Email: {contact.email}")
        # print("-" * 30)

    def display_commands(self, commands):
        """
        Вивести список доступних команд у консоль.
        """
        print("Доступні команди:")
        for command in commands:
            print(f"- {command}")

    def get_input(self, prompt):
        """
        Взяти ввід від користувача в консоль.
        """
        return input(prompt)

class Name:
    def __init__(self, value):
        self.value = value

    def __getitem__(self):
        return self.value


class Phone:
    def __init__(self):
        while True:
            self.values = []
            self.value = input("Enter phones with code: +38 plus 10 numbers after:")
            try:
                for number in self.value.split(' '):
                    if re.match('^\\+38\d{10}$', number):
                        self.values.append(number)
                    else:
                        raise ValueError
            except ValueError:
                print('Incorrect phone number!')
            else:
                break

    def __getitem__(self):
        return self.values


class Address:
    def __init__(self, value=""):
        self.value = value

    def __getitem__(self):
        return self.value


class Birthday:
    def __init__(self, value=''):
        while True:
            if value:
                self.value = value
            else:
                self.value = input("Birthday date in format (dd/mm/yyyy) : ")
            try:
                if re.match('^\d{2}/\d{2}/\d{4}$', self.value):
                    self.value = datetime.strptime(self.value, "%d/%m/%Y")
                    break
                elif self.value == '':
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Incorrect date! Please provide correct date format.')

    def __getitem__(self):
        return self.value


class Email:
    def __init__(self, value=''):
        while True:
            if value:
                self.value = value
            else:
                self.value = input("Email: ")
            try:
                if re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', self.value):
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Incorrect email! Please enter right email.')

    def __getitem__(self):
        return self.value


class Record:
    def __init__(self, name="", phones='', address='', birthday='', email=''):
        self.name = name
        self.phones = phones
        self.address = address
        self.birthday = birthday
        self.email = email

    def __str__(self):
        return (f"Contact name: {self.name},\nphones: {self.phones},\n"
                f"email: {self.email},\nbirthday: {self.birthday},\naddress: {self.address}")


class Bot:
    def __init__(self, ui: UserInterface):
        self.book = AddressBook()
        self.notebook = Notes()
        self.ui = ui  # Використовуємо інтерфейс для користувацького уявлення

    def handle(self, action):
        if action == 'add':
            #name = Name(input("Name: ")).value.strip()
            name = self.ui.get_input("Name: ").strip()
            phones = Phone().value
            birthday = Birthday().value
            email = Email().value.strip()
            address = Address(input("Address: ")).value.strip()
            record = Record(name, phones, address, birthday, email)
            self.ui.display_contact_card(record)
            #print(record)
            return self.book.add(record)
        elif action == 'search':
            #pattern = input('Enter Search pattern: ')
            pattern = self.ui.get_input('Enter Search pattern: ')
            result = self.book.search_by_match(pattern)
            if result:
                for item in result:
                    #print(item)
                    self.ui.display_contact_card(item)
            else:
                print("There is no such Contact name!")
        elif action == 'edit':
            # contact_name = input('Contact name: ')
            # parameter = input('Which parameter to edit(name, phones, birthday, address, email): ').strip()
            contact_name = self.ui.get_input('Contact name: ')
            parameter = self.ui.get_input('Which parameter to edit(name, phones, birthday, address, email): ').strip()
            return self.book.editing_contact(contact_name, parameter)
        elif action == 'remove':
            #contact_name = input('Contact name: ')
            contact_name = self.ui.get_input('Contact name: ')
            return self.book.delete(contact_name)
        elif action == 'save':
            #file_name = input("File name: ")
            file_name = self.ui.get_input("File name: ")
            return self.book.save(file_name)
        elif action == 'load':
            #file_name = input("File name: ")
            file_name = self.ui.get_input("File name: ")
            return self.book.load(file_name)
        elif action == 'birthdays':
            #days = input("Enter the number of days until Birthday: ")
            days = self.ui.get_input("Enter the number of days until Birthday: ")
            self.book.list_contacts_with_day_of_birthday(days)
        elif action == 'view':
            #print(self.book)
            self.ui.display_contact_card(self.book)
        elif action == 'sorting':
            #folder_path = input("Input path to folder where you want to sort files: ")
            folder_path = self.ui.get_input("Input path to folder where you want to sort files: ")
            file_sorter = FileSorter(folder_path)
            file_sorter.sort_files()
        elif action == 'notes':
            #note_action = input('Which action for Notes(add, find, edit, delete, sort, save): ').strip()
            note_action = self.ui.get_input('Which action for Notes(add, find, edit, delete, sort, save): ').strip()
            if note_action == "add":
                #text = input("Enter Note text: ")
                #tags = input("Enter Note tags: ").split()
                text = self.ui.get_input("Enter Note text: ")
                tags = self.ui.get_input("Enter Note tags: ").split()
                new_note = (Note(text))
                new_note.add_tag(tags)
                print(new_note)
                self.notebook.add(new_note)
            elif note_action == "find":
                #search_parameter = input("Search by tags(Y) or text(N): ")
                search_parameter = self.ui.get_input("Search by tags(Y) or text(N): ")
                search_parameter = True if search_parameter == "Y" else False
                find_text = self.ui.get_input("Enter Search pattern: ")
                #find_text = input("Enter Search pattern: ")
                search_result = self.notebook.find(find_text, search_parameter)
            elif note_action == "edit":
                #edit_text = input("Enter pattern for note: ")
                edit_text = self.ui.get_input("Enter pattern for note: ")
                edit_note = self.notebook.find(edit_text, False)[0]
                self.notebook.edit_note(edit_note)
            elif note_action == "delete":
                #edit_text = input("Enter pattern for note: ")
                edit_text = self.ui.get_input("Enter pattern for note: ")
                edit_note = self.notebook.find(edit_text, False)[0]
                self.notebook.delete(edit_note)
            elif note_action == "sort":
                self.notebook.sort_notes()
            elif note_action == "save":
                #file_name = input("File name: ")
                file_name = self.ui.get_input("File name: ")
                return self.notebook.save(file_name)
            elif note_action == "load":
                file_name = input("File name: ")
                return self.notebook.load(file_name)
            else:
                print("There is no such command for notes!")
            if note_action in ['add', 'delete', 'edit']:
                self.notebook.save("auto_save_notes")
        elif action == 'exit':
            pass
        else:
            print("There is no such command!")


def main():
    command = ""
    #bot = Bot()
    ui = ConsoleUserInterface()  # Використовуємо консольний інтерфейс
    bot = Bot(ui)  # Передаємо інтерфейс до бота
    bot.book.load("auto_save")
    bot.notebook.load("auto_save_notes")
    commands_help = ['Add', 'Search', 'Edit', 'Load', 'Remove', 'Save', 'Birthdays', 'View', 'Notes (add, find, edit, delete, sort, save)', 'Sorting', 'Exit']
    while True:
        #command = input("Enter your command or the command Help to see a list of commands: ").lower()
        command = ui.get_input("Enter your command or the command Help to see a list of commands: ").lower()
        if command == 'help':
        #     format_str = str('{:%s%d}' % ('^', 20))
        #     for command in commands_help:
        #         print(format_str.format(command))
        #     command = input().strip().lower()
        #     bot.handle(command)
        #     if command in ['add', 'remove', 'edit']:
        #         bot.book.save("auto_save")
        # else:
        #     bot.handle(command)
        #     if command in ['add', 'remove', 'edit']:
        #         bot.book.save("auto_save")
            ui.display_commands(commands_help)
            command = ui.get_input("Choose a command: ").strip().lower()
        bot.handle(command)
        if command in ['add', 'remove', 'edit']:
                bot.book.save("auto_save")
        if command == 'exit':
            print("Good bay")
            break


if __name__ == '__main__':
    main()

