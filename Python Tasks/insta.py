from instagrapi import Client

cl = Client()
cl.login("USERNAME", "PASSWORD")  #ENTER YOUR OWN USERNAME AND PASSWORD

cl.photo_upload(
    path="YOUR FILE PATH",
    caption="Hello from Python! 🌟"
)