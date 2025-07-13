import pywhatkit
import random

fun_messages = [
    "🌞 Good Morning! Let's rule the world today! 😎💪",
    "🐍 Python says: Hello there! 🧠🚀",
    "⚠ Alert: You've received a message from the coolest coder alive 😎",
    "🎉 Surprise! This message was sent by a bot. Resistance is futile. 🤖",
    "👀 Who said Python can't chat? Here I am!"
]

pywhatkit.sendwhatmsg_instantly(
    phone_no="+919876543210",  #ENTER YOUR PHONE NUMBER
    message=random.choice(fun_messages),
    wait_time=10,
    tab_close=True
)