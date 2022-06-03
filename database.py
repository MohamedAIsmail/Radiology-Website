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
  

  mycursor.execute("CREATE TABLE PATIENTS (patientFname VARCHAR(100), patientLname VARCHAR(100), PID int NOT NULL AUTO_INCREMENT, patientpassword VARCHAR(100),age INT DEFAULT NULL, gender VARCHAR(10), mobilephone VARCHAR(12),  Email VARCHAR(30), medicine VARCHAR(3), surgery VARCHAR(3), bloodTransfer VARCHAR(3), virusCorB VARCHAR(3), disease VARCHAR(3) ,PRIMARY KEY(PID))")

  mycursor.execute("CREATE TABLE DOCTORS (doctorFname VARCHAR(100), doctorLname VARCHAR(100), DID VARCHAR(20), PID int, doctorpassword VARCHAR(100), age INT DEFAULT NULL, gender VARCHAR(10), mobilephone VARCHAR(12), salary INT,  Email VARCHAR(30), clinicname VARCHAR(100), PRIMARY KEY(DID), FOREIGN KEY (PID) REFERENCES PATIENTS(PID))")

  mycursor.execute("CREATE TABLE ADMINS (adminFname VARCHAR(100), adminLname VARCHAR(100), AID VARCHAR(20), adminpassword VARCHAR(100), age INT DEFAULT NULL, gender VARCHAR(10), mobilephone VARCHAR(12), salary INT,  Email VARCHAR(30),PRIMARY KEY(AID))")

  mycursor.execute("CREATE TABLE REPORT (DoctorName VARCHAR(200), PatientName VARCHAR(200),PID int, Date DATE NOT NULL, Diagnosis VARCHAR(300), Procedures VARCHAR(300), img VARCHAR(300),FOREIGN KEY (PID) REFERENCES PATIENTS(PID))")

  mycursor.execute("CREATE TABLE COMPLAINTS (Name VARCHAR(200), CONTACTNUMBER VARCHAR(12), EMAIL VARCHAR(200), SUBJECT VARCHAR(100), MESSAGE VARCHAR(300), CNUMBER int NOT NULL AUTO_INCREMENT, PRIMARY KEY(CNUMBER), PID int, FOREIGN KEY (PID) REFERENCES PATIENTS(PID) )")

  mycursor.execute("CREATE TABLE APPOINTMENT (PFname VARCHAR(100), PLname VARCHAR(100), Date VARCHAR(100), Time VARCHAR(100), mobilephone VARCHAR(12), ClinicName VARCHAR(100), Email VARCHAR(30), APPNUMBER int NOT NULL AUTO_INCREMENT,PRIMARY KEY(APPNUMBER), DID VARCHAR(20), PID int, FOREIGN KEY (PID) REFERENCES PATIENTS(PID),FOREIGN KEY (DID) REFERENCES DOCTORS(DID) ) ")

  # mycursor.execute("Show tables;")
 
  # myresult = mycursor.fetchall()
 
  # for x in myresult:
  #     print(x)

  # *********************************** ADD TO DOCTOR *******************************************
  sql="INSERT INTO DOCTORS (doctorFname , doctorLname , DID , doctorpassword ,clinicname ,age , gender , mobilephone , salary ,  Email ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
  value = [
    ('Dina','Salama','D1','1234', 'Dina','21','female','011266672701','99999999','dinakhalid404@gmail.com'),
    ('Fady', 'Nour', 'D2', '1324', 'Fady', '33', 'male', '010555672701', '100000', 'fady20@gmail.com'),

  ]

  mycursor.executemany(sql,value)
  mydb.commit()
  
  # *********************************** ADD TO PATIENT *******************************************

  sql = "INSERT INTO PATIENTS (patientFname , patientLname , PID , patientpassword , age , gender , mobilephone,  Email, medicine, surgery , bloodTransfer , virusCorB , disease ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
  value = [
    ('Ereny', 'Eleya', '1', '9876', '21', 'female', '012888888888', 'ereny2022@gmail.com','NO','YES','NO','C','YES'),
    ('Ahmed', 'Mohammed', '2', '1368', '25', 'male', '012123456789', 'amohammed@gmail.com','YES', 'NO','NO','B','YES'),
    ('Maryam', 'Ahmed', '3', '1111', '30', 'female', '010888834888', 'maro2020@gmail.com','NO','YES','NO','C','YES'),
    ('Nour', 'Emad', '4', '1212', '23', 'female', '011888888222', 'nonoemad@gmail.com','NO','NO','NO','NO','NO'),
  ]

  mycursor.executemany(sql,value)
  mydb.commit()

  # *********************************** ADD TO ADMIN *******************************************
  sql = "INSERT INTO ADMINS (adminFname , adminLname , AID , adminpassword , age , gender , mobilephone , salary ,  Email ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
  value = [
    ('Maha', 'Mohammed', 'A1', '3333', '22', 'female', '012111111111', '5000', 'dmaha@gmail.com'),
    ('Mohamed', 'Gamal', 'A2', '9999', '29', 'male', '010555777777', '7000', 'mgamal@gmail.com'),
  ]

  mycursor.executemany(sql,value)
  mydb.commit()

  sql="INSERT INTO  COMPLAINTS (Name , CONTACTNUMBER , EMAIL , SUBJECT, MESSAGE) VALUES (%s,%s,%s,%s,%s)"
  value = [
    ('Dina','01126672701','dina@gmail.com','تطبيل','اجمد بروجكت دا ولا ايه؟'),


  ]
  mycursor.executemany(sql,value)
  mydb.commit()

  sql = "INSERT INTO  REPORT ('DoctorName', 'PatientName' ,'PID', 'Date', 'Diagnosis', 'Procedures', 'img') VALUES (%s,%s,%s,%s,%s,%s,%s)"
  value = [
    ('Dina Salama', 'Ereny', 1, '2022-06-03', 'Danger!!', 'Increase in cuteness level you HAVE to do something',
     'static/uploads/No17.jpg')
  ]
  mycursor.executemany(sql, value)
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

