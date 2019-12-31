#Web scraping, file downloads, in Databricks using Python, Selenium, Chrome (headless mode), Chromedriver
#References
#https://forums.databricks.com/questions/15480/how-to-add-webdriver-for-selenium-in-databricks.html
#https://stackoverflow.com/questions/45631715/downloading-with-chrome-headless-and-selenium

import time
import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import datetime
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#check if Chrome is already installed, otherwise install it and download the corresponding version of Chrome Driver
chrome_version = os.popen('chromium-browser --product-version').read()
chrome_version
if(len(chrome_version)<2):
  #install Chrome
  print(os.popen('/usr/bin/yes | sudo apt update').read())
  print(os.popen('/usr/bin/yes | sudo apt install chromium-browser').read())
  chrome_version = os.popen('chromium-browser --product-version').read()
  #Retrieve Chrome version
  chrome_main_version = chrome_version.split('.')[0]
  print(chrome_main_version)
  #Identifiy the Chrome Driver version that matches the installed Chrome version
  cv_t = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_'+chrome_main_version
  print(cv_t)
  chromedriver_version = requests.get(cv_t).text
  print(chromedriver_version)
  #Download, unzip Chrome Driver
  system_call = 'wget https://chromedriver.storage.googleapis.com/'+chromedriver_version+'/chromedriver_linux64.zip -O /tmp/chromedriver_linux64.zip'
  print(system_call)
  print(os.system(system_call))
  print(os.popen('mkdir /tmp/chromedriver').read())
  print(os.popen('unzip /tmp/chromedriver_linux64.zip -d /tmp/chromedriver/').read())
  chrome_options = webdriver.ChromeOptions()

#Set headless Chrome options
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-popup-blocking')
chrome_driver = '/tmp/chromedriver/chromedriver'
chrome_options.add_argument('--disable-gpu')
prefs = {'download.default_directory' : '/tmp'}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_options)
download_path = '/tmp/'

#Run additional commands to allow for file downloads in headless mode
driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_path}}
command_result = driver.execute("send_command", params)
