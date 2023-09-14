import calendar

class Calendar:
    def __init__(self, year, month):
        self.year = year
        self.month = month

    def show_calendar(self):
        if self.month < 1 or self.month > 12:
            print("The month is entered incorrectly.")
        else:
            cal = calendar.month(self.year, self.month)
            print("\n", cal)

def calend_main():
    year = int(input("Enter the year:"))
    month = int(input("Enter the month (1-12):"))
    
    my_calendar = Calendar(year, month)
    my_calendar.show_calendar()