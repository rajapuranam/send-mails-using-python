# HTML and plaintext emails through Python and Gmail

from smtplib import SMTP, SMTPAuthenticationError, SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import getpass


# host and port for Gmail
host = "smtp.gmail.com"
port = 587

# your mail id and password
fromEmail = input('Enter your mail id : ')
password = getpass.getpass('Enter password for {} : '.format(fromEmail))

toList = ["recipient_1@gmail.com", "recipient_2@gmail.com"]

try:
    # setting connection and logging to account
    conn = SMTP(host, port)
    conn.ehlo()
    conn.starttls()
    conn.login(fromEmail, password)

    # 'alternative' used below is the standard way of calling an html
    # setting subject line, from address and to address
    theMessage = MIMEMultipart("alternative")
    theMessage['Subject'] = "Subject Line"
    theMessage['From'] = fromEmail
    theMessage['To'] = toList[0]

    # plain text as well as html rendered text
    plainText = "Sending sample message using python"
    htmltext = open('index.html', 'r').read()

    part1 = MIMEText(plainText, 'plain')
    part2 = MIMEText(htmltext, 'html')

    # adding attachments to mail
    filename = "sample.txt"
    filepath = os.path.join(os.getcwd(), filename)
    attachment = open(filepath, "rb")
    attach = MIMEBase('application', 'octet-stream')
    attach.set_payload((attachment).read())
    encoders.encode_base64(attach)
    attach.add_header('Content-Disposition',
                      "attachment; filename= %s" % filename)

    # attaching various parts to mail
    theMessage.attach(part1)
    theMessage.attach(part2)
    theMessage.attach(attach)

    # sending mail
    conn.sendmail(fromEmail, toList, theMessage.as_string())

    print('Email sent successfully!!')

    # closing connection
    conn.quit()

except SMTPAuthenticationError:
    print("Couldnot login!!")
    print("Chech your mail id and password!!")
except SMTPException:
    print("SMTP connection error!! Try again.")
except:
    print("An error occured!!")