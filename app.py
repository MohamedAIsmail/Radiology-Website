from pydoc import doc
from flask import Flask, redirect, url_for, request, render_template, session, flash, jsonify
import sys
from pyrsistent import m
from werkzeug.utils import secure_filename
import mysql.connector  

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="3669",
    database="Raddb"
  )

mycursor = mydb.cursor(buffered=True)

app = Flask(__name__)
app.secret_key = "super secret key"



@app.route('/')
def Home():
    return render_template('Home.html')

# ---- Registering ----

@app.route('/Login', methods=['POST', 'GET'])

# -------------------------------- LOGIN -----------------------------------

def login():
    msg = ''
    
# ----- ADMIN LOGIN -----

    if request.method == 'POST':
        ID = request.form['RID']
        if ID[0]=='A':
            AID = ID
            print(AID[0])
            adminpassword = request.form['Pass']
            mycursor = mydb.cursor (buffered=True)
            mycursor.execute('SELECT * FROM ADMINS WHERE AID=%s AND adminpassword=%s', (AID, adminpassword,))
            account = mycursor.fetchone()
            mydb.commit()
            
            if account:
                print(account)
                session['loggedin'] = True
                session['RID'] = account[2]
                session['Pass'] = account[3]
                return redirect(url_for('Admin_profile'))
            else:
                msg = 'Incorrect username/password!'



# ----- DOCTOR LOGIN -----

        elif ID[0]=='D':

            DID = ID
            doctorpassword = request.form['Pass']
            mycursor = mydb.cursor(buffered=True)
            mycursor.execute(
                'SELECT * FROM DOCTORS WHERE DID=%s AND doctorpassword=%s', (DID, doctorpassword))
            account = mycursor.fetchone()
            mydb.commit()

            if account:
                print(account)
                session['loggedin'] = True
                session['RID'] = account[2]
                session['doctorpassword'] = account[3]
                return redirect(url_for('doctor_profile'))
            else:
                msg = 'Incorrect username/password!'
                # ---- PATIENT LOGIN ----

        else:

                PID = ID
                patientpassword = request.form['Pass']
                mycursor = mydb.cursor(buffered=True)
                mycursor.execute(
                    'SELECT * FROM PATIENTS WHERE PID = %s AND patientpassword = %s', (PID, patientpassword))
                account = mycursor.fetchone()
                mydb.commit()
                print(PID, patientpassword)
                print(account)
                if account:
                    session['loggedin'] = True
                    session['RID'] = account[2]
                    session['patientpassword'] = account[3]
                    return redirect(url_for('Patient_profile'))
                else:
                    msg = 'Incorrect username/password!'

    return render_template('Login.html')

# ---------------------- REGISTERING ----------------------

@app.route('/Register', methods=['POST', 'GET'])

def Register():
    if request.method == 'POST':  ##check if there is post data
        if request.form.get('action') == 'Reg': 
            patientFname = request.form['patientFname']
            patientLname = request.form['patientLname']
            Email = request.form['patientEmail']
            patientpassword = request.form['patientpassword']


            #for no duplicate emails
            mycursor.execute("SELECT Email FROM patients")
            allemails = mycursor.fetchall()
            for x in range(0,len(allemails)):
                em=allemails[x]
                if em[0]==Email:
                    flag=False        # -- Email already exists we shall display a message for that
                    break
                else:
                    flag=True
            if(flag):     
                sql = "INSERT INTO patients (patientFname, patientLname, Email, patientpassword) VALUES(%s,%s,%s,%s)"
                val = (patientFname, patientLname, Email, patientpassword)
                mycursor.execute(sql, val)
                mydb.commit()

        # -- This part contains an error which we will solve later but it works fine!

                mycursor.execute("SELECT PID FROM patients ORDER BY PID DESC")
                record = mycursor.fetchone()
                id=record[0]
                message = "You have successfully registered ! \n" + "Your ID is: " + str(id)
                flash(message)
            
   
    return render_template('Login.html')    



# ---- ADMIN PROFILE ----

