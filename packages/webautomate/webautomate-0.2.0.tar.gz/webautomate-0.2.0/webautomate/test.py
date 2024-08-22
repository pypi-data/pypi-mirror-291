from  browser_controller import BrowserController
import time

driver = BrowserController("C:\RPA_GIT\python-libs_bots\driver\chromedriver.exe")
driver.url_browser("https://www.rpachallenge.com/")
time.sleep(8)