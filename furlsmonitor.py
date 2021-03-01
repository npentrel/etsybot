import random
import requests
import time
import json

from config import PRIVATE_NUMBER, TWILIO_NUMBER, TWILIO_ACCOUNT_SID, \
    TWILIO_AUTH_TOKEN
from twilio.rest import Client


class ListValueException(Exception):
    pass


def send_message(msg, number):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages \
                    .create(
                         body=msg,
                         from_=TWILIO_NUMBER,
                         to=PRIVATE_NUMBER
                     )
    print(message.sid)


def check_website(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95'
               'Safari/537.36'}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)

    for item in data['product']['variants']:
        if (item['title'] == 'Purpleheart: Size D - 3.25mm'):
            return item['inventory_quantity']
    raise ListValueException("Purpleheart 3.25 not in list")


def main():
    url = "https://furlscrochet.com/products/alpha-series-wood-crochet-hook.json"
    sleeptime = 45
    counter = 1
    max_messages = 10
    message_count = 0
    expected_inventory = -1

    while message_count < max_messages:
        current_inventory = check_website(url)
        current_time = time.strftime("%H:%M:%S", time.localtime())
        print("{} ({}): Currently Available: {}".format(
              current_time, counter, current_inventory))
        if current_inventory != expected_inventory:
            msg = "Now available: {}\n {}".format(current_inventory, url)
            send_message(msg, PRIVATE_NUMBER)
            expected_inventory = current_inventory
            message_count = message_count + 1
        time.sleep(sleeptime + random.randint(0, 9))
        counter = counter + 1
    send_message("Reset me", PRIVATE_NUMBER)


try:
    main()
except ListValueException as e:
    send_message("Furls: ListValueException")
except KeyboardInterrupt:
    print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
except:
    send_message("Error", PRIVATE_NUMBER)
    raise
