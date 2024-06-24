# ReachInbox.ai - Email Automation Tool

This project is about automating email parsing, categorization, and response generation using OAuth for Gmail and Outlook integration. It uses BulllMQ for task scheduling and OpenAI for context understanding.

## Features

- Connect to Gmail and Outlook accounts using OAuth.
- Fetch incoming emails and categorize them based on content.
- Generate and send automated replies based on the email context.
- Use redis based bullmq for scheduling and managing background tasks.

## Prerequisites

- Python (>= 3.8)
- Redis server
- Google Cloud and Outlook Developer accounts for OAuth credentials
- OpenAI API key

## Setup Instructions

### 1. Clone the Repository
Please checkout to master branch

### 2. .env variables

```bash
OPENAI_API_KEY=your_openai_api_key

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password (if applicable)
```

### 3. Install Dependencies

```bash
pip install django google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client django_rq bullmq openai
```

### 4. Start the Redis Server

```bash
redis-server
```

### 5. Start Django Development Server

The development server will start running at: localhost:8000

```bash
python manage.py runserver
```

## Instructions: Project Walk-through (RED-ZONE)

#### How It Works:

1. **Gmail and Outlook OAuth Connection**: Users will be prompted to connect their Gmail and Outlook accounts for OAuth authentication.
2. **Connecting Gmail**: When clicking the Connect Gmail button on the home page, users will be prompted to connect their Gmail account. Follow the steps to authorize the application to access your Gmail.
3. **Automatic Email Processing**: Once the Gmail connection is established, the system will automatically trigger the trigger-email-processing endpoint. This will fetch the emails and you can view the fetched emails in your console.
4. **Checking Automatic Replies**: To verify the functionality, visit your Gmail's Sent section to check if automatic replies are being sent. The system is designed to send automated responses based on the context of the received emails.

#### Known Issues:

1. **Email Content Not Found**: You might encounter an error in the console indicating that the content of an email was not found. This is a known issue and is being addressed but it won't affect the working of the project.
2. **Uniform Responses**: Currently, the model used for generating automatic replies might send the same response to all emails. This could be due to limitations in the chosen model. Please connect with me if you encounter this issue.
3. **Intentionally Added Creds**: I have intentionally pushed the credentisla like OAuth Client ID, Client Secret, and the OpenAI API Key only for your reference.

### Additional Steps

If you encounter any issues or have suggestions for improvements, please reach out. Contributions and feedback are always welcome to enhance the functionality and reliability of the application.

## Connect with me here:

1. [LinkedIn] https://www.linkedin.com/in/dheeraj-parmar/

2. [Email] parmardheeraj6@gmail.com

3. [Phone] +91 941 380 2811

### Thanks!
