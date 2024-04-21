from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from google_auth_oauthlib.flow import Flow
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO
from googleapiclient.http import MediaIoBaseDownload

from app.models import FileName, CredentialsModel

sheets = [['Fayl nomi', 'Key', 'Word'], ['1.docx', 'ddd', "dddddd"], ['2.docx', 'aaa', 'aaaaaaa'],
          ['3.docx', 'ddd', 'dddddd'], ['1.docx', 'aaa', 'aaaaaaa'], ['2.docx', 'ddd', 'dddddd'],
          ['3.docx', 'aaa', 'aaaaaaa'], ['1.docx', 'ddd1', 'dddddd1'], ['2.docx', 'aaa1', 'aaaaaaa1'],
          ['3.docx', 'ddd2', 'dddddd2'], ['1.docx', 'aaa2', 'aaaaaaa2']]


def oauth2callback(request: HttpRequest):
    state = request.session['state']
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    flow = Flow.from_client_secrets_file(
        os.path.join(os.path.dirname(__file__), '../client_secret_1.json'),
        scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets'],
        state=state)
    flow.redirect_uri = "http://127.0.0.1:8001/oauth2callback"
    # print(flow.redirect_uri)

    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    for c in CredentialsModel.objects.all():
        c.delete()
    CredentialsModel.objects.create(token=credentials.token, refresh_token=credentials.refresh_token,
                                    token_uri=credentials.token_uri, client_id=credentials.client_id,
                                    client_secret=credentials.client_secret, scopes=credentials.scopes)
    request.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes}

    return redirect('index')


