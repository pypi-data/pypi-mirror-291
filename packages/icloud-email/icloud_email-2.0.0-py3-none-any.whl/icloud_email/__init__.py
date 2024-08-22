from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from smtplib import SMTP
from ssl import create_default_context
try:
    from config import ICLOUD_USERNAME
except:
    print("Error: sendgrid-email requires ICLOUD_USERNAME to be defined in config.py")
    exit(1)
try:
    from config import ICLOUD_PASSWORD
except:
    print("Error: sendgrid-email requires ICLOUD_PASSWORD to be defined in config.py")
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
    sender = f"{service_name} <{SENDER_EMAIL_ADDRESS}>"

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(html, 'html'))
    for attachment in attachments:
        msg.attach(attachment)
    # Send it off via smtp.mail.me.com
    context = create_default_context()
    with SMTP("smtp.mail.me.com", 587) as smtp:
        smtp.starttls(context=context)
        smtp.login(ICLOUD_USERNAME, ICLOUD_PASSWORD)
        smtp.sendmail(sender, recipient, msg.as_string())
