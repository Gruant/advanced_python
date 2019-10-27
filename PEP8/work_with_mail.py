import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail:
    login = ''

    def __init__(self, login='mail@gmail.ru', password='qwerty'):
        self.login = login
        self.__password = password

    def send_message(self, subject='Subject', recipients=None, message_text='Message', gmail_smtp='smtp.gmail.com'):
        """Send a message via GMAIL"""
        if recipients is None:
            recipients = ['vasya@email.com', 'petya@email.com']
        message = MIMEMultipart()
        message['From'] = self.login
        message['To'] = ', '.join(recipients)
        message['Subject'] = subject
        message.attach(MIMEText(message_text))

        mail_session = smtplib.SMTP(gmail_smtp, 587)
        mail_session.ehlo()
        mail_session.starttls()
        mail_session.ehlo()
        mail_session.login(self.login, self.__password)
        mail_session.sendmail(self.login, mail_session, message.as_string())
        mail_session.quit()

    def recieve_mail(self, gmail_type='imap.gmail.com', header=None):
        """Receive a message via GMAIL"""
        mail = imaplib.IMAP4_SSL(gmail_type)
        mail.login(self.login, self.__password)
        mail.list()
        mail.select("inbox")
        criterion = 'HEADER Subject {}'.format(lambda head: header if header else header == 'ALL')

        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'

        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        mail.logout()
        return email_message


if __name__ == '__main__':
    new_user = Mail()

