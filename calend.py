import calendar

class Calendar:
    def __init__(self, year, month):
        self.year = year
        self.month = month

    def show_calendar(self):
        if self.month < 1 or self.month > 12:
            print("Неправильно введено місяць.")
        else:
            cal = calendar.month(self.year, self.month)
            print("\n", cal)

def calend_main():
    year = int(input("Введіть рік: "))
    month = int(input("Введіть місяць (1-12): "))
    
    my_calendar = Calendar(year, month)
    my_calendar.show_calendar()