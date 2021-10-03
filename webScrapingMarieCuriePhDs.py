from selenium import webdriver
from bs4 import BeautifulSoup
import time

class Job:
    def __init__(self, title, fields, profile):
        self.title = title
        self.fields = fields
        self.profile = profile
    
    def toString(self):
        return ("Job Title: "+self.title+"\n"+
            "Fields: "+self.fields+"\n"+
            "Profile: "+self.profile+"\n"+
            "----------------------\n"
        )


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
        job_title = job_code.find('h3').text
        job_types = job_code.find_all('p', class_="jobField")
        fields = job_types[0].strong.text
        profile = job_types[1].strong.text

        if "Computer science" in fields and profile == "First Stage Researcher (R1)":
            new_job = Job(job_title, fields, profile)
            jobs.append(new_job)


    for job in jobs:
        print(job.toString())   

    driver.close()


if __name__ == "__main__":
    webScrap()