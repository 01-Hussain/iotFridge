from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

right_Now_path = os.getcwd()


def auth_account():
    """
    The file token.json stores the user's access and refresh tokens, and is
    created automatically when the authorization flow completes for the first
    time.
    """

    SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/drive.file']

    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        return creds

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            return creds
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
            return creds


def upload_basic(creds=auth_account()):
    """Insert new files and folders.
    Returns: Id's of the file's - folder's uploaded.
    """
    service = build('drive', 'v3', credentials=creds)

    filtered_DIR = filter(os.path.isdir, os.listdir())

    for dir in filtered_DIR:
        if dir == 'train':

            # create a folder that is named "train"
            file_metadata = {
                'name': 'train',
                'mimeType': 'application/vnd.google-apps.folder'
            }

            folder = service.files().create(body=file_metadata, fields='id').execute()

            # change the DIR path to inside the test DIR
            updated_test_DIR = os.getcwd() + '/' + dir
            os.chdir(updated_test_DIR)

            # list all the folders in inside the test DIR
            for folders in os.listdir():
                # Make a DIR's with the folders string in Google Drive
                file_metadata = {
                    'name': f'{folders}',
                    'parents': [folder.get('id')],
                    'mimeType': 'application/vnd.google-apps.folder'
                }

                inner_folder = service.files().create(body=file_metadata, fields='id').execute()

                # change the system path to inside the inner folders
                inner_folders_path = updated_test_DIR + '/' + folders
                os.chdir(inner_folders_path)

                # list and upload the content of the inner folders
                for content in os.listdir():
                    file_metadata = {'name': f'{content}', 'parents': [inner_folder.get('id')]}

                    content_path = inner_folders_path + '/' + content

                    media = MediaFileUpload(f'{content_path}')

                    # pylint: disable=maybe-no-member
                    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

                    if file is not None:
                        print(file.get('id'))
                    else:
                        print("File upload failed.")
                        return None


if __name__ == '__main__':
    auth_account()
    upload_basic()
