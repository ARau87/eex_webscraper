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
import requests
import os
import zipfile
import shutil

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

def load_weather_data(city, config):
      response = requests.get('https://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + config.weather_api_key)
      return (city, response.text)

def save_weather_data(data, config):
      t = time.time()
      t = time.strftime('%H%M')
      d = time.time()
      d = time.strftime('%d%m%Y')
      filename = data[0] + '_weather_' + t 
      if os.path.isdir(config.save_path + '/' + data[0]):
            if os.path.isdir(config.save_path + '/' + data[0] + '/' + d):
                  with open(config.save_path + '/' + data[0] + '/' + d + '/' + filename, 'w') as file:
                        file.write(data[1])
            else:
                  os.makedirs(config.save_path + '/' + data[0] + '/' + d)
                  save_weather_data(data, config)
      else:
            os.makedirs(config.save_path + '/' + data[0])
            save_weather_data(data, config)


def save_data(data, config):
      t = time.time()
      t = time.strftime('%H%M_%d%m%Y')
      filename = config.save_path + '/' + data[0] + '_' + t + '.json'
      with open(filename, 'w') as file:
        file.write(data[1])
      return filename

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def create_zip(dirname):
      d = time.time()
      d = time.strftime('%d%m%Y')
      zip_filename = 'data_' + d + '.zip'
      zip_file = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
      zipdir(os.path.relpath('./' + dirname), zip_file)
      zip_file.close()
      return zip_filename

def delete_old_data(dirname):
      shutil.rmtree(dirname)
      os.makedirs(dirname)
      

def job_weather(config):
      save_weather_data(load_weather_data('Muenchen', config), config)
      save_weather_data(load_weather_data('Essen', config), config)
      save_weather_data(load_weather_data('Berlin', config), config)

def job_main(config):
      email_sender = EmailSender(config)
      driver = create_driver(config)

      power_page = PagePowerGermany(driver)
      data = load_planned_data(power_page)
      planned_data_file = save_data(data, config)
      data = load_actual_data(power_page)
      actual_data_file = save_data(data, config)
      zip_file = create_zip(config.save_path)
      
      email_sender.send([zip_file])
      delete_old_data(config.save_path)
      driver.quit()

      # After clearing the data invoke weather job for consistency reasons as 
      # it may be the case the weather ran before
      job_weather(config)


if __name__ == '__main__':
 
  config = Config('config.txt')
  config.print_options()
  schedule.every().hour.do(job_weather, config)
  schedule.every().day.at(config.time).do(job_main, config)

  while True:
        schedule.run_pending()
        time.sleep(60)