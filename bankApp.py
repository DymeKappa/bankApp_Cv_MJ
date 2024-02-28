from usersData import UserData
import json

class BankApp:
    def __init__(self, user_data):
        self.user_data = user_data

    def checkSaldo(self, username):
        with open('database.json', 'r') as file:
            data = json.load(file)
            if username in data:
                saldo = data[username].get("saldo")
                print(f"Saldo użytkownika {username}: {saldo}")

    def deposit(self):
        amount = float(input("Podaj kwotę do wpłaty: "))
        if amount <= 0:
            print("Podano nieprawidłową kwotę.")
            return

        logged_user = self.user_data.logged_user
        if logged_user:
            with open('database.json', 'r+') as file:
                data = json.load(file)
                if logged_user in data:
                    data[logged_user]['saldo'] += amount
                    file.seek(0)
                    json.dump(data, file)
                    print(f"Wpłacono {amount} zł. Aktualne saldo: {data[logged_user]['saldo']} zł.")
        else:
            print("Błąd: Brak zalogowanego użytkownika.")

    def withdraw(self):
        amount = float(input("Podaj kwotę do wypłaty: "))
        if amount <= 0:
            print("Podano nieprawidłową kwotę.")
            return

        logged_user = self.user_data.logged_user
        if logged_user:
            with open('database.json', 'r+') as file:
                data = json.load(file)
                if logged_user in data:
                    saldo = data[logged_user]['saldo']
                    if amount > saldo:
                        print("Nie masz wystarczających środków na koncie.")
                        return
                    data[logged_user]['saldo'] -= amount
                    file.seek(0)
                    json.dump(data, file)
                    print(f"Wypłacono {amount} zł. Aktualne saldo: {data[logged_user]['saldo']} zł.")
        else:
            print("Błąd: Brak zalogowanego użytkownika.")


def runner():
    while True:
        user_data = UserData()  # Tworzenie instancji klasy UserData
        bank_app = BankApp(user_data)  # Tworzenie instancji klasy BankApp
        start = input("Wybierz: 1)Logowanie lub 2)Rejestracja lub q) Wyjście: ")
        if start == "1":
            user_data.login()
            if user_data.logged_user:
                while True:
                    action = input("Wybierz co chcesz zrobić: 1)Saldo, 2)Wpłać, 3)Wypłać lub q) Wyloguj: ")
                    if action == "1": # Wywołanie metody checkSaldo z nazwą użytkownika
                        bank_app.checkSaldo(user_data.logged_user)  
                    elif action == "2": # Wywołanie metody deposit
                        bank_app.deposit()
                    elif action == "3": # Wywołanie metody withdraw
                        bank_app.withdraw()
                    elif action == "q": # Wylogowanie
                        break
                    else:
                        print("Nieprawidłowy wybór.")
        elif start == "2":
            user_data.registration()
        elif start == "q":
            print("Dziękujemy za skorzystanie z naszego systemu bankowego. Do zobaczenia!")
            break
        else:
            print("Nieprawidłowy wybór.")




if __name__ == "__main__":
    runner()
