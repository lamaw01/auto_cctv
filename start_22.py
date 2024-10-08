from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
import time
import pandas as pd
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException

#web elements
login_button_element = '//*[@id="login"]/table/tbody/tr/td[2]/div/div[5]/button'

config_element = '//*[@id="nav"]/li[5]/a'

camera_management_element = '//*[@id="menu"]/div/div[2]/div[5]/span'

image_element = '//*[@id="menu"]/div/div[5]/div'

system_element = '//*[@id="menu"]/div/div[2]/div[1]'

osd = '//*[@id="image"]/li[2]'

osd_dropdown = '//*[@id="osd"]/div[1]/div[1]/span[2]/select'

camera_input = '//*[@id="osd"]/div[1]/div[2]/span[2]/div[3]/span[2]/input'

save_button = '//*[@id="osd"]/div[2]/span[2]/button/span[2]'

dropdown = '//*[@id="osd"]/div[1]/div[1]/span[2]/select/option'

maintenance = '//*[@id="menu"]/div/div[2]/div[3]/span'

reboot_button = '//*[@id="maintainUpgrade"]/div[1]/div[2]/span[1]/button'

reboot_ok_button = '//*[@id="config"]/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button[1]'

#base row
table_row = '//*[@id="tableDigitalChannels"]/div/div[2]/div'
#/span[3] -> camera name
#/span[4] -> camera ip
#/span[8] -> camera status

_cam_list = []

cam_names = ['Photo Booth 1','LOCKER 2','Ticketing area 1','Biometric','Family Gate / Locker 1','Plank Drop Release','RIVER ENTRANCE','PIRATES MARKET','Tower 1 Slipper Rack','TICKETING2','Tower 1 Release Area','CCTV MAIN GATE','MAINGATE','TENT ENTRACE','Pirates Market Counter','Commissary Extension','Events Tent','Infirmary','Olivers Cafe','Receiving','Entrance Waiting Area','Riptide Reef Release','AHOY COUNTER','PIRATES DEN','JOLLY TOWER','BRIDGE 2','HR OFFICE CCTV','FAMILY OFFICE','TURNSTYLE','Riptide Landing','BUCCANEER JRT','JT HALLWAY']
d1 = 'Photo Booth 1'
d2 = 'LOCKER 2'
d3 = 'Ticketing area 1'
d4 = 'Biometric'
d5 = 'Family Gate / Locker 1'
d6 = 'Plank Drop Release'
d7 = 'RIVER ENTRANCE'
d8 = 'PIRATES MARKET'
d9 = 'Tower 1 Slipper Rack'
d10 = 'TICKETING2'
d11 = 'Tower 1 Release Area'
d12 = 'CCTV MAIN GATE'
d13 = 'MAINGATE'
d14 = 'TENT ENTRACE'
d15 = 'Pirates Market Counter'
d16 = 'Commissary Extension'
d17 = 'Events Tent'
d18 = 'Infirmary'
d19 = "Oliver's Cafe"
d20 = 'Receiving'
d21 = 'Entrance Waiting Area'
d22 = 'Riptide Reef Release'
d23 = 'AHOY COUNTER'
d24 = 'PIRATES DEN'
d25 = 'JOLLY TOWER'
d26 = 'BRIDGE 2'
d27 = 'HR OFFICE CCTV'
d28 = 'FAMILY OFFICE'
d29 = 'TURNSTYLE'
d30 = 'Riptide Landing'
d31 = 'BUCCANEER JRT'
d32 = 'JT HALLWAY'

timeout = 5
# x = 770
# y = 390
x = 0
y = 10

def assign_excel_data():
   try:
      excel_data = pd.read_excel('cctv_data.xlsx', sheet_name='22',usecols="A")
      global d1
      d1 = excel_data.values[0][0]
      global d2
      d2 = excel_data.values[1][0]
      global d3
      d3 = excel_data.values[2][0]
      global d4
      d4 = excel_data.values[3][0]
      global d5
      d5 = excel_data.values[4][0]
      global d6
      d6 = excel_data.values[5][0]
      global d7
      d7 = excel_data.values[6][0]
      global d8
      d8 = excel_data.values[7][0]
      global d9
      d9 = excel_data.values[8][0]
      global d10
      d10 = excel_data.values[9][0]
      global d11
      d11 = excel_data.values[10][0]
      global d12
      d12 = excel_data.values[11][0]
      global d13
      d13 = excel_data.values[12][0]
      global d14
      d14 = excel_data.values[13][0]
      global d15
      d15 = excel_data.values[14][0]
      global d16
      d16 = excel_data.values[15][0]
      global d17
      d17 = excel_data.values[16][0]
      global d18
      d18 = excel_data.values[17][0]
      global d19
      d19 = excel_data.values[18][0]
      global d20
      d20 = excel_data.values[19][0]
      global d21
      d21 = excel_data.values[20][0]
      global d22
      d22 = excel_data.values[21][0]
      global d23
      d23 = excel_data.values[22][0]
      global d24
      d24 = excel_data.values[23][0]
      global d25
      d25 = excel_data.values[24][0]
      global d26
      d26 = excel_data.values[25][0]
      global d27
      d27 = excel_data.values[26][0]
      global d28
      d28 = excel_data.values[27][0]
      global d29
      d29 = excel_data.values[28][0]
      global d30
      d30 = excel_data.values[29][0]
      global d31
      d31 = excel_data.values[30][0]
      global d32
      d32 = excel_data.values[31][0]

   except Exception as e:
      print('assign_excel_data',e)

