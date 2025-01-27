from multipledispatch import dispatch
import math

class Figura(object):
    def __init__(self):
        print("Figura init")

class Prostokat(Figura):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        # dokoncz definicje

class Kwadrat(Prostokat):
    def __init__(self, x: int):
        self.x = x
        # dokoncz definicje

class Kolo(Figura):
    def __init__(self, r: float):
        self.r = r
        # dokoncz definicje

# Funkcje pole
@dispatch(Figura)
def pole(instance: Figura):
    print("Pole: Figura")
    return 0

# Napisz wersje 'pole' dla:
# - Prostokat (bez podania argumentów boków)
@dispatch(Prostokat)
def pole(instance: Prostokat):
    print("Pole: Prostokat")
    return instance.x*instance.y
# - Prostokat (z podaniem argumentów boków jako int, int)
@dispatch(Prostokat, int, int)
def pole(instance: Prostokat, x, y):
    print("Pole: Prostokat ze zmiana wymiarow")
    instance.x = x
    instance.y = y
    return instance.x*instance.y
# - Kwadrat (bez podania argumentów boku)
@dispatch(Kwadrat)
def pole(instance: Kwadrat):
    print("Pole: Kwadrat")
    return instance.x*instance.x
# - Kwadrat (z podaniem argumentów boku jako int)
@dispatch(Kwadrat,int)
def pole(instance: Kwadrat, x:int):
    print("Pole: Kwadrat ze zmiana wymiarow")
    instance.x = x
    return instance.x*instance.x
# - Kolo (bez podania argumentów promienia)
@dispatch(Kolo)
def pole(instance: Kolo):
    print("Pole: Kolo")
    return math.pi*(instance.r**2)
# - Kolo (z podaniem argumentów promienia jako float)
@dispatch(Kolo, float)
def pole(instance: Kolo, r: float):
    print("Pole: Kolo ze zmiana wymiarow")
    instance.r = r
    return math.pi*(instance.r**2)
# Uzywaj print() do weryfikacji wywolan





# Polimorfizm w czasie wykonywania
def polaPowierzchni(listaFigur):
    for i in listaFigur:
        print(f"Pole obiektu: {pole(i)}")

if __name__ == "__main__":
    # Tworzenie obiektów
    print("=== Tworzenie obiektów ===")
    a, b, c, d = Figura(), Prostokat(2, 4), Kwadrat(2), Kolo(3)

    # Wywołania funkcji pole
    print("\n=== Wywołania funkcji pole ===")
    print(f"Pole prostokąta (2x4): {pole(b)}")
    print(f"Pole kwadratu (bok=2): {pole(c)}")
    print(f"Pole koła (r=3): {pole(d)}")

    # Zmiana wymiarów za pomocą funkcji pole
    print("\n=== Zmiana wymiarów ===")
    print(f"Pole prostokąta po zmianie na 5x6: {pole(b, 5, 6)}")
    print(f"Pole kwadratu po zmianie boku na 7: {pole(c, 7)}")
    print(f"Pole koła po zmianie promienia na 4: {pole(d, 4.0)}")

    # Polimorfizm
    print("\n=== Polimorfizm w czasie wykonywania ===")
    polaPowierzchni([a, b, c, d])
