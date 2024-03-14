import json
import os


class UserData:
    def __init__(self):
        self.users = {}  # Słownik przechowujący dane użytkowników
        self.logged_user = None  # Zmienna przechowująca nazwę zalogowanego użytkownika
        self.load_from_json()

    def registration(self):
        while True:
            username = input("Podaj nazwę użytkownika (minimum 5 znaków): ").capitalize()
            if len(username) < 5:
                print("Nazwa użytkownika musi zawierać przynajmniej 5 znaków.")
                continue
            elif username in self.users:
                print("Użytkownik już istnieje. Proszę wybrać inną nazwę.")
                continue

            while True:
                password = input(
                    "Podaj hasło (minimum 8 znaków, co najmniej 1 duża litera, 1 znak specjalny i 1 cyfra): ")
                if not self.validate_password(password):
                    print("Hasło nie spełnia wymagań. Spróbuj ponownie.")
                    continue
                else:
                    break  # Przerwij pętlę, jeśli hasło jest poprawne

            saldo = 0  # Domyślne saldo dla nowego użytkownika
            self.users[username] = {"password": password, "saldo": saldo}
            self.save_to_json()
            print("Rejestracja zakończona pomyślnie.")
            return True

    def validate_password(self, password):
        if len(password) < 8:
            return False
        if not any(char.isupper() for char in password):
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char in "!@#$%^&*()-_+=[]" for char in password):
            return False
        return True

    def login(self):
        while True:
            username = input("Podaj nazwę użytkownika: ").capitalize()
            password = input("Podaj hasło: ")
            if username in self.users and self.users[username]["password"] == password:
                self.logged_user = username  # Ustawienie nazwy zalogowanego użytkownika
                print("Zalogowano pomyślnie.")
                return True
            else:
                print("Nieprawidłowe dane logowania")
                while True:
                    choice = input("Czy chcesz spróbować ponownie? (Tak/Nie): ").lower()
                    if choice == "nie":
                        register_choice = input("Czy chcesz zarejestrować nowe konto? (Tak/Nie): ").lower()
                        if register_choice == "tak":
                            self.registration()
                        elif register_choice == "nie":
                            print("Do widzenia!")
                            return False
                        else:
                            print("Niepoprawna odpowiedź. Spróbuj ponownie.")
                    elif choice == "tak":
                        break
                    else:
                        print("Nieprawidłowa odpowiedź. Spróbuj ponownie.")

    def load_from_json(self):
        if os.path.exists('database.json') and os.path.getsize('database.json') > 0:
            with open('database.json', 'r') as file:
                self.users = json.load(file)

    def save_to_json(self):
        with open('database.json', 'w') as file:
            json.dump(self.users, file)


