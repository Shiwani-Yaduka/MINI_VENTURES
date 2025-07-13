from twilio.rest import Client

account_sid = 'YOUR_ACCOUNT_SID'
auth_token = 'YOUR_ACCOUNT_TOKEN'

client = Client(account_sid, auth_token)
    message = client.messages.create(
    from_='+1608xx68941', #YOUR_TWILIO_PHONE_NUMBER
    to='+916378xx1702',   #YOUR_PHONE_NUMBER
    body='Hello! This is a test message from Twilio.'
)

print("Message SID:", message.sid)