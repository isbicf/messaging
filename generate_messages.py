import random
import string
import time
import requests
from datetime import datetime


class Generator:
    @staticmethod
    def send_message():
        size = random.randint(2, 6)
        payload = {Generator.random_key(): Generator.random_value() for _ in range(size)}
        data = {'payload': payload}

        try:
            response = requests.post('http://localhost:5000/messages', json=data, timeout=5)
            print(f'Sent: {data} → {response.status_code}')
        except Exception as err:
            print(f'Error sending message: {err}')

    @staticmethod
    def random_key():
        length = random.randint(4, 10)
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

    @staticmethod
    def random_value():
        choice = random.choice(['string', 'int', 'float', 'bool', 'timestamp'])

        match choice:
            case 'string':
                return ''.join(random.choice(string.ascii_letters) for _ in range(6))
            case 'int':
                return random.randint(1, 1000)
            case 'float':
                return round(random.random() * 100, 2)
            case 'bool':
                return random.choice([True, False])
            case 'timestamp':
                return datetime.now().isoformat()


if __name__ == '__main__':
    print('Starting continuous message generator...')
    print('Press CTRL+C to stop.')

    while True:
        Generator.send_message()
        delay = random.uniform(1, 3)   # Random delay between 1 and 3 seconds
        time.sleep(delay)
