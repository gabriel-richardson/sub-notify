import selenium
from selenium import webdriver
import time
from time import sleep
import config as c

def login():
    browser = webdriver.Chrome(c.driver)
    browser.get(c.webpage)
    time.sleep(2)

    username = browser.find_element_by_id('Username')
    username.send_keys(c.username)
    password = browser.find_element_by_id('Password')
    password.send_keys(c.password)
    submit = browser.find_element_by_id('qa-button-login')
    submit.click()

def main():
    login()

if __name__ == '__main__':
    main()