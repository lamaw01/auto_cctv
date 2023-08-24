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

next_page = '//*[@id="config"]/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/div/div/button[2]/i'

timeout = 6

x = 0
y = 390

#list of cam to ignore
#add more ip if desired to be ignore
_cam_list = ['192.168.69.109','	192.168.69.120','192.168.69.121']
#'172.21.0.74','172.21.0.216,'192.168.69.107','192.168.69.108','192.168.69.111'
_to_ignore_log = []

#open nvr 200
def open_admin_200():
   nvr_ip = 'http://172.21.0.200'
   try:
      chrome_options = Options()
      #chrome_options.add_argument("--incognito")
      chrome_options.add_experimental_option("detach", True)
      global driver_200
      # driver_200 = webdriver.Chrome(options=chrome_options)
      driver_200 = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
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
      # driver_200.close()
      driver_200.quit()
      open_admin_200()

def login_200():
   print('logging in 200...')
   nvr_username = 'admin'
   nvr_password = 'uc-1enviar'
   time.sleep(timeout)
   wait_for_element_load(login_200_button_element,driver_200)
   driver_200.find_element(By.XPATH,username_input_element).send_keys(nvr_username)
   driver_200.find_element(By.XPATH,password_input_element).send_keys(nvr_password)
   driver_200.find_element(By.XPATH,login_200_button_element).click()
   wait_for_element_load(config_element,driver_200)
   driver_200.find_element(By.XPATH,config_element).click()
   wait_for_element_load(camera_management_element,driver_200)
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
         if is_tail is True:
            print('navigate to 2nd page...')
            try:
               driver_200.find_element(By.XPATH,next_page).click()
               scan2()
            except Exception as e:
               print('no 2nd page...')
   print('standby...')

#check table if there's offline
def scan2():
   print('scanning2...')
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
           print('rebooting2...',camera_name)
           reboot(camera_ip,camera_name)
      except Exception as e:
         is_tail = True
         print('scan2',e)
   print('standby2...')

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
      if not _to_ignore_log.__contains__(ip):
         insert_log(ip,name,status,200)

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

open_admin_200()
