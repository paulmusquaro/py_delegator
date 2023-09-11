import importlib
import os
from calend import calend_main
from Addressbook import start
from notebook.nb_main import NoteManager
from file_sorter import start
from exchanger import ex_main


class Menu:
    def __init__(self):
        self.choices = {
            1: ("calend", "calend_main"),
            2: ("Addressbook", "start"),
            3: ("notebook.nb_main", "nb_main"),
            4: ("file_sorter", "start"),
            5: ("exchanger", "ex_main")
        }

    def make_decision(self, choice):
        module_name, function_name = self.choices.get(choice)
        
        if not module_name:
            return
        
        if choice == 3:
            note_folder = "notebook/notes"
            note_manager = NoteManager(note_folder)
            note_manager.nb_main()
            return True

        try:

            if choice == 4:
                directory_path = input("Enter the path to directory: ")
                if os.path.exists(directory_path) and os.path.isdir(directory_path):
                    function = getattr(importlib.import_module(module_name), function_name)
                    function(directory_path)
                else:
                    print("Invalid directory path. Please enter a valid directory path.")
            else:
                function = getattr(importlib.import_module(module_name), function_name)
                function()
        except ModuleNotFoundError:
            print("Module not found.")
        except AttributeError:
            print("Function not found in the module.")

def main():
    print("Choose an option:")
    print("1. Calendar")
    print("2. Address Book")
    print("3. Notebook")
    print("4. File Sorter")
    print("5. Exchanger")
    print("6. Exit")

    menu = Menu()
    option_3_called = False

    while True:
        try:
            choice = int(input("Enter your choice (1-6): "))
            if choice == 6:
                break
            if not option_3_called or (option_3_called and choice != 4):
                option_3_called = menu.make_decision(choice)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
