from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
import time
import requests
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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
# x = 770
# y = 390
x = 0
y = 10

#list of cam to scan
# _cam_list = ['192.168.62.114','172.21.0.223','172.21.0.221','192.168.74.115','192.168.72.116','172.21.0.224','172.21.0.243','192.168.60.139','192.168.69.110','192.168.76.108','192.168.77.115','192.168.64.111','172.21.0.254','192.168.60.114']
_cam_list = ['192.168.71.118','192.168.67.117','192.168.74.114','192.168.62.113','192.168.73.115','192.168.73.114','192.168.60.137','192.168.64.112','192.168.60.114','192.168.70.116','192.168.69.107','192.168.69.109','192.168.65.109','192.168.63.115','192.168.68.110']

#open nvr 198
def open_admin_198():
   nvr_ip = 'http://172.21.0.198'
   try:
      chrome_options = Options()
      #chrome_options.add_argument("--incognito")
      chrome_options.add_experimental_option("detach", True)
      global driver_198
      driver_198 = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
      #set position and size
      driver_198.set_window_size(1152, 648)
      driver_198.set_window_position(x, y)
      driver_198.get(nvr_ip)
      login_198()
      #run 24/7
      while True:
         scan()
         #check if viewer got logged out
         if driver_198.current_url != 'http://172.21.0.198/doc/page/config.asp':
            print('logged out...', True)
            login_198()
         #wait 5:00 sesc before refresh page
         time.sleep(300)
         #refresh page
         driver_198.refresh()
         time.sleep(30)
   except Exception as e:
      print('admin 198',e)
      #driver_198.close()
      driver_198.quit()
      open_admin_198()

def login_198():
   print('logging in 198...')
   nvr_username = 'admin'
   nvr_password = 'uc-1enviar'
   time.sleep(timeout)
   wait_for_element_load(login_button_element,driver_198)
   driver_198.find_element(By.ID,'username').send_keys(nvr_username)
   driver_198.find_element(By.ID,'password').send_keys(nvr_password)
   driver_198.find_element(By.XPATH,login_button_element).click()
   wait_for_element_load(config_element,driver_198)
   driver_198.find_element(By.XPATH, config_element).click()
   wait_for_element_load(camera_management_element,driver_198)
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
         camera_name = driver_198.find_element(By.XPATH,table_row + str([camera_count]) + '/span[3]').text
         camera_ip = driver_198.find_element(By.XPATH,table_row + str([camera_count])  + '/span[4]').text
         camera_status = driver_198.find_element(By.XPATH,table_row + str([camera_count]) + '/span[8]').text
         #if offline, get ip and reboot
         if not _cam_list.__contains__(camera_ip) and camera_status != 'Online':
            print('rebooting...',camera_name)
            reboot(camera_ip,camera_name)
      except Exception as e:
         is_tail = True
         print('scan',e)
   print('standby...')

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
      insert_log(ip,name,status,198)

#function to ensure web element loaded
def wait_for_element_load(element, driver):
   element_wait_load = EC.presence_of_element_located((By.XPATH, element))
   WebDriverWait(driver, 10).until(element_wait_load)
   time.sleep(timeout)

def insert_log(ip,name,rebooted,nvr):
   try:
      #connect db
      _mydb = mysql.connector.connect(
         host="172.21.3.25",
         database="autocctv",
         user="autocctv",
         password="autocctv123"
      )
      cursor = _mydb.cursor()
      #insert query
      sql = "INSERT INTO logs (ip,name,rebooted,nvr) VALUES (%s,%s,%s,%s)"
      val = (ip,name,rebooted,nvr)
      cursor.execute(sql, val)
      _mydb.commit()
      print(cursor.rowcount, "record inserted.")
   except mysql.connector.Error as err:
      print('insert_log',err)
   finally:
      #close connection
      cursor.close()
      _mydb.close()
      
open_admin_198()