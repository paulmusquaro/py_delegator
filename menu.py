import importlib
# from 
# from
# from
from calend import calend_main
# from
# from 

class Menu:
    def __init__(self):
        self.choices = {
            1: ("calend", "calend_main"),
            2: ("adressbook", "adressbook_main"),
            3: ("notebook", "notebook_main"),
            4: ("filesorter", "filesorter_main"),
            5: ("nth", "nth_main")
        }

    def make_decision(self, choice):
        module_name, function_name = self.choices.get(choice)
        
        if not module_name:
            return

        try:
            module = importlib.import_module(module_name)
            function = getattr(module, function_name)
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
    print("5. Nth Program")
    print("6. Exit")

    menu = Menu()

    while True:
        try:
            choice = int(input("Enter your choice (1-6): "))
            if choice == 6:
                break
            menu.make_decision(choice)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()