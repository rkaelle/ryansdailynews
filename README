# Ryan's Daily News Email Automation

## Overview

Welcome to the Ryan's Daily News Email Automation project! This repository houses a sophisticated Python script that fetches the latest events, reflections, skills, and science facts to send personalized daily emails to subscribers. The script leverages multiple technologies and APIs to deliver fresh and engaging content straight to your inbox every morning.

## Features

- **Automated Email Dispatch**: Sends personalized emails with daily updates to all subscribers in the Firestore database.
- **Event Fetching**: Retrieves events from a Google Calendar and formats them for inclusion in the email.
- **Twilio Integration**: Fetches the most recent message from a Twilio number and processes it using OpenAI to extract useful content.
- **OpenAI Integration**: Uses OpenAI to structure and enrich the text from Twilio messages.
- **Firestore Database**: Manages subscriber data and tracks the edition number for the daily newsletter.

## Technologies Used

- **Python**: Core programming language for the script.
- **smtplib**: For sending emails via SMTP.
- **Firebase Firestore**: Stores subscriber information and edition tracking.
- **Google Calendar API**: Fetches the latest events.
- **Twilio API**: Retrieves the most recent message.
- **OpenAI API**: Processes and enriches message content.
- **dotenv**: Manages environment variables.
- **logging**: Tracks and records the script's operations.

## Project Structure

- **main.py**: The main script orchestrating the email sending process.
- **calendar_module.py**: Handles fetching events from Google Calendar.
- **dailytext.py**: Sends daily SMS messages via Twilio.
- **responseFormat.py**: Processes Twilio messages using OpenAI.
- **TwilioGET.py**: Fetches the most recent message from Twilio.
- **utils.py**: Utility functions for database operations and formatting.

## Setup

1. **Clone the repository**:
   ```sh
   git clone https://github.com/your-repo/ryans-daily-news.git
   cd ryans-daily-news

2. **Create a virtual environment:**
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`

2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt

4. **Set up environment variables (a .env file) in the root directory with the following variables:**
    ```sh
    MAIL_USERNAME=your_email@example.com
    MAIL_PASSWORD=your_email_password
    TWILIO_SID=your_twilio_sid
    TWILIO_TOKEN=your_twilio_auth_token
    OPEN_API_KEY=your_openai_api_key

5. **Set up Firebase credentials:**
    Place your Firebase credentials file (firebaseCredentials.json) in the root directory.

6. **Authorize Google Calendar API:**
    Follow the instructions to set up OAuth 2.0 for the Google Calendar API and save your credentials.json in the root directory.

## Usage 

Run the main script to start sending emails:

    ```sh
    python main.py
    ```
Ideally you set it up on server so it will run every day at a desired time. For this I reccomend looking at the Crontab tool.

## Logging

The script uses Python’s logging module to log debug and error messages. Logs are printed to the console and can be redirected to a file if needed.

## Contributing

We welcome contributions to enhance this project. Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

Happy emailing!

Ryan Kaelle