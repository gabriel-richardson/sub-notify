from selenium import webdriver
import time
from time import sleep
import os
from twilio.rest import Client
import config as c

def login():
    browser = webdriver.Chrome(c.driver)
    browser.get(c.webpage)
    time.sleep(2)

    username = browser.find_element_by_id("Username")
    username.send_keys(c.username)
    password = browser.find_element_by_id("Password")
    password.send_keys(c.password)
    submit = browser.find_element_by_id("qa-button-login")
    submit.click()
    time.sleep(8)
    html_source = browser.page_source
    print(html_source)

def send_sms():
    account_sid = c.sid
    auth_token = c.auth

    client = Client(account_sid, auth_token)

    client.messages.create(
        to = c.me,
        from_ = c.twilio,
        body = "Hello, world!"
    )

def main():
    send_sms()

if __name__ == "__main__":
    main()