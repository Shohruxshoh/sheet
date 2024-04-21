from django.shortcuts import render, redirect
from docx import Document
from google_auth_oauthlib.flow import Flow
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FileName, CredentialsModel
from .sheet_create import create_sheet
# from .drive import download
from .g_drive import write_to_files
from .writing_data import writing
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from .g_file import get_file

# Create your views here.

class FileWritingView(APIView):
    def get(self, request, *args, **kwargs):
        print(request.data)
        f = FileName.objects.all()
        for i in f:
            i.delete()
        print("MJJJJJJJJJJJJJJJJJ")
        write_to_files(request.session.get('credentials', None))
        # download()
        create_sheet()
        file_name = []
        key = []
        word = []
        for name in f:
            file_name.append(name.name)
            key.append(name.key)
            word.append(name.word)
        print(file_name, key, word)
        writing(file_name, key, word)
        return Response({"message": "kkk"})


class LoginViewApi(APIView):
    def get(self, request, *args, **kwargs):

        context = {}

        flow = Flow.from_client_secrets_file(
            os.path.join(os.path.dirname(__file__), '../client_secret_1.json'),
            scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets'])
        flow.redirect_uri = request.build_absolute_uri('/oauth2callback')
        authorization_url, state = flow.authorization_url(access_type='offline')
        request.session['state'] = state
        # print(state)
        context['authorization_url'] = authorization_url
        import webbrowser

        # Brawserni ochish
        webbrowser.open(authorization_url)

        return redirect('api-index')



class AAA(APIView):
    def get(self, request, *args, **kwargs):
        import requests
        r = requests.get("http://127.0.0.1:8001/api/login")
        print(r.status_code)
        get_file()
        # print(request.data['salom'])
        lists = request.data['salom']
        credentials = request.session.get('credentials', None)
        context = {}
        cred = CredentialsModel.objects.last()
        # print(cred)
        credentials = {
            'token': cred.token,
            'refresh_token': cred.refresh_token,
            'token_uri': cred.token_uri,
            'client_id': cred.client_id,
            'client_secret': cred.client_secret,
            'scopes': cred.scopes}
        # print(credentials)
        if credentials:
            creds = Credentials(**credentials)

            drive_service = build('drive', 'v3', credentials=creds)
            folder_id = ''
            if request.data['folderId']:
                folder_id = request.data['folderId']
                # print(folder_id)
            else:
                folder_id = '1pfvXH_XLkb2mcuX5Rgnql_pnfAqfXGiL'
            # Google Drive'dagi belgilar ro'yxatini olish
            files = drive_service.files().list(q=f"'{folder_id}' in parents", fields="files(id, name)").execute()
            file_list = files.get('files', [])
            # print(file_list)
            # Agar belgilar ro'yxati bo'sh bo'lmasa
            if file_list:
                for sheet in lists:
                    for file in file_list:
                        # print(file)
                        # print(sheet)
                        # Boshqa belgilardan birini olish
                        file_id = file['id']
                        file_name = file['name']
                        # print(file_name)
                        doc = drive_service.files().export_media(fileId=file_id,
                                                                 mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document').execute()

                        # Docx faylini o'qish
                        from io import BytesIO
                        import zipfile
                        import xml.etree.ElementTree as ET

                        docx_content = BytesIO(doc)
                        zipf = zipfile.ZipFile(docx_content)
                        updated_content = BytesIO()
                        target_word = ""
                        new_word = ""
                        for f1 in FileName.objects.all():
                            if f1.key == sheet[1] and f1.name == sheet[0] and f1.name == file_name:
                                target_word = f1.word
                                new_word = sheet[2]
                                f1.word = new_word
                                f1.save()

                                docx_content = BytesIO(doc)
                                zipf = zipfile.ZipFile(docx_content)
                                updated_content = BytesIO()
                                with zipfile.ZipFile(updated_content, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
                                    for name in zipf.namelist():
                                        with zipf.open(name) as input_file:
                                            content = input_file.read()
                                            if isinstance(content, bytes):
                                                content = content.decode('utf-8')
                                            # print(target_word, new_word)
                                            content = content.replace(target_word, new_word).encode('utf-8')
                                            zf.writestr(name, content)

                                # Update the Google Docs file with the modified content
                                media = MediaIoBaseUpload(updated_content,
                                                          mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                                drive_service.files().update(fileId=file_id, media_body=media).execute()
                                print("888888888")
        return Response({"message": "kkk"})
