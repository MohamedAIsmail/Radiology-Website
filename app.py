from flask import Flask, redirect, url_for, request, render_template, session, flash, jsonify
import sys
import database
from werkzeug.utils import secure_filename
import mysql.connector  

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123456",
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
            adminpassword = request.form['Pass']
            mycursor = mydb.cursor (buffered=True)
            mycursor.execute('SELECT * FROM ADMINS WHERE AID=%s AND adminpassword=%s', (AID, adminpassword,))
            account = mycursor.fetchone()
            mydb.commit()
            print(account)

            
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
                session['DID'] = account[2]
                session['doctorpassword'] = account[3]
                return redirect(url_for('doctorProfile'))
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
                    session['PID'] = account[2]
                    session['patientpassword'] = account[3]
                    return render_template("Patient_profile.html")
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

        # Get the highest doctor's salary
        
     mycursor.execute("SELECT DID, doctorFname, salary FROM doctors ORDER BY salary DESC")
     docdata=mycursor.fetchmany(size=3)
     return render_template('Analysis.html', adminNum=adminNumbers, doctorNum=doctorNumbers, patientNum = patientNumbers, docdatas=docdata)

@app.route("/Add-complaints", methods =['POST', 'GET'])
def Addcomplaints():
    if request.method == 'POST':
        name = request.form['Name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        contactNum = request.form['ContactNumber']
        sql = "INSERT INTO complaints (Name , EMAIL , SUBJECT , MESSAGE, CONTACTNUMBER) VALUES (%s, %s, %s, %s, %s)"
        val = (name, email, subject, message, contactNum)
        mycursor.execute(sql, val)
        mydb.commit()
        print(val)

    return render_template('Add-complaints.html')


if __name__ == '__main__':
    app.run(debug=True)