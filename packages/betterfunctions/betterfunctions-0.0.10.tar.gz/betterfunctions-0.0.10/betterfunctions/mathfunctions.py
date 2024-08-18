import math

## Mathematische Funktionen


def format_number(number: int, *, decimal_places: int = 1, trailing_zero: bool = False) -> str:
    """Formatiere eine große Nummer zu einem kleinen Format.

    Parameters
    ----------
    number:
        Die zu formatierende Nummer.
    decimal_places:
        Die Anzahl der Dezimalstellen, welche dargestellt werden sollen. Default: ``1``.
    trailing_zero:
        Soll eine Trailing Zero dargestellt werden? Default: ``False``.

    Returns
    -------
    :class:`str`
        Die formatierte Zahl.

    """

    suffix = ""
    if number >= 1_000_000_000 or number <= -1_000_000_000:
        txt = f"{number / 1_000_000_000:.{decimal_places}f}"
        suffix = "B"
    elif number >= 1_000_000 or number <= -1_000_000:
        txt = f"{number / 1_000_000:.{decimal_places}f}"
        suffix = "M"
    elif number >= 100 or number <= -100:
        txt = f"{number / 1_000:.{decimal_places}f}"
        suffix = "K"
    else:
        txt = str(number)

    if not trailing_zero:
        txt = txt.rstrip("0").rstrip(".")

    return txt + suffix

def fibonacci(n: int):
    """Generiert eine Liste der Fibonacci-Zahlen bis n.

    Parameters
    ----------
    n:
        Die Zahl, bis zu welcher Fibonaccis generiert werden sollen.

    """
    fib_sequence = [0, 1]
    while fib_sequence[-1] + fib_sequence[-2] <= n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence


def is_prime(num: int):
    """Überprüft, ob eine Zahl prim ist.

    Parameters
    ----------
    num:
        Die Zahl, welche überprüft werden soll.

    """
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True


def prime_numbers(n: int):
    """Generiert eine Liste der Primzahlen bis n.

    Parameters
    ----------
    n:
        Die Zahl, bis zu welcher Primzahlen generiert werden sollen.

    """
    return [x for x in range(2, n + 1) if is_prime(x)]


def gcd(a: int, b: int):
    """Berechnet den größten gemeinsamen Teiler zweier Zahlen.

    Parameters
    ----------
    a:
        Die erste Zahl.
    b:
        Die zweite Zahl.

    """
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b:int):
    """Berechnet das kleinste gemeinsame Vielfache zweier Zahlen.

    Parameters
    ----------
    a:
        Die erste Zahl.
    b:
        Die zweite Zahl

    """
    return abs(a*b) // gcd(a, b)


def factorial(n: str):
    """Berechnet die Fakultät einer Zahl.

    Parameters
    ----------
    n:
        Die Zahl, welche als Basis dient.

    """
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)


def celsius_to_fahrenheit(celsius: float):
    """Konvertiert Celsius in Fahrenheit.

    Parameters
    ----------
    celsius:
        Die Temperatur in Celsius, welche umgewandelt werden soll.

    """
    return (celsius * 9/5) + 32


def fahrenheit_to_celsius(fahrenheit: float):
    """Konvertiert Fahrenheit in Celsius.

    Parameters
    ----------
    fahrenheit:
        Die Temperatur in Fahrenheit welche konvertiert werden soll.

    """
    return (fahrenheit - 32) * 5/9


def int_to_roman(num: str):
    """Konvertiert eine ganze Zahl in römische Ziffern.

    Parameters
    ----------
    num:
        Die Nummer welche umgewandelt werden soll.

    """
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    syms = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syms[i]
            num -= val[i]
        i += 1
    return roman_num


def distance_between_points(x1: float, y1: float, x2: float, y2: float):
    """Berechnet die Entfernung zwischen zwei Punkten.

    Parameters
    ----------
    x1:
        Die x-Koordinate des ersten Punkts
    x2:
        Die x-Koordinate des zweiten Punkts
    y1:
        Die y-Koordinate des ersten Punkts
    y2:
        Die y-Koordinate des zweiten Punkts


    """
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
