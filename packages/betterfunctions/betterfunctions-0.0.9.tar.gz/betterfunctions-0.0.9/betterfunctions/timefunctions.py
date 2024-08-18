import datetime

## Zeit Funktionen



def current_date():
    """Gibt das aktuelle Datum zurück."""
    return datetime.date.today().strftime("%d.%m.%Y")


def current_time():
    """Gibt die aktuelle Uhrzeit zurück."""
    return datetime.datetime.now().strftime("%H:%M:%S")


def is_leap_year(year):
    """Überprüft, ob ein Jahr ein Schaltjahr ist."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
