from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import bridge
import requests
from db_connect import insert_log

#web elements for page 200
username_input_element = '//*[@id="portal"]/div/div/div/div[2]/div/div/form/div[1]/div/div/input'
password_input_element = '//*[@id="portal"]/div/div/div/div[2]/div/div/form/div[2]/div/div/input'
login_200_button_element = '//*[@id="portal"]/div/div/div/div[2]/div/div/form/div[4]/div/button'
config_element = '//*[@id="preivew-container"]/div[1]/ul/li[5]/a'
camera_management_element = '//*[@id="config"]/div[2]/div[1]/div/div[1]/div/div/div/div/ul/div[2]/li/ul/li[5]/span'

#tr[1] -> row index
table_row = '//*[@id="config"]/div[2]/div[2]/div/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div/table/tbody/tr'
#/td[8]/div/text() -> status
#/td[4]/div/div -> ip
#/td[3]/div/div -> name

timeout = 5
x = 770
y = 390

#list of cam to ignore
_cam_list = ['172.21.0.216','172.21.0.74']

#open nvr 200
def open_admin_200():
   nvr_ip = 'http://172.21.0.200/'
   try:
      chrome_options = Options()
      #chrome_options.add_argument("--incognito")
      chrome_options.add_experimental_option("detach", True)
      global driver_200
      driver_200 = webdriver.Chrome(options=chrome_options)
      #set position and size
      driver_200.set_window_size(1152, 648)
      driver_200.set_window_position(x, y)
      driver_200.get(nvr_ip)
      login_200()
      #run 24/7
      while True:
         scan()
         #check if viewer got logged out
         if driver_200.current_url == 'http://172.21.0.200/doc/index.html#/portal/login':
            print('logged out...', True)
            login_200()
         #wait 5:00 mins before refresh page
         time.sleep(300)
         #refresh page
         driver_200.refresh()
         time.sleep(30)
   except Exception as e:
      print('admin 200',e)
      driver_200.close()
      open_admin_200()

def login_200():
   print('logging in 200...')
   nvr_username = 'admin'
   nvr_password = 'uc-1enviar'
   bridge.wait_for_element_load(login_200_button_element,driver_200)
   driver_200.find_element(By.XPATH,username_input_element).send_keys(nvr_username)
   driver_200.find_element(By.XPATH,password_input_element).send_keys(nvr_password)
   driver_200.find_element(By.XPATH,login_200_button_element).click()
   bridge.wait_for_element_load(config_element,driver_200)
   driver_200.find_element(By.XPATH,config_element).click()
   bridge.wait_for_element_load(camera_management_element,driver_200)
   driver_200.find_element(By.XPATH,camera_management_element).click()
   time.sleep(timeout)

#check table if there's offline
def scan():
   print('scanning...')
   camera_count = 0
   is_tail = False
   while is_tail is False:
      try:
         #click row
         driver_200.find_element(By.XPATH,table_row + str([camera_count+1])).click()
         camera_count = camera_count + 1
         #get name and status of current row
         camera_name = driver_200.find_element(By.XPATH,table_row + str([camera_count]) + '/td[3]/div/div').text
         camera_ip = driver_200.find_element(By.XPATH,table_row + str([camera_count])  + '/td[4]/div/div').text
         camera_status = driver_200.find_element(By.XPATH,table_row + str([camera_count]) + '/td[8]/div').text
         #if offline, get ip and reboot
         if not _cam_list.__contains__(camera_ip) and camera_status != 'Online':
           print('rebooting...',camera_name)
           reboot(camera_ip,camera_name)
      except Exception as e:
         is_tail = True
         print('scan',e)
   print('standby...')

#reboot ip cam using url
def reboot(ip,name):
   status = True
   try:
      #http://admin:scores135792468@192.168.64.112/ISAPI/System/reboot
      response = requests.put('http://'+ip+'/ISAPI/System/reboot',auth=('admin','123456@ad'))
      print('1st req',response.status_code)
      time.sleep(10)
      if response.status_code != 200:
         time.sleep(10)
         response = requests.put('http://'+ip+'/ISAPI/System/reboot',auth=('admin','scores135792468'))
         print('2st req',response.status_code)
   except Exception as e:
      print('reboot',e)
      status = False
   finally:
      insert_log(ip,name,status,200)

open_admin_200()