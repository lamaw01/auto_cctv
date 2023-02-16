from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import yaml
import time

#open yml file
conf = yaml.safe_load(open('credentials.yml'))

#web elements
login_button_element = '//*[@id="login"]/table/tbody/tr/td[2]/div/div[5]/button'
config_element = '//*[@id="nav"]/li[5]/a'
maintenance_element = '//*[@id="menu"]/div/div[2]/div[3]/span'
reboot_button_element = '//*[@id="maintainUpgrade"]/div[1]/div[2]/span[1]/button'
reboot_ok_button_element = '//*[@id="config"]/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button[1]'
camera_management_element = '//*[@id="menu"]/div/div[2]/div[5]/span'
camera_status_element = '//*[@id="tableDigitalChannels"]/div/div[2]/div[1]/span[8]'

table_row = '//*[@id="tableDigitalChannels"]/div/div[2]/div'
table_row_ip = '//*[@id="tableDigitalChannels"]/div/div[2]/div[2]/span[4]'

error_login_element = '//*[@id="login"]/table/tbody/tr/td[2]/div/div[2]/div/label'

#open offline ipcam viewer
def open_nvr_viewer():

   #credentials of nvr
   nvr_credentials = 'nvr'
   nvr_username = conf[nvr_credentials]['username']
   nvr_password = conf[nvr_credentials]['password']
   nvr_ip = conf[nvr_credentials]['ip']

   camera_count = 0

   try:
      chrome_options = Options()
      chrome_options.add_argument("--incognito")
      chrome_options.add_experimental_option("detach", True)
      nvr_driver = webdriver.Chrome(options=chrome_options)

      nvr_driver.get(nvr_ip)

      wait_for_element_load(login_button_element,nvr_driver)
      nvr_driver.find_element(By.ID,'username').send_keys(nvr_username)
      nvr_driver.find_element(By.ID,'password').send_keys(nvr_password)
      nvr_driver.find_element(By.XPATH,login_button_element).click()

      wait_for_element_load(config_element,nvr_driver)
      nvr_driver.find_element(By.XPATH, config_element).click()

      wait_for_element_load(camera_management_element,nvr_driver)
      nvr_driver.find_element(By.XPATH,camera_management_element).click()
      time.sleep(3)

      nvr_driver.find_element(By.XPATH,table_row + str([camera_count+1])).click()
      camera_count = camera_count + 1
      print('CAMERA COUNT ',camera_count)

      ip_selected = nvr_driver.find_element(By.XPATH,table_row+ str([camera_count])  + '/span[4]').text
      ip_link = 'http://' + ip_selected
      time.sleep(3)

      reboot_cam(ip_link)
     

   except Exception as e:
      print(e)

#open ip cam and try reboot
def reboot_cam(ip):


   #credentials of selected ip cam
   username = 'admin'
   #password = conf[ip]['password']
   password1 = '123456@ad'
   password2 = 'scores135792468'

   try:
      chrome_options = Options()
      chrome_options.add_argument("--incognito")
      chrome_options.add_experimental_option("detach", True)
      driver = webdriver.Chrome(options=chrome_options)
      #driver.set_window_size(1680, 900)
      
      driver.get(ip)

      wait_for_element_load(login_button_element,driver)

      driver.find_element(By.ID,'username').send_keys(username)
      driver.find_element(By.ID,'password').send_keys(password1)
      driver.find_element(By.XPATH,login_button_element).click()

      is_error_login = driver.find_element(By.XPATH,error_login_element).is_displayed()
      print('nakita ba', is_error_login)

      if is_error_login == False:
         driver.find_element(By.ID,'username').send_keys(username)
         driver.find_element(By.ID,'password').send_keys(password2)
         driver.find_element(By.XPATH,login_button_element).click()

      time.sleep(3)
      wait_for_element_load(config_element,driver)
      driver.find_element(By.XPATH, config_element).click()

      wait_for_element_load(maintenance_element,driver)
      driver.find_element(By.XPATH,maintenance_element).click()

      #wait_for_element_load(reboot_button_element,driver)
      #driver.find_element(By.XPATH,reboot_button_element).click()

      #wait_for_element_load(reboot_ok_button_element,driver)
      #driver.find_element(By.XPATH,reboot_ok_button_element).click()
      time.sleep(3)
      
      #close current browser
      #driver.close()

   except Exception as e:
      print(e)

#function to ensure web element loaded
def wait_for_element_load(element, driver):
   timeoutSec = 10
   element_wait_load = EC.presence_of_element_located((By.XPATH, element))
   WebDriverWait(driver, timeoutSec).until(element_wait_load)
   time.sleep(3)

#open_nvr_viewer()
reboot_cam('http://192.168.63.115')