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

    mycursor.execute("CREATE TABLE ADMINS (adminFname VARCHAR(100), adminLname VARCHAR(100), AID VARCHAR(20), adminpassword VARCHAR(100), age INT DEFAULT NULL, gender VARCHAR(10), mobilephone VARCHAR(12), Email VARCHAR(30),PRIMARY KEY(AID))")

    mycursor.execute("CREATE TABLE DOCTORS (doctorFname VARCHAR(100), doctorLname VARCHAR(100), DID VARCHAR(20), doctorpassword VARCHAR(100), age INT DEFAULT NULL, gender VARCHAR(10), mobilephone VARCHAR(12), Email VARCHAR(30), clinicname VARCHAR(100), PRIMARY KEY(DID), AID VARCHAR(20), FOREIGN KEY (AID) REFERENCES ADMINS(AID) )")

    mycursor.execute("CREATE TABLE REPORT (RPID int NOT NULL AUTO_INCREMENT, DoctorName VARCHAR(200),DID VARCHAR(20), PatientName VARCHAR(200),PID int, Date DATE NOT NULL, Diagnosis VARCHAR(300), Procedures VARCHAR(300), img VARCHAR(300),FOREIGN KEY (PID) REFERENCES PATIENTS(PID),FOREIGN KEY (DID) REFERENCES DOCTORS(DID),PRIMARY KEY(RPID))")

    mycursor.execute("CREATE TABLE COMPLAINS (CONTACTNUMBER VARCHAR(12), SUBJECT VARCHAR(100), MESSAGE VARCHAR(300), CNUMBER int NOT NULL AUTO_INCREMENT, PRIMARY KEY(CNUMBER), PID int, FOREIGN KEY (PID) REFERENCES PATIENTS(PID) )")

    mycursor.execute("CREATE TABLE UpdateDoctor (Salary VARCHAR(100),  DID VARCHAR(20), FOREIGN KEY (DID) REFERENCES DOCTORS(DID), AID VARCHAR(20), FOREIGN KEY (AID) REFERENCES ADMINS(AID))")

    mycursor.execute("CREATE TABLE APPOINTMENT (PFname VARCHAR(100), PLname VARCHAR(100), Date VARCHAR(100), Time VARCHAR(100), mobilephone VARCHAR(12), ClinicName VARCHAR(100), Email VARCHAR(30), APPNUMBER int NOT NULL AUTO_INCREMENT,PRIMARY KEY(APPNUMBER), DID VARCHAR(20), PID int, FOREIGN KEY (PID) REFERENCES PATIENTS(PID),FOREIGN KEY (DID) REFERENCES DOCTORS(DID) ) ")

    # mycursor.execute("Show tables;")

    # myresult = mycursor.fetchall()

    # for x in myresult:
    #     print(x)


        # *********************************** ADD TO ADMIN *******************************************
    sql = "INSERT INTO ADMINS (adminFname , adminLname , AID , adminpassword , age , gender , mobilephone ,Email) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    value = [
        ('Maha', 'Mohammed', 'A1', '3333', '22', 'female',
         '012111111111', 'dmaha@gmail.com'),
        ('Mohamed', 'Gamal', 'A2', '9999', '29', 'male',
            '010555777777', 'mgamal@gmail.com'),
    ]

    mycursor.executemany(sql, value)
    mydb.commit()

    # *********************************** ADD TO DOCTOR *******************************************
    sql = "INSERT INTO DOCTORS (doctorFname , doctorLname , DID , doctorpassword ,clinicname ,age , gender, mobilephone, Email, AID ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    value = [
        ('Dina', 'Salama', 'D1', '1234', 'X-Ray', '21', 'Female',
         '011266672701', 'dinakhalid404@gmail.com', 'A1'),
        ('Fady', 'Nour', 'D2', '1324', 'CT', '33', 'Male',
            '010555672701', 'fady20@gmail.com', 'A2'),
        ('Mohamed', 'Ismail', 'D10', '9999', 'MRI', '21', 'Male',
            '01142068704', 'mohamedaismail214@gmail.com', 'A2'),
        ('Mo', 'Moustafa', 'D3', '1111', 'UltraSound', '22',
            'Male', '01115674821', 'momoustafa@gmail.com', 'A1'),

    ]

    mycursor.executemany(sql, value)
    mydb.commit()

    # *********************************** ADD TO PATIENT *******************************************

    sql = "INSERT INTO PATIENTS (patientFname , patientLname , PID , patientpassword , age , gender , mobilephone,  Email, medicine, surgery , bloodTransfer , virusCorB , disease ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    value = [
        ('Ereny', 'Eleya', '1', '9876', '21', 'female', '012888888888',
         'ereny2022@gmail.com', 'NO', 'YES', 'NO', 'C', 'YES'),
        ('Ahmed', 'Mohammed', '2', '1368', '25', 'male', '012123456789',
            'amohammed@gmail.com', 'YES', 'NO', 'NO', 'B', 'YES'),
        ('Maryam', 'Ahmed', '3', '1111', '30', 'female', '010888834888',
            'maro2020@gmail.com', 'NO', 'YES', 'NO', 'C', 'YES'),
        ('Nour', 'Emad', '4', '1212', '23', 'female', '011888888222',
            'nonoemad@gmail.com', 'NO', 'NO', 'NO', 'NO', 'NO'),
    ]

    mycursor.executemany(sql, value)
    mydb.commit()


    # *********************************** ADD TO REPORT *******************************************
    sql = "INSERT INTO  REPORT (DoctorName, DID, PatientName, PID, Date, Diagnosis, Procedures, img) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    value = [
        ('Dina Salama', 'D1', 'Ereny', '1', '2022-06-03', 'Danger!!', 'Increase in cuteness level you HAVE to do something',
         '../static/uploads/No17.jpg'),
        ('Fady Nour', 'D2', 'Ereny', '1', '2022-06-04', 'Trivial Report', 'noʎ ǝɹɐ ʍoɥ',
            '../static/uploads/no5.jpg'),
        ('Mo Moustafa', 'D3', 'Ereny', '1', '2022-06-05', 'UltraSound', 'What is the sound of the sea?',
            '../static/uploads/no4.jpg'),
    ]
    mycursor.executemany(sql, value)
    mydb.commit()

    # *********************************** ADD TO APPOINTMENT *******************************************
    sql = "INSERT INTO APPOINTMENT (PFname, PLname, Date, Time, mobilephone, ClinicName, Email, DID, PID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    value = [
        ('Ereny', 'Eleya', '2022-06-12', '12:00',
         '012888888888', 'CT', 'ereny2022@gmail.com', 'D2', '1'),
        ('Ereny', 'Eleya', '2022-06-03', '12:00',
            '012888888888', 'CT', 'ereny2022@gmail.com', 'D2', '1'),
        ('Ahmed', 'Mohammed', '2022-06-11', '12:00',
            '012123456789', 'X-Ray', 'amohammed@gmail.com', 'D1', '2'),
        ('Ereny', 'Eleya', '2022-06-05', '12:00', '012888888888',
            'X-Ray', 'ereny2022@gmail.com', 'D1', '1'),
        ('Ereny', 'Eleya', '2022-06-03', '12:00', '012888888888',
            'MRI', 'ereny2022@gmail.com', 'D10', '1'),
        ('Ahmed', 'Mohammed', '2022-06-11', '01:00',
            '012123456789', 'CT', 'amohammed@gmail.com', 'D2', '2'),
        ('Ereny', 'Eleya', '2022-06-04', '12:00',
            '012888888888', 'CT', 'ereny2022@gmail.com', 'D2', '1'),
        ('Ereny', 'Eleya', '2022-06-03', '12:00', '012888888888',
            'X-Ray', 'ereny2022@gmail.com', 'D1', '1'),
        ('Ahmed', 'Mohammed', '2022-06-11', '12:00',
            '012123456789', 'MRI', 'amohammed@gmail.com', 'D10', '2'),
        ('Ereny', 'Eleya', '2022-06-11', '12:00', '012888888888',
            'X-Ray', 'ereny2022@gmail.com', 'D1', '1'),
        ('Maryam', 'Ahmed', '2022-06-03', '12:00',
            '010888834888', 'CT', 'maro2020@gmail.com', 'D2', '3'),
        ('Maryam', 'Ahmed', '2022-06-05', '12:00', '010888834888',
            'X-Ray', 'maro2020@gmail.com', 'D1', '3'),
        ('Maryam', 'Ahmed', '2022-06-12', '12:00',
            '010888834888', 'MRI', 'maro2020@gmail.com', 'D10', '3'),
        ('Ereny', 'Eleya', '2022-06-03', '12:00', '012888888888', 'CT', 'ereny2022@gmail.com', 'D2', '1'),
        ('Ereny', 'Eleya', '2022-06-04', '12:00', '012888888888', 'CT', 'ereny2022@gmail.com', 'D2', '1'),
        ('Ahmed', 'Mohammed', '2022-06-05', '12:00', '012123456789', 'X-Ray', 'amohammed@gmail.com', 'D1', '2'),
        ('Ereny', 'Eleya', '2022-06-06', '12:00', '012888888888', 'X-Ray', 'ereny2022@gmail.com', 'D1', '1'),
        ('Ereny', 'Eleya', '2022-06-07', '12:00', '012888888888', 'MRI', 'ereny2022@gmail.com', 'D10', '1'),
        ('Ahmed', 'Mohammed', '2022-06-08', '01:00', '012123456789', 'CT', 'amohammed@gmail.com', 'D2', '2'),
        ('Nour', 'Emad', '2022-06-09', '12:00', '011888888222', 'CT', 'nonoemad@gmail.com', 'D2', '4'),
        ('Nour', 'Emad', '2022-06-10', '12:00', '011888888222', 'X-Ray', 'nonoemad@gmail.com', 'D1', '4'),
        ('Nour', 'Emad', '2022-06-06', '12:30', '011888888222', 'MRI', 'nonoemad@gmail.com', 'D10', '4'),
        ('Nour', 'Emad', '2022-06-11', '1:30', '011888888222', 'X-Ray', 'nonoemad@gmail.com', 'D1', '4'),
        ('Nour', 'Emad', '2022-06-03', '1:00', '011888888222', 'CT', 'nonoemad@gmail.com', 'D2', '4'),
        ('Nour', 'Emad', '2022-06-05', '5:00', '011888888222', 'X-Ray', 'nonoemad@gmail.com', 'D1', '4'),
        ('Nour', 'Emad', '2022-06-12', '4:00', '011888888222', 'MRI', 'nonoemad@gmail.com', 'D10', '4'),
        ('Ahmed', 'Mohammed', '2022-06-07', '3:00', '012123456789', 'X-Ray', 'amohammed@gmail.com', 'D1', '2'),
        ('Ahmed', 'Mohammed', '2022-06-08', '2:00', '012123456789', 'X-Ray', 'amohammed@gmail.com', 'D1', '2'),
        ('Ahmed', 'Mohammed', '2022-06-10', '1:00', '012123456789', 'X-Ray', 'amohammed@gmail.com', 'D1', '2'),

    ]
    mycursor.executemany(sql, value)
    mydb.commit()

    # *********************************** ADD TO UPDATE *******************************************
    sql = "INSERT INTO UPDATEDOCTOR (Salary, AID, DID) VALUES (%s, %s, %s)"
    value = [
        ('10000', 'A1', 'D1'),
        ('10000', 'A1', 'D3'),
        ('10000', 'A2', 'D2'),
        ('10000', 'A2', 'D10'),
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



def isEmail(email,cursor,isDoc=0):
    # for no duplicate emails
    if isDoc:
        cursor.execute("SELECT Email FROM DOCTORS")
    else:
        cursor.execute("SELECT Email FROM patients")
    allemails = cursor.fetchall()
    for x in range(0, len(allemails)):
        em = allemails[x]
        if em[0] == email:
            flag = False  # -- Email already exists we shall display a message for that
            break
        else:
            flag = True
    return flag


def isID(id,cursor):
    # for no duplicate emails
    cursor.execute("SELECT DID FROM DOCTORS")

    allIDs = cursor.fetchall()
    for x in range(0, len(allIDs)):
        em = allIDs[x]
        if em[0] == id:
            flag = False  # -- Email already exists we shall display a message for that
            break
        else:
            flag = True
    return flag

recreatedb(1)