@app.route("/Admin_profile", methods =['GET', 'POST']) 
def Admin_profile(): 
    if 'loggedin' in session:  
        AID = session['RID']
        sql ="SELECT * FROM admins WHERE AID = %s"
        val= (AID,)
        mycursor.execute(sql, val)
        account = mycursor.fetchone() 
        return render_template("Admin_profile.html", data=account) 

    return redirect(url_for('login')) 

#----------------EDIT ADMIN PROFILE--------------------------------------------------
@app.route("/edit-admin-profile", methods =['GET', 'POST']) 
def edit_admin_profile(): 
    if request.method == 'POST':  ##check if there is post data
        if request.form.get('action') == 'update': #All info must be filled!!!
            AdminFname = request.form['fname']
            AdminLname = request.form['lname']
            Age = request.form['age']
            gender = request.form['gen']
            Email = request.form['email']
            mobile= request.form['mobile']
            
            
        if 'loggedin' in session:  
            AID = session['RID'] 
            sql = "UPDATE admins SET adminFname = %s, adminLname=%s, age=%s, gender=%s, Email=%s, mobilephone=%s WHERE AID = %s"
            val = (AdminFname, AdminLname, Age, gender,Email, mobile,AID)
            mycursor.execute(sql, val)
            mydb.commit()

            print(mycursor.rowcount, "record(s) affected")   

    return render_template('edit-admin-profile.html')    


# ---- DOCTOR PROFILE ----

@app.route("/doctor_profile", methods =['GET', 'POST']) 
def doctor_profile(): 
    if 'loggedin' in session:
         
        DID = session['RID']
        sql ="SELECT * FROM DOCTORS WHERE DID=%s"
        val= (DID,)
        mycursor.execute(sql, val)
        account = mycursor.fetchone() 
        return render_template("doctor_profile.html", data=account) 

    return redirect(url_for('login')) 

#----------------EDIT DOCTOR PROFILE--------------------------------------------------
@app.route("/edit-doctor-profile", methods =['GET', 'POST']) 
def edit_doctor_profile(): 
    if request.method == 'POST':  ##check if there is post data
        if request.form.get('action') == 'update': #All info must be filled!!!
            doctorFname = request.form['fname']
            doctorLname = request.form['lname']
            Age = request.form['age']
            gender = request.form['gen']
            Email = request.form['email']
            mobile= request.form['mobile']
            
            
        if 'loggedin' in session:  
            DID = session['RID'] 
            sql = "UPDATE doctors SET doctorFname = %s, doctorLname=%s, age=%s, gender=%s, Email=%s, mobilephone=%s WHERE DID = %s"
            val = (doctorFname, doctorLname, Age, gender,Email, mobile,DID)
            mycursor.execute(sql, val)
            mydb.commit()

            print(mycursor.rowcount, "record(s) affected")   

    return render_template('edit-doctor-profile.html') 


# ---- PATIENT PROFILE ----

@app.route("/Patient_profile", methods =['GET', 'POST']) 
def Patient_profile(): 
    if 'loggedin' in session:  
        PID = session['RID']
        sql ="SELECT * FROM patients WHERE PID = %s"
        val= (PID,)
        mycursor.execute(sql, val)
        account = mycursor.fetchone() 
        return render_template("Patient_profile.html", data=account) 

    return redirect(url_for('login')) 

#----------------EDIT PATIENT PROFILE--------------------------------------------------

#EDIT PERSONAL INFO
@app.route("/edit_patient_profile", methods =['GET', 'POST']) 
def edit_personal_pinfo(): 
    if request.method == 'POST':  ##check if there is post data
        if request.form.get('action') == 'update': #All info must be filled!!!
            patientFname = request.form['fname']
            patientLname = request.form['lname']
            Age = request.form['age']
            gender = request.form['gen']
            Email = request.form['email']
            mobile= request.form['mobile']
            
            
        if 'loggedin' in session:  
            PID = session['RID'] 
            sql = "UPDATE patients SET patientFname = %s, patientLname=%s, age=%s, gender=%s, Email=%s, mobilephone=%s WHERE PID = %s"
            val = (patientFname, patientLname, Age, gender,Email, mobile,PID)
            mycursor.execute(sql, val)
            mydb.commit()

            print(mycursor.rowcount, "record(s) affected")   

    return render_template('edit_patient_profile.html') 

