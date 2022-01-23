from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ['enable-automation'])
driver = webdriver.Chrome(options=options)
url = "https://docs.google.com/forms/d/e/1FAIpQLScLhHgD5pMnwxl8JyRfXXsJekF8_pDG36XtSEwaGsFdU2egyw/viewform"
try:
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    input_field = driver.find_element(By.CLASS_NAME, 'exportInput')
    wait.until(EC.element_to_be_clickable(input_field))
    input_field.send_keys('Sasha')
    input_div = driver.find_element(By.CSS_SELECTOR, 'div[role="list"]')
    input_div.screenshot('input.png')
    submit_button = driver.find_element(By.CSS_SELECTOR, 'div[role="button"]')
    submit_button.click()
    wait.until(EC.url_changes(url))
    message = driver.find_element(By.CLASS_NAME, 'exportFormCard')
    message.screenshot('message.png')

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
