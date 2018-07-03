import smtplib

from os.path import basename

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

class EmailSender(object):
    def __init__(self, config):
        super (EmailSender, self).__init__()

        self.server = config.email_server
        self.port = config.email_server_port
        self.username = config.email_user
        self.password = config.email_password
        self.receiver = config.email_receiver

    def send(self, files):
              
        txt = '''
        Got another set of data from https://www.eex-transparency.com/homepage/power/germany. Check out the attachments!\n
        Please note that the data is NOT from today but from yesterday! Use the timestamps inside of the json files.
        '''
        
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = self.receiver
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = 'eex-transparency data'
        msg.attach(MIMEText(txt))

        for file in files or []:
            with open(file, 'rb') as f:
                part = MIMEApplication(f.read(), Name=basename(file))
            part['Content-Disposition'] = 'attachment; filename="%s"' %basename(file)
            msg.attach(part)


        try:
            if self.port == 465:
                server = smtplib.SMTP_SSL(self.server, self.port)
                server.ehlo()
                server.login(self.username, self.password)
                server.sendmail(self.username, self.receiver, msg.as_string())
                server.close()
                print('successfully sent the mail')
            if self.port == 587:
                server = smtplib.SMTP(self.server, self.port)
                server.ehlo()
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.username, self.receiver, msg.as_string())
                server.close()
                print('successfully sent the mail')
        except:
            print("failed to send mail")

        

        