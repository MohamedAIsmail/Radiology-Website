import mysql.connector

def recreatedb(bool):
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123456"
  )

  mycursor = mydb.cursor()
  if bool:
    mycursor.execute("DROP DATABASE Raddb")
  mycursor.execute("CREATE DATABASE Raddb")

  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123456",
    database="Raddb"
  )

  mycursor = mydb.cursor()
  

  mycursor.execute("CREATE TABLE DOCTORS (doctorFname VARCHAR(100), doctorLname VARCHAR(100), DID VARCHAR(20), doctorpassword VARCHAR(100),clinicname VARCHAR(100),age INT DEFAULT NULL, gender VARCHAR(10), mobilephone VARCHAR(12), salary INT,  Email VARCHAR(30),PRIMARY KEY(DID))")

  mycursor.execute("CREATE TABLE PATIENTS (patientFname VARCHAR(100), patientLname VARCHAR(100), PID int NOT NULL AUTO_INCREMENT, patientpassword VARCHAR(100),age INT DEFAULT NULL, gender VARCHAR(10), mobilephone VARCHAR(12),  Email VARCHAR(30),PRIMARY KEY(PID))")

  mycursor.execute("CREATE TABLE ADMINS (adminFname VARCHAR(100), adminLname VARCHAR(100), AID VARCHAR(20), adminpassword VARCHAR(100), age INT DEFAULT NULL, gender VARCHAR(10), mobilephone VARCHAR(12), salary INT,  Email VARCHAR(30),PRIMARY KEY(AID))")

  mycursor.execute("CREATE TABLE REPORT (DoctorName VARCHAR(200), PatientName VARCHAR(200), Date DATE NOT NULL, Diagnosis VARCHAR(300), Procedures VARCHAR(300), img VARCHAR(300), mimetype VARCHAR(300))")

  #mycursor.execute("CREATE TABLE APPOINTMENT (PFname VARCHAR(100), PLname VARCHAR(100), Date&Time DATETIME NOT NULL, mobilephone VARCHAR(12), Department VARCHAR(100))")


  # *********************************** ADD TO DOCTOR *******************************************
  sql="INSERT INTO DOCTORS (doctorFname , doctorLname , DID , doctorpassword ,clinicname ,age , gender , mobilephone , salary ,  Email ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
  value = [
    ('Dina','Salama','D1','1234', 'Dina','21','female','011266672701','99999999','dinakhalid404@gmail.com'),
    ('Fady', 'Nour', 'D6', '1324', 'Fady', '33', 'male', '010555672701', '100000', 'fady20@gmail.com'),

  ]
  mycursor.executemany(sql,value)
  mydb.commit()
  
  # *********************************** ADD TO PATIENT *******************************************

  sql = "INSERT INTO PATIENTS (patientFname , patientLname , PID , patientpassword , age , gender , mobilephone,  Email ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
  value = [
    ('Ereny', 'Eleya', '2', '9876', '21', 'female', '012888888888', 'ereny2022@gmail.com'),
    ('Ahmed', 'Mohammed', '3', '1368', '25', 'male', '012123456789', 'amohammed@gmail.com'),
    ('Maryam', 'Ahmed', '4', '1111', '30', 'female', '010888834888', 'maro2020@gmail.com'),
    ('Nour', 'Emad', '5', '1212', '23', 'female', '011888888222', 'nonoemad@gmail.com'),
  ]
  mycursor.executemany(sql,value)
  mydb.commit()

  # *********************************** ADD TO ADMIN *******************************************
  sql = "INSERT INTO ADMINS (adminFname , adminLname , AID , adminpassword , age , gender , mobilephone , salary ,  Email ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
  value = [
    ('Maha', 'Mohammed', '7', '3333', '22', 'female', '012111111111', '5000', 'dmaha@gmail.com'),
    ('Mohamed', 'Gamal', '8', '9999', '29', 'male', '010555777777', '7000', 'mgamal@gmail.com'),

  ]

  mycursor.executemany(sql,value)
  mydb.commit()

def connect():
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123456",
    database="Raddb"
  )

  mycursor = mydb.cursor()
  return mycursor, mydb