def get_file_name(request):
    credentials = request.session.get('credentials', None)
    creds = Credentials(**credentials)

    drive_service = build('drive', 'v3', credentials=creds)
    folder_id = '1pfvXH_XLkb2mcuX5Rgnql_pnfAqfXGiL'
    # Google Drive'dagi belgilar ro'yxatini olish
    files = drive_service.files().list(q=f"'{folder_id}' in parents", fields="files(id, name)").execute()
    file_list = files.get('files', [])
    # print(file_list)
    for file_data in FileName.objects.all():
        file_data.delete()
    # Agar belgilar ro'yxati bo'sh bo'lmasa
    if file_list:
        for file in file_list:
            print(file)
            # Boshqa belgilardan birini olish
            file_id = file['id']
            file_name = file['name']
            print(file_name)
            # # Download the existing file content
            # existing_content = download_file(drive_service, file_id)
            #
            # # Modify the content as needed
            # modified_content = modify_content(existing_content)
            #
            # # Upload the modified content back to the file
            # upload_file(drive_service, file_id, modified_content)
            # print("File updated:", file['name'])
            # Google Docs belgisini olish
            doc = drive_service.files().export_media(fileId=file_id,
                                                     mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document').execute()

            # Docx faylini o'qish
            from io import BytesIO
            import zipfile
            import xml.etree.ElementTree as ET

            docx_content = BytesIO(doc)
            zipf = zipfile.ZipFile(docx_content)
            # updated_content = BytesIO()
            # target_word = ""
            # new_word = ""

            # with zipfile.ZipFile(updated_content, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
            #     for name in zipf.namelist():
            #         with zipf.open(name) as input_file:
            #             content = input_file.read()
            #             if isinstance(content, bytes):
            #                 content = content.decode('utf-8')
            #             content = content.replace(target_word, new_word).encode('utf-8')
            #             zf.writestr(name, content)
            #
            # # Update the Google Docs file with the modified content
            # media = MediaIoBaseUpload(updated_content,
            #                           mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            # drive_service.files().update(fileId=file_id, media_body=media).execute()

            # Docx fayl ichidagi malumotlarni olish
            xml_content = zipf.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            text_elements = tree.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t')

            # Malumotlarni qaytarish
            lines = []
            elems = []
            for elem in text_elements:
                elems.append(elem.text)
            # print(elems)
            for elem in text_elements:
                word = elem.text.split(":")
                if len(word) > 1:
                    a = elems.index(elem.text)
                    # print(elem.text)
                    # print(elems[a + 1])
                    if a + 1 > len(elems):
                        word[1] = elems[a + 1]
                    # print(word)
                    f = FileName(name=file_name, key=word[0], word=word[-1])
                    lines.append(f)
            FileName.objects.bulk_create(lines)
    return HttpResponse("salom")


def index(request: HttpRequest):
    # Get credentials from session if available
    credentials = request.session.get('credentials', None)
    context = {}
    print(credentials)
    if credentials:
        creds = Credentials(**credentials)

        drive_service = build('drive', 'v3', credentials=creds)
        folder_id = '1pfvXH_XLkb2mcuX5Rgnql_pnfAqfXGiL'
        # Google Drive'dagi belgilar ro'yxatini olish
        files = drive_service.files().list(q=f"'{folder_id}' in parents", fields="files(id, name)").execute()
        file_list = files.get('files', [])
        # print(file_list)
        # Agar belgilar ro'yxati bo'sh bo'lmasa
        if file_list:
            for sheet in sheets:
                for file in file_list:
                    print(file)
                    # Boshqa belgilardan birini olish
                    file_id = file['id']
                    file_name = file['name']
                    print(file_name)
                    # # Download the existing file content
                    # existing_content = download_file(drive_service, file_id)
                    #
                    # # Modify the content as needed
                    # modified_content = modify_content(existing_content)
                    #
                    # # Upload the modified content back to the file
                    # upload_file(drive_service, file_id, modified_content)
                    # print("File updated:", file['name'])
                    # Google Docs belgisini olish
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
                                        print(target_word, new_word)
                                        content = content.replace(target_word, new_word).encode('utf-8')
                                        zf.writestr(name, content)

                            # Update the Google Docs file with the modified content
                            media = MediaIoBaseUpload(updated_content,
                                                      mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                            drive_service.files().update(fileId=file_id, media_body=media).execute()
                            print("888888888")
                # Docx fayl ichidagi malumotlarni olish
        #         xml_content = zipf.read('word/document.xml')
        #         tree = ET.fromstring(xml_content)
        #         text_elements = tree.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t')
        #
        #         # Malumotlarni qaytarish
        #         lines = []
        #         for elem in text_elements:
        #             if 'МИНИСТЕРСТВО' in elem.text:
        #                 elem.text = elem.text.replace('МИНИСТЕРСТВО', 'new_word')
        #
        #                 # Convert the modified XML tree back to bytes
        #             updated_doc_content = ET.tostring(tree)
        #
        #             # Update the Google Docs file with the modified content
        #             media = MediaIoBaseUpload(BytesIO(updated_doc_content),
        #                                       mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        #             drive_service.files().update(fileId=file_id, media_body=media).execute()
        # context['document_text'] = text_data
    else:
        # No credentials available, redirect to OAuth2 flow
        # print("QQQQQQQQQQQQQQQQQQ")
        flow = Flow.from_client_secrets_file(
            os.path.join(os.path.dirname(__file__), '../client_secret_1.json'),
            scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets'])
        flow.redirect_uri = request.build_absolute_uri('/oauth2callback')
        authorization_url, state = flow.authorization_url(access_type='offline')
        request.session['state'] = state
        # print(state)
        context['authorization_url'] = authorization_url

    return render(request, 'index.html', context)


# def modify_content(existing_content):
#     encodings_to_try = ['utf-8', 'latin-1', 'windows-1252']  # Add more encodings if necessary
#
#     for encoding in encodings_to_try:
#         try:
#             existing_content_str = existing_content.decode(encoding)
#             break  # If decoding succeeds, exit the loop
#         except UnicodeDecodeError:
#             continue  # If decoding fails, try the next encoding
#     # Your modification logic goes here
#     modified_content_str = existing_content_str.replace('old_text', 'new_text')
#
#     # Encode the modified content back to bytes
#     modified_content_bytes = modified_content_str.encode('utf-8')
#
#     return modified_content_bytes
#
# def download_file(drive_service, file_id):
#     request = drive_service.files().export_media(fileId=file_id,
#                                                  mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
#     fh = BytesIO()
#     downloader = MediaIoBaseDownload(fh, request)
#     done = False
#     while done is False:
#         status, done = downloader.next_chunk()
#         print("Download %d%%." % int(status.progress() * 100))
#     return fh.getvalue()
#
#
# from googleapiclient.http import MediaIoBaseUpload
#
#
# def upload_file(drive_service, file_id, content):
#     media = MediaIoBaseUpload(BytesIO(content),
#                               mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
#     drive_service.files().update(fileId=file_id, media_body=media).execute()


def login_oauth(request: HttpRequest):
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

    return render(request, 'index.html', context)
