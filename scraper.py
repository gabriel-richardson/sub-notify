from selenium import webdriver
import time
from time import sleep
import os
from twilio.rest import Client
import config as c
import pickle

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
    
    time.sleep(10)
    return browser

def get_jobs(browser):
    jobs = browser.find_element_by_id("availableJobs").find_elements_by_class_name("job")
    new_jobs = {}
    for job in jobs:
        new_jobs[job.get_attribute("id")] = job
    return new_jobs

def compare_jobs(new_jobs):
    file = open("jobs_dict.txt", "rb")
    old_jobs = pickle.load(file)

    for job in old_jobs:
        print(job)
        if job not in new_jobs:
            old_jobs.pop(job)
    for job in new_jobs:
        print("\n--\n")
        print(job)
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

    for job in jobs:
        details = job_details(jobs[job])
        msg = "You have " + len(jobs) + " new job(s) available:\n" + details

    client.messages.create(
        to = c.me,
        from_ = c.twilio,
        body = msg
    )

def job_details(job):
    name = job.find_element_by_class_name("name").text
    title = job.find_element_by_class_name("title").text
    date = job.find_element_by_class_name("itemDate").text
    start = job.find_element_by_class_name("startTime").text
    end = job.find_element_by_class_name("endTime").text
    location = job.find_element_by_class_name("locationName").text
    return name + "\n" + title + "\nFrom " + start + " to " + end + " on " + date + " at " + location

def main():
    browser = login()
    new_jobs = get_jobs(browser)
    new_jobs = compare_jobs(new_jobs)
    if len(new_jobs) != 0:
      send_sms(new_jobs)

if __name__ == "__main__":
    main()