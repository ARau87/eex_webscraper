from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

class Page():

    def __init__(self, driver, **kwargs):
        self.url = kwargs['url']
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.title = kwargs['title']

    def go_to(self):
        print(self.url)
        self.driver.get(self.url)

    def wait_to_load(self):
        self.wait.until(EC.title_is(self.title))
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME,'body')))
        
        
        
        