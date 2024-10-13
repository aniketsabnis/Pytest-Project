import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# python -m smtpd -n -c DebuggingServer localhost:1025

def send_email(subject, body, to_email, from_email, smtp_server, smtp_port, username=None, password=None, attachment_path=None):
    try:
        # Create a MIMEMultipart message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach the email body
        msg.attach(MIMEText(body, 'plain'))   

        # Attach a file (if provided)
        if attachment_path:
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={attachment_path.split("/")[-1]}')
                msg.attach(part)

        # Connect to the SMTP server
        if(smtp_port != 1025):
            print("For all other emails")
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  # Use TLS
                server.login(username, password)  # Log in
                server.send_message(msg)  # Send the email
        else:
            print("For all local python email")
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.sendmail(msg['From'], [msg['To']], msg.as_string())

        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {str(e)}")

# Example usage
if __name__ == "__main__":
    # send_email(
    #     subject="Test Email",
    #     body="This is a test email from Python!",
    #     to_email="aniket.n.sabnis@gmail.com",
    #     from_email="your_email@example.com",
    #     smtp_server="smtp.example.com",
    #     smtp_port=587,  # Use 465 for SSL
    #     username="your_email@example.com",
    #     password="your_password",
    #     attachment_path=None  # Provide path to attachment if needed
    # )
    send_email(
        subject="Test Email",
        body="This is a test email from Python!",
        to_email="aniket.n.sabnis@gmail.com",
        from_email="your_email@example.com",  # Change to a valid email for local server
        smtp_server='localhost',
        smtp_port=1025,
        username=None,  # Not needed for local server
        password=None,  # Not needed for local server
        attachment_path=None  # Provide path to attachment if needed
    )