#EDIT MEDICAL INFO
@app.route("/edit-medical-info", methods =['GET', 'POST']) 
def edit_medical_pinfo(): 
    if request.method == 'POST':  ##check if there is post data
        if request.form.get('action') == 'update': #All info must be filled!!!
            med = request.form['med']
            sur = request.form['sur']
            bt = request.form['bt']
            v = request.form['v']
            ds = request.form['ds']
                   
        if 'loggedin' in session:  
            PID = session['RID'] 
            sql = "UPDATE patients SET medicine = %s, surgery=%s, bloodTransfer=%s, virusCorB=%s, disease=%s WHERE PID = %s"
            val = ( med, sur, bt, v, ds, PID)
            mycursor.execute(sql, val)
            mydb.commit()

            print(mycursor.rowcount, "record(s) affected")   

    return render_template('edit-medical-info.html')     

    




# ---- Logout ----

# @app.route('/logout')
# def logout():
#     session.pop('loggedin', None)
#     session.pop('PID', None)
#     session.pop('patientpassword', None)
#     return redirect(url_for('Home'))







#------- VIEW DOCTORS ---------

@app.route('/View-doctor', methods = ['POST', 'GET'])
def viewdoctor():

   if request.method == 'POST':
      return render_template('Admin_profile.html')
   else:
      mycursor.execute("SELECT DID, doctorFname, clinicname,mobilephone,Email,salary FROM doctors")
      row_headers=[x[0] for x in mycursor.description] 
      myresult = mycursor.fetchall()
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
            }
      return render_template('View-doctor.html',data=myresult)


@app.route('/Analysis', methods = ['POST', 'GET'])
def analysis():
    if request.method == 'POST':
     return render_template('Admin_profile.html')

    else:

        # Get the number of doctors, patients in the hospital

     mycursor.execute("SELECT COUNT(*) FROM admins")
     adminNumbers = mycursor.fetchone()
     mycursor.execute("SELECT COUNT(*) FROM doctors")
     doctorNumbers = mycursor.fetchone()
     mycursor.execute("SELECT COUNT(*) FROM patients")
     patientNumbers = mycursor.fetchone()
     mycursor.execute("SELECT COUNT(*) FROM COMPLAINTS")
     feedbackNumbers= mycursor.fetchone()

        # Get the highest doctor's salary
        
     mycursor.execute("SELECT DID, doctorFname, salary FROM doctors ORDER BY salary DESC")
     docdata=mycursor.fetchmany(size=3)
     return render_template('Analysis.html', adminNum=adminNumbers, doctorNum=doctorNumbers, patientNum = patientNumbers, docdatas=docdata, feedbackdata=feedbackNumbers)



# ------------------- ADD COMPLAINT -------------------

@app.route("/Add-complaints", methods =['POST', 'GET'])
def Addcomplaints():
    if 'loggedin' in session:  
        PID = session['RID']
        if request.method == 'POST':
            sql = "SELECT patientFname, Email, mobilephone FROM PATIENTS WHERE PID=%s"
            val=(PID,)
            mycursor.execute(sql,val)
            patients=mycursor.fetchall()

            subject = request.form['subject']
            message = request.form['message']

            print(patients[0])

            sql = "INSERT INTO complaints (Name , EMAIL , SUBJECT , MESSAGE, CONTACTNUMBER) VALUES (%s, %s, %s, %s, %s)"
            for x in patients:
                val = (x[0], x[1], subject, message, x[2])
            mycursor.execute(sql, val)
            mydb.commit()
            print(val)

    return render_template('Add-complaints.html')



#---------------------- VIEW COMPLAINTS -----------------------

@app.route('/View-complaints.html', methods = ['POST', 'GET'])
def Viewcomplaints():

   if request.method == 'POST':
      return render_template('Admin_profile.html')
   else:
      mycursor.execute("SELECT Name, EMAIL, CONTACTNUMBER,SUBJECT,MESSAGE FROM COMPLAINTS")
      row_headers=[x[0] for x in mycursor.description]
      myresult = mycursor.fetchall()
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
            }
      return render_template('View-complaints.html',data=myresult)

