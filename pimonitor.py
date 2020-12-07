import random
import requests
import time

from bs4 import BeautifulSoup
from config import PRIVATE_NUMBER, TWILIO_NUMBER, TWILIO_ACCOUNT_SID, \
    TWILIO_AUTH_TOKEN, ETSY_ACCOUNT
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
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find_all(class_="wt-mr-md-2")[0].get_text()


def main():
    url = "https://www.etsy.com/uk/shop/" + ETSY_ACCOUNT
    sleeptime = 45
    counter = 1
    max_messages = 10
    message_count = 0
    expected_items = "0"

    while message_count < max_messages:
        current_items = check_website(url)
        current_time = time.strftime("%H:%M:%S", time.localtime())
        print("{} ({}): Currently Available: {}".format(
              current_time, counter, current_items))
        if current_items != expected_items:
            msg = "Now available: {}\n {}".format(current_items, url)
            send_message(msg, PRIVATE_NUMBER)
            expected_items = current_items
            message_count = message_count + 1
        time.sleep(sleeptime + random.randint(0, 9))
        counter = counter + 1
    send_message("Reset me", PRIVATE_NUMBER)


main()