#open nvr 22
def open_admin_22():
   nvr_ip = 'http://192.168.220.22'
   try:
      chrome_options = Options()
      #chrome_options.add_argument("--incognito")
      chrome_options.add_experimental_option("detach", True)
      global driver22
      # driver22 = webdriver.Chrome(options=chrome_options)
      driver22 = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
      #set position and size
      driver22.set_window_size(800, 600)
      driver22.set_window_position(x, y)
      driver22.get(nvr_ip)
      login_22()
      time.sleep(timeout)
      assign_excel_data()
      #run 24/7
      while True:
         open_image()
         time.sleep(30)
         scan()
         #check if viewer got logged out
         if driver22.current_url != 'http://192.168.220.22/doc/page/config.asp':
            print('logged out...', True)
            login_22()
         #wait 5:00 sesc before refresh page
         time.sleep(1800)
         #refresh page
         driver22.refresh()
         time.sleep(30)
   except Exception as e:
      print('admin 22',e)
      #driver22.close()
      driver22.quit()
      open_admin_22()

def login_22():
   print('logging in 22...')
   nvr_username = 'admin'
   nvr_password = '#7s3asNVR_'
   time.sleep(timeout)
   wait_for_element_load(login_button_element,driver22)
   driver22.find_element(By.ID,'username').send_keys(nvr_username)
   driver22.find_element(By.ID,'password').send_keys(nvr_password)
   driver22.find_element(By.XPATH,login_button_element).click()
   wait_for_element_load(config_element,driver22)
   driver22.find_element(By.XPATH, config_element).click()
   time.sleep(timeout)

def open_image():
   time.sleep(timeout)
   wait_for_element_load(image_element,driver22)
   driver22.find_element(By.XPATH,image_element).click()
   time.sleep(timeout)
   wait_for_element_load(osd,driver22)
   driver22.find_element(By.XPATH,osd).click()
   time.sleep(timeout)
   loop_cams_rename()
   time.sleep(timeout)
   wait_for_element_load(system_element,driver22)
   driver22.find_element(By.XPATH,system_element).click()
   time.sleep(timeout)

def loop_cams_rename():
   select = Select(driver22.find_element(By.XPATH,osd_dropdown))
   time.sleep(timeout)
   print(len(select.options))
   for i in range(len(select.options)):
      select.select_by_index(i)
      name = driver22.find_element(By.XPATH,dropdown + str([i+1])).text
      if(name[3:4] == ']'):
         print(name)
         print(name[5:])
         switch(name[0:4],name[5:])
      else:
         print(name)
         print(name[6:])
         switch(name[0:5],name[6:])

def switch(arg,cam_name):
   if arg == "[D1]" and cam_name != d1:
      new_name(d1,arg)
   elif arg == "[D2]" and cam_name != d2:
      new_name(d2,arg)
   elif arg == "[D3]" and cam_name != d3:
      new_name(d3,arg)
   elif arg == "[D4]" and cam_name != d4:
      new_name(d4,arg)
   elif arg == "[D5]" and cam_name != d5:
      new_name(d5,arg)
   elif arg == "[D6]" and cam_name != d6:
      new_name(d6,arg)
   elif arg == "[D7]" and cam_name != d7:
      new_name(d7,arg)
   elif arg == "[D8]" and cam_name != d8:
      new_name(d8,arg)
   elif arg == "[D9]" and cam_name != d9:
      new_name(d9,arg)
   elif arg == "[D10]" and cam_name != d10:
      new_name(d10,arg)
   elif arg == "[D11]" and cam_name != d11:
      new_name(d11,arg)
   elif arg == "[D12]" and cam_name != d12:
      new_name(d12,arg)
   elif arg == "[D13]" and cam_name != d13:
      new_name(d13,arg)
   elif arg == "[D14]" and cam_name != d14:
      new_name(d14,arg)
   elif arg == "[D15]" and cam_name != d15:
      new_name(d15,arg)
   elif arg == "[D16]" and cam_name != d16:
      new_name(d16,arg)
   elif arg == "[D17]" and cam_name != d17:
      new_name(d17,arg)
   elif arg == "[D18]" and cam_name != d18:
      new_name(d18,arg)
   elif arg == "[D19]" and cam_name != d19:
      new_name(d19,arg)
   elif arg == "[D20]" and cam_name != d20:
      new_name(d20,arg)
   elif arg == "[D21]" and cam_name != d21:
      new_name(d21,arg)
   elif arg == "[D22]" and cam_name != d22:
      new_name(d22,arg)
   elif arg == "[D23]" and cam_name != d23:
      new_name(d23,arg)
   elif arg == "[D24]" and cam_name != d24:
      new_name(d24,arg)
   elif arg == "[D25]" and cam_name != d25:
      new_name(d25,arg)
   elif arg == "[D26]" and cam_name != d26:
      new_name(d26,arg)
   elif arg == "[D27]" and cam_name != d27:
      new_name(d27,arg)
   elif arg == "[D28]" and cam_name != d28:
      new_name(d28,arg)
   elif arg == "[D29]" and cam_name != d29:
      new_name(d29,arg)
   elif arg == "[D30]" and cam_name != d30:
      new_name(d30,arg)
   elif arg == "[D31]" and cam_name != d31:
      new_name(d31,arg)
   elif arg == "[D32]" and cam_name != d32:
      new_name(d32,arg)

