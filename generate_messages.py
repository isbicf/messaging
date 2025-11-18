import random
import string
import time
import requests
from datetime import datetime


API_URL = 'http://localhost:5000/messages'


def random_key():
    length = random.randint(4, 10)
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def random_value():
    types = ['string', 'int', 'float', 'bool', 'timestamp']

    choice = random.choice(types)

    if choice == 'string':
        return ''.join(random.choice(string.ascii_letters) for _ in range(6))

    if choice == 'int':
        return random.randint(1, 1000)

    if choice == 'float':
        return round(random.random() * 100, 2)

    if choice == 'bool':
        return random.choice([True, False])

    if choice == 'timestamp':
        return datetime.now().isoformat()


def generate_random_payload():
    size = random.randint(2, 6)   # number of keys
    return {random_key(): random_value() for _ in range(size)}


def send_message():
    payload = generate_random_payload()

    data = {'payload': payload}

    try:
        response = requests.post(API_URL, json=data, timeout=5)
        print(f'Sent: {data} → {response.status_code}')
    except Exception as err:
        print(f'Error sending message: {err}')


def main():
    print('Starting continuous message generator...')
    print('Press CTRL+C to stop.')

    while True:
        send_message()
        delay = random.uniform(1, 3)   # Random delay between 1 and 3 seconds
        time.sleep(delay)


if __name__ == '__main__':
    main()
