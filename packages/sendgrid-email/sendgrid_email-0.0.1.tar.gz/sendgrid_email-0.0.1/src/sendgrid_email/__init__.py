from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from smtplib import SMTP_SSL
try:
    from config import SENDGRID_API_KEY
except:
    print("Error: sendgrid-email requires SENDGRID_API_KEY to be defined in config.py")
    exit(1)
try:
    from config import SENDER_EMAIL_ADDRESS
except:
    print("Error: sendgrid-email requires SENDER_EMAIL_ADDRESS to be defined in config.py")
    exit(1)

#
# Put an email together in MIMEMultipart and send it off.
#
def send_email(service_name, recipient, subject, html, attachments=[]):
    sender = f"{service_name} <{SENDER_EMAIL_ADDRESS>"

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(html, 'html'))
    for attachment in attachments:
        msg.attach(attachment)
    # Send it off via smtp.sendgrid.net
    with SMTP_SSL("smtp.sendgrid.net", 465) as smtp:
        smtp.login("apikey", SENDGRID_API_KEY)
        smtp.sendmail(sender, recipient, msg.as_string())
