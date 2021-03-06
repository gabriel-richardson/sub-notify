from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from time import sleep
import os
from twilio.rest import Client
import config as c
import pickle
from job import Job

def login():
    options = Options()
    options.headless = True
    browser = webdriver.Chrome(c.driver, chrome_options=options)
    browser.get(c.webpage)

    while True:
        try:
            username = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.ID, "Username")))
            password = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.ID, "Password")))
            submit = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.ID, "qa-button-login")))
            break
        except TimeoutException:
            print("Couldn't find login form, refreshing")
            browser.refresh()

    username.send_keys(c.username)
    password.send_keys(c.password)
    submit.click()
    print("Login successful")
    
    return browser

def get_jobs(browser):
    while True:
        try:
            jobTable = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.ID, "availableJobs")))
            break
        except TimeoutException:
            print("Couldn't find job table, refreshing")
            browser.refresh()
            login()

    jobs = jobTable.find_elements_by_class_name("job")
    new_jobs = {}
    for job in jobs:
        jobObj = Job(job)
        new_jobs[jobObj.get_id()] = jobObj
    return new_jobs

def compare_jobs(new_jobs):
    file = open("jobs_dict.txt", "rb")
    old_jobs = pickle.load(file)
    file.close()

    print("Fetching new jobs")
    
    for job in old_jobs.keys():
        if job not in new_jobs:
            old_jobs.pop(job)
    for job in new_jobs.keys():
        if job in old_jobs:
            new_jobs.pop(job)
        else:
            old_jobs.update({job:new_jobs[job]})

    file = open("jobs_dict.txt", "wb")
    pickle.dump(old_jobs, file)
    file.close()

    return new_jobs

def send_sms(jobs):
    account_sid = c.sid
    auth_token = c.auth

    client = Client(account_sid, auth_token)

    msg = "You have " + str(len(jobs)) + " new job(s) available:\n\n"

    for job in jobs:
        details = jobs[job].job_message()
        link = "https://sub.aesoponline.com/Substitute/Home"
        msg += details
    
    msg += "View here: " + link

    client.messages.create(
        to = {c.abby},
        from_ = c.twilio,
        body = msg
    )

    client.messages.create(
        to = {c.me},
        from_ = c.twilio,
        body = msg
    )

def main(refresh, br):
    if not refresh:
        browser = login()
    else:
        browser = br
        browser.refresh()
        print("Refreshing page")

    new_jobs = get_jobs(browser)
    new_jobs = compare_jobs(new_jobs)
    if len(new_jobs) != 0:
        send_sms(new_jobs)
        print("New jobs sent")
    else:
        print("No new jobs")
    print("Checking again in 15 minutes")
    time.sleep(900)
    main(True, browser)

if __name__ == "__main__":
    main(False, None)