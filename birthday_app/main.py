from collections import defaultdict
from datetime import datetime, timedelta
from faker import Faker
import json 
from json.decoder import JSONDecodeError

fake = Faker()

def get_next_week_birthdays(json_filename):
    users = get_users(json_filename)
    if not users:
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

    show_birthdays(birthdays)

def show_birthdays(birthdays):
    print("\n" + format_bold_msg("Next week's birthdays:"))

    for day, names in birthdays.items():
        print(f"{format_underline_msg(day)}: {', '.join(names)}")

def get_users(json_filename):
    try:
        with open(json_filename, 'r') as file:
            users = json.load(file)
            if not users:
                raise FileNotFoundError
            return users
    except FileNotFoundError:
        regenerate_users(json_filename)
    except JSONDecodeError:
        regenerate_users(json_filename)

    return
  
def regenerate_users(json_filename):
    print(format_error_msg("Could not find users.json. Please regenerate users."))
    while True:
        action = input("Would you like to regenerate users? (y/n)\n")
        if action == 'y':
            generate_users()
            get_next_week_birthdays(json_filename)
            return
        elif action == 'n':
            print(format_error_msg("Good bye!"))
            break
        else:
            print(format_error_msg("I don't understand that command"))

def generate_users():
    amount = get_int_input("How many users would you like to generate?\n")

    users = datetime_start = datetime(1996, 10, 1) 
    datetime_end = datetime(1996, 12, 31) 
    users = [{
    "name": fake.name(), 
    "birthday": fake.date_time_between(start_date=datetime_start, end_date=datetime_end).isoformat()
    } for _ in range(amount)]

    write_to_json_file(users, 'birthday_app/users.json')

def write_to_json_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
        print(f'Wrote {len(data)} users to {filename}')

def format_error_msg(msg):
    return "\033[91m" + msg + "\033[0m"

def format_bold_msg(msg):
    return "\033[1m" + msg + "\033[0m"

def format_underline_msg(msg):
    return "\033[4m" + msg + "\033[0m"

def get_int_input(prompt, error_msg="Please enter a valid number"):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print(format_error_msg(error_msg))

def main():
    try:
        action = input("What would you like to do? \n (1) Regenerate users \n (2) Get next week's birthdays \n")
        if action == '1':
            generate_users()
        elif action == '2':
            get_next_week_birthdays('birthday_app/users.json')
        else:
            print(format_error_msg("I don't understand that command"))
    except KeyboardInterrupt:
        print("\nGood bye!")
        return

if __name__ == "__main__":
    main()