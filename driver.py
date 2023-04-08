'''
from selenium.webdriver.common.by import By
from google.oauth2.credentials import Credentials
from selenium.webdriver.support.ui import WebDriverWait
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from selenium.webdriver.support import expected_conditions as EC
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import openai
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from selenium.common.exceptions import NoSuchElementException
import os
import pickle
import time
import json

class LinkedInResumeGenerator:
    
    def __init__(self, credentials_file, prompt_file):
        with open(credentials_file, "r") as f:
            credentials = json.load(f)
        self.email = credentials['email']
        self.password = credentials['password']
        self.openai_api_key = credentials['openai_api_key']
        with open(prompt_file, "r") as f:
            self.prompt = f.read()
        self.job_container = []
        self.selected_jobs = []
        self.resumes = []
        
    def login_to_linkedin(self):
        # initialize the driver
        self.driver = webdriver.Chrome()

        # navigate to the LinkedIn login page
        self.driver.get("https://www.linkedin.com/login")

        # enter the email and password
        email_box = self.driver.find_element_by_id("username")
        email_box.send_keys(self.email)
        password_box = self.driver.find_element_by_id("password")
        password_box.send_keys(self.password)
        password_box.send_keys(Keys.RETURN)

        # wait for the login to complete
        time.sleep(3)
    def extract_job_titles(self, search_query):
        url = f"https://www.linkedin.com/jobs/search/?keywords={search_query}"
        self.driver.get(url)

        job_titles_container = self.driver.find_element_by_css_selector(".jobs-search-results-list")

        last_height = self.driver.execute_script("return arguments[0].scrollHeight", job_titles_container)
        while True:
            self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", job_titles_container)
            time.sleep(1)
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", job_titles_container)
            if new_height == last_height:
                break
            last_height = new_height

        job_cards = self.driver.find_elements_by_css_selector(".job-card-container--clickable")

        # Collect all the job titles and links in a list
        jobs_list = []
        for job_card in job_cards:
            title_element = job_card.find_element_by_css_selector(".job-card-container__link.job-card-list__title")
            title = title_element.text
            all_links = job_card.find_elements_by_css_selector("a")
            link = ""
            for a_link in all_links:
                if title in a_link.text:
                    link = a_link.get_attribute("href")
                    break
            jobs_list.append((title, link))

        # Navigate to each link and extract the additional information
        for title, link in jobs_list:
            self.driver.get(link)
            time.sleep(1)

            company_name_element = self.driver.find_element_by_css_selector(".jobs-unified-top-card__company-name a")
            company = company_name_element.text

            location_element = self.driver.find_element_by_css_selector(".jobs-unified-top-card__bullet")
            location = location_element.text

            try:
                workplace_type_element = self.driver.find_element_by_css_selector(".jobs-unified-top-card__workplace-type")
                workplace_type = workplace_type_element.text
            except NoSuchElementException:
                workplace_type = "None"

            try:
                see_more_button = self.driver.find_element_by_css_selector("button[aria-label='Click to see more description']")
                see_more_button.click()
                time.sleep(1)
            except NoSuchElementException:
                pass

            try:
                job_description_element = self.driver.find_element_by_css_selector("#job-details")
                job_description = job_description_element.text
            except NoSuchElementException:
                job_description = "None"

            self.job_container.append({"title": title, "location": location, "company": company, "link": link, "description": job_description, "workplace_type": workplace_type})

        # Navigate back to the job search page
        self.driver.get(url)




    def select_jobs(self):
        # let the user select the jobs to generate resumes for
        for i, job in enumerate(self.job_container):
            print(f"{i+1}. {job['title']} at {job['company']}")
            selected = input("Generate resume for this job? (y/n) ")
            if selected == "y":
                self.selected_jobs.append(job)
    
    def generate_resumes(self):
        # authenticate with the OpenAI API
        openai.api_key = self.openai_api_key
        # generate resumes for the selected jobs
        for job in self.selected_jobs:
            job_description = job['description']
            prompt_with_description = f"{self.prompt}\nJob Ad:\n{job_description}"
            
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_with_description},
            ]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            resume = response['choices'][0]['message']['content'].strip()
            self.resumes.append({"company": job["company"], "workplace_type": job["workplace_type"], "resume": resume})
    
    def write_to_drive(self):
        # authenticate with Google Drive
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            with open('GDriveAuthentication.json', 'r') as f:
                client_config = json.load(f)

            flow = InstalledAppFlow.from_client_config(client_config, scopes=['https://www.googleapis.com/auth/drive.file'])
            creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        # create a new folder in Google Drive for the resumes
        service = build('drive', 'v3', credentials=creds)
        folder_metadata = {'name': 'Resumes', 'mimeType': 'application/vnd.google-apps.folder'}
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder.get('id')

        # write each resume to a new file in the folder
        for resume in self.resumes:
            # Search for the company folder
            query = f"mimeType='application/vnd.google-apps.folder' and trashed = false and parents in '{folder_id}' and name='{resume['company']}'"
            response = service.files().list(q=query, spaces='drive', fields='nextPageToken, files(id, name)').execute()
            files = response.get('files', [])

            if not files:
                # Create the company folder if it doesn't exist
                company_folder_metadata = {'name': resume['company'], 'parents': [folder_id], 'mimeType': 'application/vnd.google-apps.folder'}
                company_folder = service.files().create(body=company_folder_metadata, fields='id').execute()
                company_folder_id = company_folder.get('id')
            else:
                # Get the existing company folder ID
                company_folder_id = files[0].get('id')

            # Create the Google Docs file and write content
            file_metadata = {'name': 'Sina Naeemi', 'parents': [company_folder_id], 'mimeType': 'application/vnd.google-apps.document'}
            doc = service.files().create(body=file_metadata).execute()

            # Write content to the created Google Docs file
            docs_service = build('docs', 'v1', credentials=creds)
            requests = [
                {
                    'insertText': {
                        'location': {
                            'index': 1
                        },
                        'text': resume['resume']
                    }
                }
            ]
            docs_service.documents().batchUpdate(documentId=doc['id'], body={'requests': requests}).execute()
            print(f"Resume for {resume['company']} written to file {doc.get('id')} in folder {company_folder_id}")

            # TODO: Add formatting to the document, such as bolding certain text, changing the font, adding bullet points, etc.
            # TODO: Use the Google Drive API to modify the document and apply formatting.

if __name__ == '__main__':
    
    # create an instance of the LinkedInResumeGenerator class
    generator = LinkedInResumeGenerator("credentials.json", "prompt")

    # login to LinkedIn
    generator.login_to_linkedin()

    # extract job titles
    generator.extract_job_titles('Software Engineer')

    # let user select jobs to generate resumes for
    generator.select_jobs()

    # generate resumes for selected jobs
    generator.generate_resumes()

    # write resumes to Google Drive
    generator.write_to_drive()