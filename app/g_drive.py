import os
import docx
from google.oauth2 import credentials
from .Google import Create_Service
from .models import FileName
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
import io
from google.oauth2.credentials import Credentials
folder_path = os.getcwd()
# print(folder_path) kAj4a?ZrcJy!

new_data = {
    "C_KEY": "Hello Amerika00",
    "D_KEY": "Hello Paris00",
    # Add more key-word pairs as needed
}


def write_to_files(*args):
    FOLDER_PATH = os.getcwd()
    CLIENT_SECRET_FILE = os.path.join(FOLDER_PATH, 'client_secret_1.json')
    API_SERVICE_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    # service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)
    # Foydalanuvchini Google Drive ga kirish uchun ruxsat berish
    # flow = InstalledAppFlow.from_client_secrets_file(
    #     'client_secrets.json', scopes=['https://www.googleapis.com/auth/drive'])
    # # creds = flow
    # # print("kkkkkkk", creds)
    # creds = credentials.Credentials.from_authorized_user_file('client_secrets.json')
    # print(args[0])
    creds = Credentials(**args[0])
    service = build(API_SERVICE_NAME, API_VERSION, credentials=creds)
    # # Yetkilangan ma'lumotlar
    # drive_service = build('drive', 'v3', credentials=creds)
    drive_service = service
    # Klonlanadigan papka ID si
    folder_id = '1eUj7ys6Mh7EEoPPVCqH9SsMRLscJBvYF'

    # Papkadagi fayllarni ro'yxatga olish
    results = drive_service.files().list(q=f"'{folder_id}' in parents", fields="files(id, name)").execute()
    files = results.get('files', [])
    # print(files)
    # Fayllarga mazmun qo'shish
    for file in files:
        file_id = file.get('id')
        file_name = file.get('name')

        # Faylni o'qish
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        print("download", file_name)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        with open(os.path.join(os.getcwd(), file_name), 'wb') as f:
            f.write(fh.read())
            f.close()

        # def update_docx_files_in_folder(folder_path, new_data):
        #     # for filename in files['name']:
        #     if file_name.endswith('.docx'):
        #         file_path = os.path.join(folder_path, file_name)
        #         file_name1 = os.path.splitext(file_name)[0]
        #         # update_docx_file(file_path, new_data, file_name)  # Fayl nomini ham uzatish
        #         writing_sheet(file_path, file_name1)
        #
        # # writing_file = []
        # # writing_key = []
        # # writing_word = []
        #
        # def writing_sheet(file_path, file_name1):
        #     # print(file_path)
        #     doc = docx.Document(file_path)
        #     for paragraph in doc.paragraphs:
        #         word1 = paragraph.text.split(":")
        #
        #         # print(word1)
        #         # writing_file.append(file_name)
        #         if word1[0] == "":
        #             f = FileName(name=file_name1, key=word1[0])
        #             f.save()
        #         else:
        #             f = FileName(name=file_name1, key=word1[0], word=word1[1])
        #             f.save()
        #     # print(writing_file)
        #     doc.save(file_path)
        #
        # update_docx_files_in_folder(folder_path, new_data)

        # Faylni yangilash uchun
        content = "Bu faylga yozildi."
        # print("fh", fh.name)
        fh.seek(0)
        fh.write(content.encode())
        fh.seek(0)

        # Faylni yuklash uchun
        media = MediaIoBaseUpload(fh, mimetype='application/octet-stream', resumable=True)
        drive_service.files().update(fileId=file_id, media_body=media).execute()
