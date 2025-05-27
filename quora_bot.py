from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://quora.com/search?q=YOUR_KEYWORD")
questions = driver.find_elements_by_css_selector(".q-text")

for q in questions[:5]:
    q.click()
    answer_box = driver.find_element_by_css_selector(".ql-editor")
    answer_box.send_keys(f"Here's a detailed guide: {your_url}")
    driver.find_element_by_xpath("//button[text()='Post']").click()
