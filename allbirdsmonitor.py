import random
import requests
import time
import json

from config import PRIVATE_NUMBER, TWILIO_NUMBER, TWILIO_ACCOUNT_SID, \
    TWILIO_AUTH_TOKEN
from twilio.rest import Client


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

    return data['products']['womens-wool-lounger-fluffs-natural-white']['sizes']['uk-6']['available']


def main():
    url = "https://www.allbirds.co.uk/collections/womens-wool-lounger-fluffs?view=master-product"
    sleeptime = 45
    counter = 1
    max_messages = 10
    message_count = 0
    expected_status = False

    while message_count < max_messages:
        current_status = check_website(url)
        current_time = time.strftime("%H:%M:%S", time.localtime())
        print("{} ({}): Currently Available: {}".format(
              current_time, counter, current_status))
        if current_status != expected_status:
            msg = "Now available: {}\n {}".format(current_status, url)
            send_message(msg, PRIVATE_NUMBER)
            expected_status = current_status
            message_count = message_count + 1
        time.sleep(sleeptime + random.randint(0, 9))
        counter = counter + 1
    send_message("Reset me", PRIVATE_NUMBER)


try:
    main()
except:
    send_message("Error", PRIVATE_NUMBER)
    raise
