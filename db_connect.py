import mysql.connector
#from mysql.connector import errorcode

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