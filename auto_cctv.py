from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from time import ctime

#web elements
login_button_element = '//*[@id="login"]/table/tbody/tr/td[2]/div/div[5]/button'
config_element = '//*[@id="nav"]/li[5]/a'
maintenance_element = '//*[@id="menu"]/div/div[2]/div[3]/span'
reboot_button_element = '//*[@id="maintainUpgrade"]/div[1]/div[2]/span[1]/button'
reboot_ok_button_element = '//*[@id="config"]/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button[1]'
camera_management_element = '//*[@id="menu"]/div/div[2]/div[5]/span'

#base row
table_row = '//*[@id="tableDigitalChannels"]/div/div[2]/div'
#/span[3] -> camera name
camera_name_element = '//*[@id="tableDigitalChannels"]/div/div[2]/div[1]/span[3]'
#/span[4] -> camera ip
camera_ip_element = '//*[@id="tableDigitalChannels"]/div/div[2]/div[1]/span[4]'
#/span[8] -> camera status
camera_status_element = '//*[@id="tableDigitalChannels"]/div/div[2]/div[1]/span[8]'


global timeout
timeout = 5

#open nvr viewer
def open_viewer():
   #credentials of nvr
   nvr_ip = 'http://172.21.0.198/'
   nvr_username = 'admin'
   nvr_password = 'uc-1enviar'

   try:
      chrome_options = Options()
      chrome_options.add_argument("--incognito")
      chrome_options.add_experimental_option("detach", True)
      nvr_driver = webdriver.Chrome(options=chrome_options)
      nvr_driver.set_window_size(1200, 1000)
      nvr_driver.get(nvr_ip)

      wait_for_element_load(login_button_element,nvr_driver)
      nvr_driver.find_element(By.ID,'username').send_keys(nvr_username)
      nvr_driver.find_element(By.ID,'password').send_keys(nvr_password)
      nvr_driver.find_element(By.XPATH,login_button_element).click()

      wait_for_element_load(config_element,nvr_driver)
      nvr_driver.find_element(By.XPATH, config_element).click()

      wait_for_element_load(camera_management_element,nvr_driver)
      nvr_driver.find_element(By.XPATH,camera_management_element).click()
      time.sleep(timeout)

      #run 24/7
      while True:
         cycle_table(nvr_driver)
         #refresh page
         nvr_driver.refresh()
         time.sleep(60)

   except Exception as e:
      print('error opening viewer',e)

#check table if there's offline
def cycle_table(driver):
   camera_count = 0
   is_tail = False
   while is_tail is False:
      try:
         #click row
         driver.find_element(By.XPATH,table_row + str([camera_count+1])).click()
         camera_count = camera_count + 1
         print('camera count',camera_count)
         
         #get name and status of current row
         camera_name = driver.find_element(By.XPATH,table_row + str([camera_count]) + '/span[3]').text
         camera_status = driver.find_element(By.XPATH,table_row + str([camera_count]) + '/span[8]').text
         
         #if offline, get ip and reboot
         if camera_status != 'Online':
            #select ip element and reboot
            ip_selected = driver.find_element(By.XPATH,table_row + str([camera_count])  + '/span[4]').text
            ip_link = 'http://' + ip_selected

            write_logs(camera_name)
            reboot(ip_link)

      except Exception as e:
         is_tail = True
         print(is_tail,e)
    
   print('camera limit count ',camera_count)

#open ip cam and try reboot
def reboot(ip):
   try:
      chrome_options = Options()
      chrome_options.add_argument("--incognito")
      chrome_options.add_experimental_option("detach", True)
      driver = webdriver.Chrome(options=chrome_options)

      #set position and size
      driver.set_window_size(1200, 1000)
      driver.set_window_position(350, 20, windowHandle='current')

      driver.get(ip)

      wait_for_element_load(login_button_element,driver)
      login(driver)
      time.sleep(timeout)

      wait_for_element_load(config_element,driver)
      driver.find_element(By.XPATH, config_element).click()

      wait_for_element_load(maintenance_element,driver)
      driver.find_element(By.XPATH,maintenance_element).click()

      wait_for_element_load(reboot_button_element,driver)
      driver.find_element(By.XPATH,reboot_button_element).click()

      wait_for_element_load(reboot_ok_button_element,driver)
      driver.find_element(By.XPATH,reboot_ok_button_element).click()
   
      time.sleep(timeout)
      
   except Exception as e:
      print('reboot camera error',e)
   
   finally:
      #close current browser
      driver.close()

#write logs
def write_logs(cam_name):
   is_file_exist = os.path.isfile('logs.txt')
   if is_file_exist:
      with open('logs.txt', 'a') as f:
         f.write('\n' + cam_name + ' -> ' + ctime())
   else:
      with open('logs.txt', 'w') as f:
         f.write('\n' + cam_name + ' -> ' + ctime())


def login(driver):
   #credentials of selected ip cam
   username = 'admin'
   password1 = '123456@ad'
   password2 = 'scores135792468'

   pre_login_url = driver.current_url
   #login using first password
   driver.find_element(By.ID,'username').send_keys(username)
   driver.find_element(By.ID,'password').send_keys(password1)
   driver.find_element(By.XPATH,login_button_element).click()
   
   time.sleep(timeout)
   post_login_url = driver.current_url
   #check if password is error
   if pre_login_url == post_login_url:
      driver.find_element(By.ID,'username').send_keys(username)
      driver.find_element(By.ID,'password').send_keys(password2)
      driver.find_element(By.XPATH,login_button_element).click()

#function to ensure web element loaded
def wait_for_element_load(element, driver):
   element_wait_load = EC.presence_of_element_located((By.XPATH, element))
   WebDriverWait(driver, 10).until(element_wait_load)
   time.sleep(timeout)

open_viewer()
#reboot('http://192.168.69.107')