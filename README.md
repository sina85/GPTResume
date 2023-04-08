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


3. Download the appropriate [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) for your system and add it to your PATH variable.

4. Create a `GDriveAuthentication.json` file containing your Google API credentials, and save it in the project folder. Follow the [Google Drive API Python Quickstart](https://developers.google.com/drive/api/v3/quickstart/python) guide to create a new project and obtain the credentials.

5. Get an OpenAI API key by signing up for the [OpenAI API](https://be
The script will prompt you to select jobs, generate resumes, and save them to Google Drive.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and submit a pull request.

## License

This project is licensed under the MIT License.ta.openai.com/signup/).

6. Set the OpenAI API key as an environment variable:
export OPENAI_API_KEY=your_api_key_here


## Usage

1. Modify the `LinkedInResumeGenerator` instantiation in the `__main__` section with your LinkedIn email and password, and the file name containing your prompt text.

2. Run the script:
python linkedin_resume_generator.py


The script will prompt you to select jobs, generate resumes, and save them to Google Drive.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and submit a pull request.

## License

This project is licensed under the MIT License.
