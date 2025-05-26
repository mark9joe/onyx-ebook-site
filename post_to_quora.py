from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time, json, random

# Load a random post
with open("content_pool.json", "r", encoding="utf-8") as f:
    post = random.choice(json.load(f))

EMAIL = "your_email@example.com"
PASSWORD = "your_password"

# Setup
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.quora.com/")

# Login
time.sleep(3)
driver.find_element(By.NAME, "email").send_keys(EMAIL)
driver.find_element(By.NAME, "password").send_keys(PASSWORD + Keys.RETURN)

time.sleep(5)  # wait for login

# Go to your Space or Profile (adjust this URL)
driver.get("https://www.quora.com/profile/YOUR-PROFILE/")

time.sleep(4)
driver.find_element(By.XPATH, "//span[text()='Add Post']").click()

time.sleep(3)
driver.find_element(By.XPATH, "//div[contains(@class, 'q-box')]").send_keys(
    f"{post['title']}\n\n{post['description']}\n\nRead more: {post['url']}"
)

time.sleep(2)
driver.find_element(By.XPATH, "//span[text()='Post']").click()

print("✅ Quora post submitted.")
time.sleep(5)
driver.quit()
