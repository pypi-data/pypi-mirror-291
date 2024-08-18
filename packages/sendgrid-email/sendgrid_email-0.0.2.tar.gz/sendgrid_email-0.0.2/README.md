# CommonMark Website

This is a Python package that provides the function `send_email`:

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

## Installation

    pip install sendgrid-email

## Usage

    from email.mime.application import MIMEApplication
    from sendgrid_email import send_email

    attachment = MIMEApplication(b"File contents", name="filename.txt")
    attachment['Content-Disposition'] = 'attachment; filename="filename.txt"'

    send_email(
        "Example Service",
        "recipient@example.org",
        "Re: Example Subject",
        "<h1>This is an example email</h1>",
        [attachment],
    )
