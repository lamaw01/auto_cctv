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

cam_names = ['KIDDIE POOL/TENT ENTRANCE','KIDDIE POOL (LOCKER 2) ','COMMISARRY KITCHEN','OLIVER OUTSIDE','PIRACHUTE LANDING','LOCKER 1 OUTSIDE','LOCKER 1','BRIDGE 1',"Employees' Locker Room",'Cyclone Hallway','TREASURE ISLAND','Pirates Den Area','CYCLONE GATE','POWERHOUSE CONTROL ROOM','POWER HOUSE 2','POWER HOUSE 1','CYCLONE LANDING','Spyglass Counter','Olivers Cafe','ROUNDABOUT 2','ROUNDABOUT 3','LAZY RIVER HALLWAY','BUCCANNER LW']
d1 = 'KIDDIE POOL/TENT ENTRANCE'
d2 = 'KIDDIE POOL (LOCKER 2) '
d3 = 'COMMISARRY KITCHEN'
d4 = 'OLIVER OUTSIDE'
d5 = 'PIRACHUTE LANDING'
d6 = 'LOCKER 1 OUTSIDE'
d7 = 'LOCKER 1'
d8 = 'BRIDGE 1'
d9 = "Employees' Locker Room"
d10 = 'Cyclone Hallway'
d11 = 'TREASURE ISLAND'
d12 = 'Pirates Den Area'
d13 = 'CYCLONE GATE'
d14 = 'POWERHOUSE CONTROL ROOM'
d15 = 'POWER HOUSE 2'
d16 = 'POWER HOUSE 1'
d17 = 'CYCLONE LANDING'
d18 = 'Spyglass Counter'
d19 = "ROUNDABOUT 1"
d20 = 'ROUNDABOUT 2'
d21 = 'ROUNDABOUT 3'
d22 = 'LAZY RIVER HALLWAY'
d23 = 'BUCCANNER LW'

timeout = 5
# x = 770
# y = 390
x = 0
y = 350

def assign_excel_data():
    try:
        excel_data = pd.read_excel('cctv_data.xlsx', sheet_name='19',usecols="A")
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
    except Exception as e:
        print('assign_excel_data',e)

#open nvr 19
def open_admin_19():
    nvr_ip = 'http://192.168.220.19'
    try:
        chrome_options = Options()
        #chrome_options.add_argument("--incognito")
        chrome_options.add_experimental_option("detach", True)
        global driver19
        # driver19 = webdriver.Chrome(options=chrome_options)
        driver19 = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
        #set position and size
        driver19.set_window_size(800, 600)
        driver19.set_window_position(x, y)
        driver19.get(nvr_ip)
        login_19()
        # open_image()
        time.sleep(timeout)
        assign_excel_data()
        #run 24/7
        while True:
            open_image()
            time.sleep(30)
            scan()
            #check if viewer got logged out
            if driver19.current_url != 'http://192.168.220.19/doc/page/config.asp':
                print('logged out...', True)
                login_19()
            #wait 5:00 sesc before refresh page
            time.sleep(1800)
            #refresh page
            driver19.refresh()
            time.sleep(30)
    except Exception as e:
        print('admin 19',e)
        #driver19.close()
        driver19.quit()
        open_admin_19()

def login_19():
    print('logging in 19...')
    nvr_username = 'autocctv'
    nvr_password = '4zmSPrg@'
    time.sleep(timeout)
    wait_for_element_load(login_button_element,driver19)
    driver19.find_element(By.ID,'username').send_keys(nvr_username)
    driver19.find_element(By.ID,'password').send_keys(nvr_password)
    driver19.find_element(By.XPATH,login_button_element).click()
    wait_for_element_load(config_element,driver19)
    driver19.find_element(By.XPATH, config_element).click()
    time.sleep(timeout)

