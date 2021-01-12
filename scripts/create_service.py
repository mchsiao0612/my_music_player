import os
import pickle
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request

def create_service(client_secret_file, api_name, api_version, scopes):

    # Create the folder "tokens" if it's not existed.
    if os.path.exists("../tokens") == False:
        os.system("mkdir ../tokens")

    # Set file name for the pickle file.
    # The pickle file records the user's access tokens and refresh tokens.
    # The pickle file is created when the authorization flow completes for the first time.
    pickle_file = "../tokens/token.pickle"

    # Check whether the pickle file exists or not.
    credential = None
    if os.path.exists(pickle_file):
        with open(pickle_file, "rb") as token:
            credential = pickle.load(token)

    # If the access token is expired, request a new one from google authorization server.
    # If there are no credential, create a new flow and start a local web server to ask the user for login.
    # Save the new credential for next run.
    if not credential or not credential.valid:
        if credential and credential.expired and credential.refresh_token:
            credential.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes)
            credential = flow.run_local_server(port=0)
        with open(pickle_file, "wb") as token:
            pickle.dump(credential, token)

    # Construct an instance for interacting with the API.
    try:
        service_instance = build(api_name, api_version, credentials=credential)
        return service_instance
    except Exception as e:
        print(e)
        return None
