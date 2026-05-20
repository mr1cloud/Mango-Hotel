from art import tprint
from colorama import init, Fore, Style
import os
from core.mongo import MongoDB
from modules.staff import Staff

init(autoreset=True)

class HotelApp:
    def __init__(self):
        self.db    = None
        self.staff = None
        self.menu  = {
            "1": ("Staff Management", self._staff_menu),
            "0": ("Exit", None),
        }

    def connect(self):
        try:
            mongo = MongoDB("mongodb://localhost:27017")
            mongo.connect()
            self.db    = mongo.get_database("mango_hotel")
            self.staff = Staff(self.db)
            self.print("Database connected successfully!", color="GREEN")
        except Exception as e:
            self.print(f"Warning: Could not connect to MongoDB: {e}", color="YELLOW")

    @staticmethod
    def print(text, color=None):
        prefix = getattr(Fore, color, "") if color else ""
        print(prefix + text + Style.RESET_ALL, flush=True)

    @staticmethod
    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    def header(self):
        self.clear()
        tprint("Mango Hotel")

    def _staff_menu(self):
        if self.staff:
            self.staff.menu()
        else:
            self.print("Database connection failed. Staff management unavailable.", color="RED")

    def run(self):
        self.connect()
        self.header()
        self.print("Welcome! Use the menu below.")

        while True:
            print("\nMenu:")
            for key, (label, _) in self.menu.items():
                self.print(f"  {key}. {label}")
            
            choice = input("\nEnter your choice: ").strip()
            if choice not in self.menu:
                self.print("Invalid choice. Please try again.", color="RED")
                continue
            if choice == "0":
                self.print("Exiting the program. Goodbye!", color="GREEN")
                break

            _, action = self.menu[choice]
            if action:
                self.clear()
                action()
                self.header()


if __name__ == "__main__":
    HotelApp().run()