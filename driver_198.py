from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import bridge

#web elements
login_button_element = '//*[@id="login"]/table/tbody/tr/td[2]/div/div[5]/button'
config_element = '//*[@id="nav"]/li[5]/a'
camera_management_element = '//*[@id="menu"]/div/div[2]/div[5]/span'

#base row
table_row = '//*[@id="tableDigitalChannels"]/div/div[2]/div'
#/span[3] -> camera name
#/span[4] -> camera ip
#/span[8] -> camera status

timeout = 5
x = 0
y = 10

#list of cam to scan
_cam_list = ['192.168.62.114','172.21.0.223','172.21.0.221','192.168.74.115','192.168.72.116','172.21.0.224','172.21.0.243','192.168.60.139','192.168.69.110','192.168.76.108','192.168.77.115','192.168.64.111','172.21.0.254','192.168.60.114']

#open nvr 198
def open_admin_198():
   nvr_ip = 'http://172.21.0.198/'
   try:
      chrome_options = Options()
      #chrome_options.add_argument("--incognito")
      chrome_options.add_experimental_option("detach", True)
      global driver_198
      driver_198 = webdriver.Chrome(options=chrome_options)
      #set position and size
      driver_198.set_window_size(1152, 648)
      driver_198.set_window_position(x, y)
      driver_198.get(nvr_ip)
      login_198()
      #run 24/7
      while True:
         scan()
         #refresh page
         driver_198.refresh()
         time.sleep(timeout)
         #check if viewer got logged out
         if driver_198.current_url != 'http://172.21.0.198/doc/page/config.asp':
            print('logged out...', True)
            login_198()
         #wait 2:00 sesc before refresh page
         time.sleep(120)
   except Exception as e:
      print('error admin 198',e)
      driver_198.close()
      open_admin_198()

def login_198():
   print('logging in 198...')
   nvr_username = 'admin'
   nvr_password = 'uc-1enviar'
   bridge.wait_for_element_load(login_button_element,driver_198)
   driver_198.find_element(By.ID,'username').send_keys(nvr_username)
   driver_198.find_element(By.ID,'password').send_keys(nvr_password)
   driver_198.find_element(By.XPATH,login_button_element).click()
   bridge.wait_for_element_load(config_element,driver_198)
   driver_198.find_element(By.XPATH, config_element).click()
   bridge.wait_for_element_load(camera_management_element,driver_198)
   driver_198.find_element(By.XPATH,camera_management_element).click()
   time.sleep(timeout)

#check table if there's offline
def scan():
   print('scanning...')
   camera_count = 0
   is_tail = False
   while is_tail is False:
      try:
         #click row
         driver_198.find_element(By.XPATH,table_row + str([camera_count+1])).click()
         camera_count = camera_count + 1
         #get name and status of current row
         global camera_name
         camera_name = driver_198.find_element(By.XPATH,table_row + str([camera_count]) + '/span[3]').text
         global camera_ip
         camera_ip = driver_198.find_element(By.XPATH,table_row + str([camera_count])  + '/span[4]').text
         camera_status = driver_198.find_element(By.XPATH,table_row + str([camera_count]) + '/span[8]').text
         #if offline, get ip and reboot
         if _cam_list.__contains__(camera_ip) and camera_status != 'Online':
            bridge.reboot(camera_ip,camera_name,x,y,'198')
      except Exception as e:
         is_tail = True
         print('error scan',e)
   print('standby...')

open_admin_198()