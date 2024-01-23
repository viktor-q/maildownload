import os
import sys
import imaplib
import email
from imapclient import IMAPClient

# Заполнить
username = 'your_username'
password = 'your_password'
folder = 'INBOX'
output_directory = '/path/to/save/attachments'



def download_attachments(username, password, folder, output_directory):
    # Установка соединения с почтовым сервером
    server = IMAPClient('mailserver.kolhoz.spb.ru', use_uid=True)
    server.login(username, password)

    # Выбор папки с письмами
    server.select_folder(folder)

    # Поиск писем со вложениями
    messages = server.search(['HAS', 'ATTACHMENT'])

    for msgid, data in server.fetch(messages, 'RFC822').items():
        email_message = email.message_from_bytes(data[b'RFC822'])

        for part in email_message.walk():
            # Проверка наличия вложений
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            # Сохранение вложений в указанную папку
            filename = part.get_filename()
            if filename:
                att_path = os.path.join(output_directory, filename)
                with open(att_path, 'wb') as attachment:
                    attachment.write(part.get_payload(decode=True))

    server.logout()


download_attachments(username, password, folder, output_directory)