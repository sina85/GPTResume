# LinkedIn Resume Generator

LinkedIn Resume Generator is a Python project that automates the process of generating personalized resumes for job applications on LinkedIn. It scrapes job postings, selects desired jobs, generates resumes using OpenAI's GPT-3.5 Turbo, and saves the resumes as Google Docs files in specific folders on Google Drive.

## Features

- Login to LinkedIn
- Extract job titles and descriptions
- User selection of jobs for generating resumes
- Generate resumes using OpenAI's GPT-3.5 Turbo
- Save resumes as Google Docs files in Google Drive

## Dependencies

- Selenium
- Google API Client Library
- Google Auth Library
- OpenAI

## Installation

1. Clone this repository:

git clone https://github.com/yourusername/linkedin-resume-generator.git

2. Install the required packages:

pip install selenium google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client openai

3. Download the appropriate ChromeDriver for your system and add it to your PATH variable.

4. Create a `credentials.json` file containing your LinkedIn credentials and OpenAI API key, and save it in the project folder. The file should have the following format:
```json
{
    "email": "your_linkedin_email@example.com",
    "password": "your_linkedin_password",
    "openai_api_key": "your_openai_api_key"
}
```

5. Follow the Google Drive API Python Quickstart guide to create a new project and obtain the credentials. Save the GDriveAuthentication.json file in the project folder.

## Usage

1. Modify the LinkedInResumeGenerator instantiation in the __main__ section with the file name containing your prompt text.

2. Run the script:

python linkedin_resume_generator.py

3.The script will prompt you to select jobs, generate resumes, and save them to Google Drive.

## How You Can Contribute

We welcome contributions to improve and expand the LinkedIn Resume Generator. Here are some ideas for how you can contribute:

1. **Create a new way for the user to select the desired jobs:** Improve the user interface for job selection, making it more user-friendly and efficient.
2. **Create a Google Drive formatting option to bold and bullet point:** Enhance the formatting of the generated resumes in Google Docs, including adding bold text and bullet points where appropriate.
3. **Make the prompt better:** Refine the prompt used for generating resumes with GPT-3.5 Turbo, ensuring it produces high-quality, tailored resumes.
4. **Make the search better by adding LinkedIn filters:** Integrate LinkedIn filters to improve the job search functionality, allowing users to find more relevant job postings.


## Contributing
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and submit a pull request.

Thank you for your interest in contributing to the LinkedIn Resume Generator project!


## License
This project is licensed under the MIT License.
