from selenium import webdriver
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def webScrap():
    url = "https://ec.europa.eu/research/mariecurieactions/jobs"

    driver = webdriver.Chrome('/Users/janjimenezserra/Documents/chromedriver')

    # Load the HTML page
    driver.get(url)
    time.sleep(2)

    # Parse processed webpage with BeautifulSoup
    page_soup = BeautifulSoup(driver.page_source, 'lxml')
    jobs_code = page_soup.find_all('div', class_=lambda value: value and value.startswith("jobOp views-row"))

    jobs = []
    for job_code in jobs_code:
        job_types = job_code.find_all('p', class_="jobField")
        fields = job_types[0].strong.text
        profile = job_types[1].strong.text

        if "Computer science" in fields and profile == "First Stage Researcher (R1)":
            jobs.append(job_code)

    driver.close()
    return jobs

def sendEmail(jobs):
    sendEmail = "jan.jime.serra@gmail.com"
    recEmail = "jan.jime.serra@gmail.com"
    password = input(str("Enter email password: "))

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Marie Curie PhD Positions."

    # Create the body of the message
    html = ""
    for job in jobs:
        html += job.prettify()

    # Record the MIME types of both parts - text/plain and text/html.
    body = MIMEText(html, 'html')
    msg.attach(body)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(sendEmail, password)
    print("Login successful!")
    server.sendmail(sendEmail, recEmail, msg.as_string())
    print("Email has been sent to ", recEmail)
    server.quit()

if __name__ == "__main__":
    jobs = webScrap()
    sendEmail(jobs)