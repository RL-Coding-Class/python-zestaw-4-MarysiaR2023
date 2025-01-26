from functools import singledispatch, singledispatchmethod

# Singledispatch: globalna funkcja do logowania zdarzeń
@singledispatch
def log_event(event):
    raise NotImplementedError(f"Brak implementacji dla typu: {type(event)}")

# Napisz obsluge zdarzen str
@log_event.register
def _(arg: str, verbose=False):
    if verbose:
        print("Handling strings?", end = "")
    print(arg)

# Napisz obsluge zdarzen int
@log_event.register
def _(arg: int, verbose=False):
    if verbose:
        print("Strength in numbers, eh?", end=" ")
    print(arg)

# Napisz obsluge zdarzen typu dict
@log_event.register
def _(arg: dict, verbose=False):
    if verbose:
        print("Enumerate this:")
    for i, (key, value) in enumerate(arg.items()):
        print(key+":" , value)


# Klasa z metodą używającą singledispatchmethod
class EventHandler:
    def __init__(self):
        self.event_count = 0 # uwaga: licznik powiekszac o +1 przy kazdej rejestracji

    @singledispatchmethod
    def handle_event(self, event):
        """Domyślna obsługa zdarzeń"""
        raise NotImplementedError(f"Nieobsługiwany typ zdarzenia: {type(event)}")

    # Napisz obsluge zdarzen str, pamietaj: self.event_count += 1
    @handle_event.register
    def _(self,arg: str):
        print("handling string: ", arg)
        self.event_count = self.event_count+1

    # Napisz obsluge zdarzen int
    @handle_event.register
    def _(self,arg: int):
        print("handling integer: ", arg)
        self.event_count = self.event_count+1

    # Napisz obsluge zdarzen list
    @handle_event.register
    def _(self,arg: list):
        print("handling integer:", end = " ")
        for i, elem in enumerate(arg):
            print(elem, end=" ")
        self.event_count = self.event_count+1


# Klasa pochodna z nowymi rejestracjami typów
class DerivedHandler(EventHandler):

    # Napisz obsluge zdarzen int
    @EventHandler.handle_event.register
    def _(self,arg: int):
        print("handling integer from derived class: ", arg)
        self.event_count = self.event_count+1

    # Napisz obsluge zdarzen float
    @EventHandler.handle_event.register
    def _(self,arg: float):
        print("handling float: ", arg)
        self.event_count = self.event_count+1


# Demonstracja użycia
if __name__ == "__main__":
    # Globalna funkcja logowania zdarzeń
    print("=== Globalne logowanie zdarzeń ===")
    log_event("Uruchomienie systemu")
    log_event(404)
    log_event({"typ": "error", "opis": "Nieznany błąd"})

    # Klasa obsługująca zdarzenia
    print("\n=== Klasa EventHandler ===")
    handler = EventHandler()
    handler.handle_event("Zdarzenie logowania")
    handler.handle_event(123)
    handler.handle_event(["zdarzenie1", "zdarzenie2", "zdarzenie3"])

    # Obsługa nieobsługiwanego typu
    print("\n=== Obsługa nieobsługiwanego typu ===")
    try:
        log_event(3.14)  # Nieobsługiwany typ w log_event
    except NotImplementedError as e:
        print(e)

    try:
        handler.handle_event(set([1, 2, 3]))  # Nieobsługiwany typ w handle_event
    except NotImplementedError as e:
        print(e)

    # Klasa DerivedHandler
    print("\n=== Klasa DerivedHandler ===")
    derived_handler = DerivedHandler()
    derived_handler.handle_event("Inne zdarzenie tekstowe")
    derived_handler.handle_event(789)  # Obsługa zmieniona dla int
    derived_handler.handle_event(3.14)  # Obsługa float zarejestrowana w DerivedHandler

    # Niespodzianka: prosze sprawdzic co zobaczymy?
    handler.handle_event(12356789)
