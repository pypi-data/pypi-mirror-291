# icloud-email

This is a Python package that provides the function `send_email`:

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

## Installation

    pip install icloud-email

## Usage

    from email.mime.application import MIMEApplication
    from icloud_email import send_email

    attachment = MIMEApplication(b"File contents", name="filename.txt")
    attachment['Content-Disposition'] = 'attachment; filename="filename.txt"'

    send_email(
        "Example Service",
        "recipient@example.org",
        "Re: Example Subject",
        "<h1>This is an example email</h1>",
        [attachment],
    )
