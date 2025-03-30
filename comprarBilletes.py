import time
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

ser = "julianix882@gmail.com"
password = "CHAQUETA"

options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")
'''
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
'''
driver = webdriver.Chrome(options=options)
driver.get("https://booking.avanzabus.com/user/bonos.php")

WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "input_password"))
            )
WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "input_login"))
            )