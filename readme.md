## Introduction

## Functionality of Folders
The files are organized in folders as following:
- **scripts**: where the python scripts are placed.
- **credentials**: the credentials (client_secret.json) for accessing the Google-API project are placed here.
- **tokens**: after the authentication flow completes for the first time, the token file (token.pickle) is placed here.
- **downloads**: the files downloaded from Google Drive are placed in this folder.

## Reminders
- The credential (client_secret.json) should be downloaded from [Google Cloud Platform](http://console.cloud.google.com/), and placed in the folder "credentials".
- The token file (token.pickle) will be created automatically when the Google authentication flow completes for the first time.
- The folders "tokens" and "downloads" will be created automatically if not existed, but the folders "credentials" should be created manually.
