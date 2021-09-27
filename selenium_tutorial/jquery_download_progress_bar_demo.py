import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

os.environ['PATH'] += r"C:/SeleniumDrivers"
driver = webdriver.Chrome()
driver.get("https://www.seleniumeasy.com/test/jquery-download-progress-bar-demo.html")
driver.implicitly_wait(8)
my_element = driver.find_element_by_id("downloadButton")  # since an object will be returned, we assign it to a variable
my_element.click()

# progress_element = driver.find_element_by_class_name('progress-label')  # note that class in the web is different from the class meaning in OOP in python
# print(f"{progress_element.text == 'Completed!'}")

# instantiate the WebDriverWait class
WebDriverWait(driver, 30).until(
    EC.text_to_be_present_in_element(
        (By.CLASS_NAME, 'progress-label'),  # Element filtration
        'Complete!'  # The expected text
    )
)
