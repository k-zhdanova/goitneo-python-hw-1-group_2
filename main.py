from helpers.generate_users import generate_users, write_to_py_file
from collections import defaultdict
from datetime import datetime, timedelta
import json

def get_birthdays_per_week(json_filename):
    with open(json_filename, 'r') as file:
        users = json.load(file)

    today = datetime.today().date()
    start_of_next_week = today + timedelta(days=7 - today.weekday())
    end_of_next_week = start_of_next_week + timedelta(days=4)

    birthdays = defaultdict(list)

    for user in users:
        birthday = datetime.fromisoformat(user['birthday']).date()
        birthday_this_year = birthday.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        day_of_week = birthday_this_year.weekday()

        if birthday_this_year >= start_of_next_week - timedelta(days=2) and birthday_this_year < start_of_next_week:
            birthdays['Monday'].append(user['name'])
        elif start_of_next_week <= birthday_this_year <= end_of_next_week and day_of_week < 5:
            day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'][day_of_week]
            birthdays[day_name].append(user['name'])

    for day, names in birthdays.items():
        print(f"{day}: {', '.join(names)}")

def regenerate_users(amount=100):
  users = generate_users(amount)
  write_to_py_file(users, 'constants/users.json')

def format_error_msg(msg):
  return "\033[91m" + msg + "\033[0m"

def main():
  def get_int_input(prompt, error_msg="Please enter a valid number"):
    while True:
      try:
        return int(input(prompt))
      except ValueError:
        print(format_error_msg(error_msg))

  print("What would you like to do? \n (1) Regenerate users \n (2) Get birthdays this week")
  action = input()

  if action == '1':
    amount = get_int_input("How many users would you like to generate?\n")
    regenerate_users(amount)
  elif action == '2':
    get_birthdays_per_week('constants/users.json')
  else:
    print(format_error_msg("I don't understand that command"))

if __name__ == "__main__":
  main()