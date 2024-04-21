from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from app.models import FileName, CredentialsModel


def get_file():
    cred = CredentialsModel.objects.last()
    print(cred)
    credentials = {
        'token': cred.token,
        'refresh_token': cred.refresh_token,
        'token_uri': cred.token_uri,
        'client_id': cred.client_id,
        'client_secret': cred.client_secret,
        'scopes': cred.scopes}
    print(credentials)
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

            # Google Docs belgisini olish
            doc = drive_service.files().export_media(fileId=file_id,
                                                     mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document').execute()

            # Docx faylini o'qish
            from io import BytesIO
            import zipfile
            import xml.etree.ElementTree as ET

            docx_content = BytesIO(doc)
            zipf = zipfile.ZipFile(docx_content)

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

                    if a + 1 < len(elems):
                        print(word[1])
                        word[1] = elems[a + 1]
                        # print(elems[a + 1])
                    # print(word)
                    f = FileName(name=file_name, key=word[0], word=word[-1])
                    lines.append(f)
            FileName.objects.bulk_create(lines)
