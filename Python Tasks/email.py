import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg['Subject'] = 'Test Email'
msg['From'] = 'xxxxx@gmail.com'
msg['To'] = 'yyyyy@gmail.com'
msg.set_content('Hello! This is a test email sent using Python without any attachments.')

# Send the email using Gmail's SMTP server
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login('xxxxx@gmail.com', 'xyz')  # Use your App Password here
    smtp.send_message(msg)

print("✅ Email sent successfully!")