from helpers.main import format_error_msg, get_int_input
from collections import defaultdict
from datetime import datetime, timedelta
from faker import Faker
import json

fake = Faker()

def get_birthdays_per_week(json_filename):
  try:
    with open(json_filename, 'r') as file:
      users = json.load(file)
  except FileNotFoundError:
    print(format_error_msg("Could not find users.json. Please regenerate users."))
    input("Press enter to generate users")
    regenerate_users()
    get_birthdays_per_week(json_filename)
    return

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

def generate_users(n):
  datetime_start = datetime(1996, 10, 1) 
  datetime_end = datetime(1996, 12, 31) 
  users = [{
    "name": fake.name(), 
    "birthday": fake.date_time_between(start_date=datetime_start, end_date=datetime_end).isoformat()
    } for _ in range(n)]
  return users

def write_to_py_file(data, filename):
  with open(filename, 'w') as file:
    json.dump(data, file, indent=4)
    print(f'Wrote {len(data)} users to {filename}')

def regenerate_users():
  amount = get_int_input("How many users would you like to generate?\n")

  users = generate_users(amount)
  write_to_py_file(users, 'birthday_app/users.json')

def run_birthday_app():
  print("What would you like to do? \n (1) Regenerate users \n (2) Get next week's birthdays")
  action = input()

  if action == '1':
    regenerate_users()
  elif action == '2':
    get_birthdays_per_week('birthday_app/users.json')
  else:
    print(format_error_msg("I don't understand that command"))