def open_image():
    time.sleep(timeout)
    wait_for_element_load(image_element,driver19)
    driver19.find_element(By.XPATH,image_element).click()
    time.sleep(timeout)
    wait_for_element_load(osd,driver19)
    driver19.find_element(By.XPATH,osd).click()
    time.sleep(timeout)
    loop_cams_rename()
    time.sleep(timeout)
    wait_for_element_load(system_element,driver19)
    driver19.find_element(By.XPATH,system_element).click()
    time.sleep(timeout)

def loop_cams_rename():
    select = Select(driver19.find_element(By.XPATH,osd_dropdown))
    time.sleep(timeout)
    print(len(select.options))
    for i in range(len(select.options)):
        select.select_by_index(i)
        name = driver19.find_element(By.XPATH,dropdown + str([i+1])).text
        print(name)
        switch(name)

def switch(arg):
    if arg == "IP Camera1":
        new_name(d1,arg)
    elif arg == "IP Camera2":
        new_name(d2,arg)
    elif arg == "IP Camera3":
        new_name(d3,arg)
    elif arg == "IP Camera4":
        new_name(d4,arg)
    elif arg == "IP Camera5":
        new_name(d5,arg)
    elif arg == "IP Camera6":
        new_name(d6,arg)
    elif arg == "IP Camera7":
        new_name(d7,arg)
    elif arg == "IP Camera8":
        new_name(d8,arg)
    elif arg == "IP Camera9":
        new_name(d9,arg)
    elif arg == "IP Camera10":
        new_name(d1,arg)
    elif arg == "IP Camera11":
        new_name(d11,arg)
    elif arg == "IP Camera12":
        new_name(d12,arg)
    elif arg == "IP Camera13":
        new_name(d13,arg)
    elif arg == "IP Camera14":
        new_name(d14,arg)
    elif arg == "IP Camera15":
        new_name(d15,arg)
    elif arg == "IP Camera16":
        new_name(d16,arg)
    elif arg == "IP Camera17":
        new_name(d17,arg)
    elif arg == "IP Camera18":
        new_name(d18,arg)
    elif arg == "IP Camera19":
        new_name(d19,arg)
    elif arg == "IP Camera20":
        new_name(d20,arg)
    elif arg == "IP Camera21":
        new_name(d21,arg)
    elif arg == "IP Camera19":
        new_name(d22,arg)
    elif arg == "IP Camera23":
        new_name(d23,arg)

def new_name(d_number,arg):
    time.sleep(timeout)
    wait_for_element_load(camera_input,driver19)
    camera_name = driver19.find_element(By.XPATH,camera_input).get_attribute('value')
    print(camera_name + ' | ' + d_number)
    if(camera_name != d_number):
        # print('rename')
        driver19.find_element(By.XPATH,camera_input).click()
        driver19.find_element(By.XPATH,camera_input).clear()
        driver19.find_element(By.XPATH,camera_input).send_keys(d_number)
        driver19.find_element(By.XPATH,save_button).click()
        insert_log(arg,d_number,2,19)
        time.sleep(timeout)

#check table if there's offline
def scan():
    time.sleep(timeout)
    wait_for_element_load(camera_management_element,driver19)
    driver19.find_element(By.XPATH,camera_management_element).click()
    time.sleep(timeout)
    print('scanning19...')
    camera_count = 0
    is_tail = False
    while is_tail is False:
        try:
            #click row
            driver19.find_element(By.XPATH,table_row + str([camera_count+1])).click()
            camera_count = camera_count + 1
            #get name and status of current row
            camera_name = driver19.find_element(By.XPATH,table_row + str([camera_count]) + '/span[3]').text
            camera_ip = driver19.find_element(By.XPATH,table_row + str([camera_count])  + '/span[3]').text
            camera_status = driver19.find_element(By.XPATH,table_row + str([camera_count]) + '/span[8]').text
            #if offline, get ip and reboot
            if not _cam_list.__contains__(camera_ip) and camera_status != 'Online':
                print('rebooting19...',camera_name)
                reboot(camera_ip,camera_name)
        except Exception as e:
            is_tail = True
            print('scan19',e)
    print('standby19...')

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
        insert_log(ip,name,status,19)

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
      
open_admin_19()