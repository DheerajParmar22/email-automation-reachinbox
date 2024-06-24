import os
import openai
import google.auth
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
import email

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']
openai.api_key = 'sk-proj-NmtYq5os55EZyuM0FIzaT3BlbkFJ2gjUDNZREij1SeFyjndl'
REDIRECT_URI = 'http://localhost:8000/gmail_callback/'

def get_gmail_auth_url():
    flow = InstalledAppFlow.from_client_secrets_file('email_app\client_secret_168879313172-ob1cr7fim197m7t9p3vfjpaeoqkmh6at.apps.googleusercontent.com.json', SCOPES, redirect_uri=REDIRECT_URI)
    auth_url, _ = flow.authorization_url(access_type='offline', prompt='consent')
    return auth_url

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('email_app\client_secret_168879313172-ob1cr7fim197m7t9p3vfjpaeoqkmh6at.apps.googleusercontent.com.json', SCOPES,redirect_uri=REDIRECT_URI)
            creds = flow.run_local_server(port=8080)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def save_gmail_credentials(credentials):
    with open('token.json', 'w') as token:
        token.write(credentials.to_json())


def get_emails(service):
    try:
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
        messages = results.get('messages', [])
        emails = []
        if not messages:
            print('No new messages.')
        else:
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
                email_data = {
                    'from': '',
                    'subject': '',
                    'content': ''
                }
                for header in msg['payload']['headers']:
                    if header['name'] == 'From':
                        email_data['from'] = header['value']
                    if header['name'] == 'Subject':
                        email_data['subject'] = header['value']
                
                if 'parts' in msg['payload']:
                    for part in msg['payload']['parts']:
                        if part['mimeType'] == 'text/plain':
                            email_data['content'] = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                            break
                else:
                    email_data['content'] = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')
                    
                emails.append(email_data)
        print(f"Fetched {len(emails)} emails")
        return emails
    except HttpError as error:
        print(f'An error occurred: {error}')
        return []
    except Exception as e:
        print(f'An error occurred while fetching emails: {e}')
        return []


def categorize_email(content):
  try:
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Categorize the following email: {content}\n\nLabels: Interested, Not Interested, More information",
        max_tokens=50
    )
    category = response.choices[0].text.strip()
  except Exception as e:
        print(f"Error categorizing email: {e}")
        category = "Uncategorized"
  return category

def generate_response(content, category):
  try:
    prompt = f"Generate a response for an email categorized as '{category}'.\nEmail content: {content}"
    response = openai.Completion.create(
        model="text-embedding-3-small",
        prompt=prompt,
        max_tokens=150
    )
    reply = response.choices[0].text.strip()
  except Exception as e:
        print(f"Error generating response: {e}")
        reply = "Sorry, there was an error processing your email."
  return reply

def send_email(email_to, reply):
    service = get_gmail_service()
    # message = email.mime.text.MIMEText(reply)
    message = MIMEText(reply)
    message['to'] = email_to
    message['from'] = 'parmardheeraj6@example.com'
    message['subject'] = 'Re: ' + email_to
    raw = base64.urlsafe_b64encode(message.as_string().encode('utf-8'))
    raw = raw.decode('utf-8')
    body = {'raw': raw}
    try:
        message = service.users().messages().send(userId='me', body=body).execute()
        print('Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        print('An error occurred: %s' % error)
        return None



