from art import tprint
from colorama import init, Fore, Style
import os

init(autoreset=True)

menu = {
    "0": ("Exit", None),
}

def console_print(text, color=None):
    prefix = getattr(Fore, color, '') if color else ''
    reset = Style.RESET_ALL if color else ''
    print(prefix + text + reset, flush=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    tprint("Mango Hotel")
    console_print("Welcome! Use the menu below.")
    while True:
        print("\nMenu:")
        for key, (description, _) in menu.items():
            console_print(f"{key}. {description}")
        choice = input("\nEnter your choice: ")
        if choice in menu:
            if choice == "0":
                console_print("Exiting the program. Goodbye!", color='GREEN')
                break
            else:
                _, action = menu[choice]
                if action:
                    action()
                    clear_screen()
                    tprint("Mango Hotel")
        else:
            console_print("Invalid choice. Please try again.", color='RED')

if __name__ == "__main__":
    main()