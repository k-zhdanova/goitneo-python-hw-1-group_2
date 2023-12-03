from helpers.main import format_error_msg
from assistant_app.main import run_assistant_app
from birthday_app.main import run_birthday_app

def main():
  print("Chose the app you want to run: \n (1) Birthdays app \n (2) Assistant app")
  action = input()

  if action == '1':
    run_birthday_app()
  elif action == '2':
    run_assistant_app()
  else:
    print(format_error_msg("I don't understand that command"))

if __name__ == "__main__":
  main()