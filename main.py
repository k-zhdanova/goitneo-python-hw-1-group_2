from assistant_app.main import main as run_assistant_app
from birthday_app.main import main as run_birthday_app

def main():
    try:
        print("Chose the app you want to run: \n (1) Birthdays app \n (2) Assistant app")
        action = input()
        if action == '1':
            run_birthday_app()
        elif action == '2':
            run_assistant_app()
        else:
            print('\033[91mI don\'t understand that command\033[0m')
    except KeyboardInterrupt:
        print("\nGood bye!")
        return

if __name__ == "__main__":
    main()