def new_name(d_number,arg):
   time.sleep(timeout)
   wait_for_element_load(camera_input,driver22)
   driver22.find_element(By.XPATH,camera_input).click()
   driver22.find_element(By.XPATH,camera_input).clear()
   driver22.find_element(By.XPATH,camera_input).send_keys(d_number)
   driver22.find_element(By.XPATH,save_button).click()
   insert_log(arg,d_number,2,22)
   time.sleep(timeout)

#check table if there's offline
def scan():
   time.sleep(timeout)
   wait_for_element_load(camera_management_element,driver22)
   driver22.find_element(By.XPATH,camera_management_element).click()
   time.sleep(timeout)
   print('scanning22...')
   camera_count = 0
   is_tail = False
   while is_tail is False:
      try:
         #click row
         driver22.find_element(By.XPATH,table_row + str([camera_count+1])).click()
         camera_count = camera_count + 1
         #get name and status of current row
         camera_name = driver22.find_element(By.XPATH,table_row + str([camera_count]) + '/span[3]').text
         camera_ip = driver22.find_element(By.XPATH,table_row + str([camera_count])  + '/span[4]').text
         camera_status = driver22.find_element(By.XPATH,table_row + str([camera_count]) + '/span[8]').text
         #if offline, get ip and reboot
         if not _cam_list.__contains__(camera_ip) and camera_status != 'Online':
            print('rebooting22...',camera_name)
            reboot(camera_ip,camera_name)
      except Exception as e:
         is_tail = True
         print('scan22',e)
   print('standby22...')

def reboot(ip,name):
   status = True
   try:
      chrome_options = Options()
      chrome_options.add_experimental_option("detach", True)
      global driverReboot
      driverReboot = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
      #set position and size
      driverReboot.set_window_size(800, 600)
      # driverReboot.set_window_position(x, y)
      driverReboot.get('http://'+ip)
      print('logging in ' + ip)
      nvr_username = 'admin'
      nvr_password = 'camng7seas'
      time.sleep(timeout)
      # element_present = EC.presence_of_element_located((By.XPATH, login_button_element))
      # WebDriverWait(driverReboot, timeout).until(element_present)
      wait_for_element_load(login_button_element,driverReboot)
      driverReboot.find_element(By.ID,'username').send_keys(nvr_username)
      driverReboot.find_element(By.ID,'password').send_keys(nvr_password)
      driverReboot.find_element(By.XPATH,login_button_element).click()
      wait_for_element_load(config_element,driverReboot)
      driverReboot.find_element(By.XPATH, config_element).click()
      time.sleep(timeout)
      wait_for_element_load(maintenance,driverReboot)
      driverReboot.find_element(By.XPATH,maintenance).click()
      time.sleep(timeout)
      wait_for_element_load(reboot_button,driverReboot)
      driverReboot.find_element(By.XPATH,reboot_button).click()
      time.sleep(timeout)
      wait_for_element_load(reboot_ok_button,driverReboot)
      driverReboot.find_element(By.XPATH,reboot_ok_button).click()
      time.sleep(30)
   except TimeoutException:
      status = False
   except Exception as e:
      print('reboot',e)
      status = False
   finally:
      driverReboot.quit()
      insert_log(ip,name,status,22)

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

#function to ensure web element loaded
def wait_for_element_load(element, driver):
   element_wait_load = EC.presence_of_element_located((By.XPATH, element))
   WebDriverWait(driver, 10).until(element_wait_load)
   time.sleep(timeout)
      
open_admin_22()