# -------------- RESERVE APPOINTMENTS -------------

@app.route("/Patient-reserve.html", methods =['GET', 'POST']) 

def ReserveAppointment():
    if 'loggedin' in session:  
        PID = session['RID']

        if request.method == 'POST':
            doctorChosen = request.form.get('doctorChosen')
            
            DATE = request.form['date']
            TIME = request.form['time']
            print(doctorChosen)
            
            sql= "SELECT DID FROM Doctors where doctorFname = %s"
            val= (doctorChosen,)
            mycursor.execute(sql,val)
            docID = mycursor.fetchone()
            doctorID= docID[0]


            sql ="SELECT patientFname,patientLname,mobilephone FROM patients WHERE PID = %s"
            val= (PID,)
            mycursor.execute(sql,val)
            patientInfo=mycursor.fetchall()

            for x in patientInfo:
                Pfname = x[0]
                Plname = x[1]
                mobilephone= x[2]

            sql ="INSERT INTO APPOINTMENT (PFname, PLname, Date, Time, mobilephone, DID, PID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (Pfname, Plname , DATE, TIME, mobilephone, doctorID , PID)
            mycursor.execute(sql, val)
            mydb.commit()

    return redirect(url_for('Returningdoc'))

@app.route("/Returningdoc", methods =['GET', 'POST'])

def Returningdoc():
     mycursor.execute("SELECT doctorFname FROM doctors")
     myresult = mycursor.fetchall()

     return render_template('Patient-reserve.html', data=myresult)


# -------------------------------- VIEW APPOINTMENT PATIENT -------------------------------------------

@app.route("/ViewAppointment-Patient", methods =['GET', 'POST'])
def viewAppointment():
    if 'loggedin' in session:  
        PID = session['RID']

        # Exception handeling in case there are no appointments must be done!!!!

        sql="SELECT DID FROM Appointment WHERE PID = %s"
        val =(PID,)
        mycursor.execute(sql,val)
        docID=mycursor.fetchone()
        print(docID)

        sql = "SELECT doctorFname FROM DOCTORS WHERE DID = %s"
        val =(docID,)
        mycursor.executemany(sql,val)
        result=mycursor.fetchall()

        for x in result:
            print(x)

        sql = "SELECT APPNUMBER, PFname, Date, Time FROM Appointment WHERE PID = %s"
        val =(PID,)
        mycursor.execute(sql,val)
        myresult=mycursor.fetchall()
        

    return render_template('view-appointment -patient.html', data=myresult, docname=result) 

# -------------------------------- VIEW APPOINTMENT DOCTOR -------------------------------------------

@app.route("/ViewAppointment-Doctor", methods =['GET', 'POST'])
def viewDocAppointment():

    if 'loggedin' in session:  
        DID = session['RID']

        # Exception handeling in case there are no appointments must be done!!!!

        sql="SELECT PID FROM Appointment WHERE DID = %s"
        val =(DID,)
        mycursor.execute(sql,val)
        patientID=mycursor.fetchone()
        print(patientID)

        sql = "SELECT APPNUMBER, PFname, Date, Time FROM Appointment WHERE DID = %s"
        val =(DID,)
        mycursor.execute(sql,val)
        myresult=mycursor.fetchall()
        

    return render_template('view-appointment-doctor.html', data=myresult) 

 # ------------------- VIEW PATIENT --------------------
@app.route("/ViewPatient", methods =['GET', 'POST'])
def viewPatient():

    if 'loggedin' in session:  
        DID = session['RID']

        # Exception handeling in case there are no appointments must be done!!!!

        sql="SELECT PID FROM Appointment WHERE DID = %s"
        val =(DID,)
        mycursor.execute(sql,val)
        patientID=mycursor.fetchone()
        print(patientID)

        sql = "SELECT  PID, patientFname, mobilephone, Email FROM PATIENTS WHERE PID = %s"
        val =(patientID,)
        mycursor.executemany(sql,val)
        myresult=mycursor.fetchall()
        

    return render_template('patient-view.html', data=myresult) 

if __name__ == '__main__':
    app.run(debug=True)