"""
Read pdf file, extract text, search for valid email.
If found send text to this email.
"""

# Reaquire's modules
# pip install pdfminer pdfminer.six smtplib

from pdfminer import high_level
import re
import smtplib

# Regex search for valid email address, simple not validate all!
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

# Name of pdf file
FILE_NAME = 'p.pdf'

# Store attrrib here
store_email = {'email': None,
               'sender': 'Here is username for gmail', 'password': 'Here is gmail user password'}

# Email configuration is hard code here
EMAIL_PORT = 587
EMAIL_SMTP = 'smtp.gmail.com'
MSG = 'Borko send massage!'


def send_email(obj_data):
    """
    Standart function for send email use gmail acc
    """
    server = smtplib.SMTP(EMAIL_SMTP, EMAIL_PORT)
    server.starttls()
    server.login(obj_data['sender'], obj_data['password'])
    msg = MSG
    server.sendmail(obj_data['sender'], obj_data['email'], msg)


def check(email):
    """ return true if read line is valid email else false """
    return re.search(regex, email)


def search_text_in_file(text):
    """
    Split pdf convert file for new line, use generator 
    for low memori usage if text is big
    """
    for line in text.split("\n"):
        yield line


class ReadPdf:
    """
    Class use high_level module
    """

    def __init__(self, file) -> None:
        self.local_pdf_filename = file
        self.pages = [0]

    def extract(self):
        self.extracted_text = high_level.extract_text(
            self.local_pdf_filename, "", self.pages)
        return self.extracted_text


if __name__ == '__main__':
    pdf = ReadPdf(FILE_NAME).extract()

    for line in search_text_in_file(pdf):
        if check(line):
            store_email['email'] = line
            break

    if store_email['email']:
        send_email(store_email)
    else:
        print("Not found valid email address sorry...")
