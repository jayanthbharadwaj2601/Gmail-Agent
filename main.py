import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.message import EmailMessage
from fastapi import FastAPI
from google import genai
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pydantic import BaseModel
import os.path
from fastapi.middleware.cors import CORSMiddleware
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from fastapi import FastAPI
import base64
from email.message import EmailMessage
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class mailbody(BaseModel):
  fromid: str
  toid: str
  body:str
SCOPES = ["https://www.googleapis.com/auth/gmail.compose","https://www.googleapis.com/auth/gmail.readonly"]

app = FastAPI()
origins = [
    
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/")
def gmail_create_draft(mail:mailbody):
  """Create and insert a draft email.
   Print the returned draft's message and id.
   Returns: Draft object, including draft id and message meta data.

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  creds = Credentials.from_authorized_user_file("token.json", SCOPES)

  client = genai.Client(api_key="AIzaSyC7LB7Jy1CRfTpxd9935-LVA0C5VhzKzHc")
  

  

  try:
    # create gmail api client
    service = build("gmail", "v1", credentials=creds)
    a=mail.toid.split(',')
    for i in a:
      message = EmailMessage()
      response = client.models.generate_content(
      model="gemini-1.5-flash", contents="Draft a mail to"+i+"based on the following summarized version:"+mail.body+"Use proper salutation and closing remark. While addressing the recipient and myself,use the names instead of mail ids.Extract the names from given mail ids.You already have the recipients mail id. Here is mine:"+mail.fromid+".Dont provide me with the subject,just the body"
    )
      subject = client.models.generate_content(
      model="gemini-1.5-flash", contents="Generate an appropriate subject based on the following summarized version of the body:"+mail.body+".Make sure it is as concise as possible and fits in a single line"
    )
    
      message.set_content(response.text)

      message["To"] = i
      message["From"] = mail.fromid
      message["Subject"] = subject.text

      # encoded message
      encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

      create_message = {"message": {"raw": encoded_message}}
      # service.users().messages.send(userId="me",body=create_message)
      # pylint: disable=E1101
      draft = (
          service.users()
          .drafts()
          .create(userId="me", body=create_message)
          .execute()
      )

      print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')

  except HttpError as error:
    print(f"An error occurred: {error}")
    draft = None
  draft={"result":"Success"}
  return draft
@app.post('/login')
def main():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])

    if not labels:
      print("No labels found.")
      return
    print("Labels:")
    for label in labels:
      print(label["name"])

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    return {"error":error}
@app.post('/send')
def gmail_send_message(mail:mailbody):
  """Create and insert a draft email.
   Print the returned draft's message and id.
   Returns: Draft object, including draft id and message meta data.

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  creds = Credentials.from_authorized_user_file("token.json", SCOPES)

  client = genai.Client(api_key="AIzaSyC7LB7Jy1CRfTpxd9935-LVA0C5VhzKzHc")
  

  

  try:
    # create gmail api client
    service = build("gmail", "v1", credentials=creds)
    a=mail.toid.split(',')
    for i in a:
      message = EmailMessage()
      response = client.models.generate_content(
      model="gemini-1.5-flash", contents="Draft a mail to"+i+"based on the following summarized version:"+mail.body+"Use proper salutation and closing remark. While addressing the recipient and myself,use the names instead of mail ids.Extract the names from given mail ids.You already have the recipients mail id. Here is mine:"+mail.fromid+".Dont provide me with the subject,just the body"
    )
      subject = client.models.generate_content(
      model="gemini-1.5-flash", contents="Generate an appropriate subject based on the following summarized version of the body:"+mail.body+".Make sure it is as concise as possible and fits in a single line"
    )
    
      message.set_content(response.text)

      message["To"] = i
      message["From"] = mail.fromid
      message["Subject"] = subject.text

      # encoded message
      encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

      create_message = {"raw": encoded_message}
      # service.users().messages.send(userId="me",body=create_message)
      # pylint: disable=E1101
      draft = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )

      print(f'Message Id: {draft["id"]}')

  except HttpError as error:
    print(f"An error occurred: {error}")
    draft = None
  draft={"result":"Success"}
  return draft