from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Configure Chrome
def get_driver(mobile=False):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    if mobile:
        mobile_emulation = { "deviceName": "Pixel 2" }
        options.add_experimental_option("mobileEmulation", mobile_emulation)
    return webdriver.Chrome(options=options)

def post_instagram(username, password, caption):
    driver = get_driver(mobile=True)
    driver.get("https://www.instagram.com/accounts/login/")

    time.sleep(5)
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password + Keys.ENTER)

    time.sleep(8)
    # Instagram doesn't allow direct post upload via web without hacks.
    print("❌ Instagram posting is blocked in desktop mode. Use mobile app or API workaround.")
    driver.quit()

def post_twitter(username, password, tweet):
    driver = get_driver()
    driver.get("https://twitter.com/login")

    time.sleep(5)
    driver.find_element(By.NAME, "text").send_keys(username + Keys.ENTER)
    time.sleep(3)
    driver.find_element(By.NAME, "password").send_keys(password + Keys.ENTER)

    time.sleep(6)
    tweet_box = driver.find_element(By.XPATH, "//div[@aria-label='Tweet text']")
    tweet_box.click()
    tweet_box.send_keys(tweet)

    time.sleep(1)
    driver.find_element(By.XPATH, "//div[@data-testid='tweetButtonInline']").click()

    print("✅ Tweet posted!")
    time.sleep(5)
    driver.quit()

def post_facebook(username, password, post_text):
    driver = get_driver()
    driver.get("https://www.facebook.com/")

    time.sleep(5)
    driver.find_element(By.ID, "email").send_keys(username)
    driver.find_element(By.ID, "pass").send_keys(password + Keys.ENTER)

    time.sleep(8)
    post_box = driver.find_element(By.XPATH, "//div[contains(text(),'on your mind')]")
    post_box.click()

    time.sleep(4)
    active_box = driver.find_element(By.XPATH, "//div[@aria-label='Create a post']//div[@role='textbox']")
    active_box.send_keys(post_text)

    time.sleep(2)
    post_button = driver.find_element(By.XPATH, "//div[@aria-label='Create a post']//div[@aria-label='Post']")
    post_button.click()

    print("✅ Facebook post done!")
    time.sleep(5)
    driver.quit()

def post_linkedin(username, password, post_text):
    driver = get_driver()
    driver.get("https://www.linkedin.com/login")

    time.sleep(5)
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password + Keys.ENTER)

    time.sleep(6)
    driver.find_element(By.CLASS_NAME, "share-box-feed-entry__trigger").click()
    time.sleep(3)

    editor = driver.find_element(By.CLASS_NAME, "ql-editor")
    editor.send_keys(post_text)

    time.sleep(2)
    driver.find_element(By.XPATH, "//button/span[text()='Post']").click()

    print("✅ LinkedIn post done!")
    time.sleep(5)
    driver.quit()

if _name_ == "_main_":
    # Replace with your actual credentials (preferably load from .env or input securely)
    USER = "your_username"
    PASS = "your_password"
    TEXT = "🚀 Hello from Selenium automation!"

    # Uncomment the ones you want to use
    post_instagram(USER, PASS, TEXT)
    post_twitter(USER, PASS, TEXT)
    post_facebook(USER, PASS, TEXT)
    post_linkedin(USER, PASS, TEXT)