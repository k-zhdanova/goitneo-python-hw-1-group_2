from datetime import datetime
from faker import Faker
import json

fake = Faker()

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
