from twilio.rest import Client

# Twilio credentials
account_sid = 'YOUR_ACCOUNT_SID'
auth_token = 'YOUR_ACCOUNT_AUTH'
client = Client(account_sid, auth_token)

# Create the call to your friend
call = client.calls.create(
    to='+18777804236',            # Your friend's number
    from_='+16086368941',         # Your Twilio number
    url='https://demo.twilio.com/welcome/voice/'  # TwiML that tells Twilio to dial you
)

print("Call SID:", call.sid)
