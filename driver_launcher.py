from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
driver_path =r"C:\Users\nares\Downloads\Task 9april\chromedriver.exe"

def driver_launchfun(url):
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get(url)
    driver.maximize_window()
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(2)
    return driver
