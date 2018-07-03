from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from lib.config import Config
from lib.page_power_germany import PagePowerGermany
from lib.email_sender import EmailSender

import time
import schedule

url = 'https://www.eex-transparency.com/homepage/power/germany'

def create_driver(config):
      if config.driver == 'phantom':
            driver = webdriver.PhantomJS(executable_path=config.driver_executable)
            driver.implicitly_wait(15)
            return driver

      if config.driver == 'firefox':
            options = Options()
            #options.add_argument("--headless")
            driver = webdriver.Firefox(executable_path=config.driver_executable, firefox_options=options)
            driver.implicitly_wait(15)
            return driver

      if config.driver == 'chrome':
            driver = webdriver.Chrome(executable_path=config.driver_executable)
            driver.implicitly_wait(15)
            return driver

def load_planned_data(page):
      data = ''
      data_type = 'planned'
      while len(data) == 0:
            data = page.get_planned_data()
            time.sleep(2)

      return (data_type, data)

def load_actual_data(page):
      data = ''
      data_type = 'actual'
      while len(data) == 0:
            data = page.get_actual_data()
            time.sleep(2)

      return (data_type, data)

def load_weather_data(page):
      data = ''
      data_type = 'weather'
      while len(data) == 0:
            data = page.get_weather_data()
            time.sleep(2)

      return (data_type, data)


def save_data(data, config):
      t = time.time()
      t = time.strftime('%H%M_%d%m%Y')
      filename = config.save_path + '/' + data[0] + '_' + t + '.json'
      with open(filename, 'w') as file:
        file.write(data[1])
      return filename

def main(config):
      email_sender = EmailSender(config)
      driver = create_driver(config)

      power_page = PagePowerGermany(driver)
      data = load_planned_data(power_page)
      planned_data_file = save_data(data, config)
      data = load_actual_data(power_page)
      actual_data_file = save_data(data, config)
      
      #email_sender.send([planned_data_file, actual_data_file])
      driver.quit()   


if __name__ == '__main__':
 
  config = Config('config.txt')
  config.print_options()
  main(config)
  #schedule.every().day.at(config.time).do(main, config)

  #while True:
        #schedule.run_pending()
        #time.sleep(60)

  

