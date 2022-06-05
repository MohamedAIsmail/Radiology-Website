import os
from flask import Flask, redirect, url_for, request, render_template, session, flash
from datetime import date
from werkzeug.utils import secure_filename
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="Raddb"
)

mycursor = mydb.cursor(buffered=True)

app = Flask(__name__)
app.secret_key = "super secret key"
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
        if ID[0] == 'A':
            AID = ID
            print(AID[0])
            adminpassword = request.form['Pass']
            mycursor = mydb.cursor(buffered=True)
            mycursor.execute(
                'SELECT * FROM ADMINS WHERE AID=%s AND adminpassword=%s', (AID, adminpassword,))
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

        elif ID[0] == 'D':

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
    mycursor.execute("SELECT PID FROM patients ORDER BY PID DESC")
    record = mycursor.fetchone()
    id = record[0]
    if request.method == 'POST':  # check if there is post data
        if request.form.get('action') == 'Reg':
            patientFname = request.form['patientFname']
            patientLname = request.form['patientLname']
            Email = request.form['patientEmail']
            patientmobPhone = request.form['patientphone']
            patientpassword = request.form['patientpassword']


            # for no duplicate emails
            mycursor.execute("SELECT Email FROM patients")
            allemails = mycursor.fetchall()
            for x in range(0, len(allemails)):
                em = allemails[x]
                if em[0] == Email:
                    flag = False        # -- Email already exists we shall display a message for that
                    break
                else:
                    flag = True


            if(flag):
                sql = "INSERT INTO patients (patientFname, patientLname, mobilephone, Email, patientpassword) VALUES(%s, %s, %s, %s, %s)"
                val = (patientFname, patientLname,patientmobPhone, Email, patientpassword)
                mycursor.execute(sql, val)
                mydb.commit()

    return render_template('Login.html', newID=id)



# ---- ADMIN PROFILE ----

@app.route("/Admin_profile", methods=['GET', 'POST'])
def Admin_profile():
    if 'loggedin' in session:
        AID = session['RID']
        sql = "SELECT * FROM admins WHERE AID = %s"
        val = (AID,)
        mycursor.execute(sql, val)
        account = mycursor.fetchone()
        return render_template("Admin_profile.html", data=account)

    return redirect(url_for('login'))

# ----------------EDIT ADMIN PROFILE--------------------------------------------------


@app.route("/edit-admin-profile", methods=['GET', 'POST'])
def edit_admin_profile():
    if request.method == 'POST':  # check if there is post data
        if request.form.get('action') == 'update':  # All info must be filled!!!
            AdminFname = request.form['fname']
            AdminLname = request.form['lname']
            Age = request.form['age']
            gender = request.form['gen']
            Email = request.form['email']
            mobile = request.form['mobile']

        if 'loggedin' in session:
            AID = session['RID']
            sql = "UPDATE admins SET adminFname = %s, adminLname=%s, age=%s, gender=%s, Email=%s, mobilephone=%s WHERE AID = %s"
            val = (AdminFname, AdminLname, Age, gender, Email, mobile, AID)
            mycursor.execute(sql, val)
            mydb.commit()

            print(mycursor.rowcount, "record(s) affected")

    return render_template('edit-admin-profile.html')


# ---- DOCTOR PROFILE ----

@app.route("/doctor_profile", methods=['GET', 'POST'])
def doctor_profile():
    if 'loggedin' in session:

        DID = session['RID']
        sql = "SELECT doctorFname, doctorLname, doctors.DID, age, gender, Email, mobilephone, updatedoctor.Salary FROM DOCTORS JOIN updatedoctor WHERE doctors.DID=%s AND updatedoctor.DID = %s"
        val = (DID, DID)
        mycursor.execute(sql, val)
        account = mycursor.fetchone()
        return render_template("doctor_profile.html", data=account)

    return redirect(url_for('login'))

# ----------------EDIT DOCTOR PROFILE--------------------------------------------------


@app.route("/edit-doctor-profile", methods=['GET', 'POST'])
def edit_doctor_profile():
    if request.method == 'POST':  # check if there is post data
        if request.form.get('action') == 'update':  # All info must be filled!!!
            doctorFname = request.form['fname']
            doctorLname = request.form['lname']
            Age = request.form['age']
            gender = request.form['gen']
            Email = request.form['email']
            mobile = request.form['mobile']

        if 'loggedin' in session:
            DID = session['RID']
            sql = "UPDATE doctors SET doctorFname = %s, doctorLname=%s, age=%s, gender=%s, Email=%s, mobilephone=%s WHERE DID = %s"
            val = (doctorFname, doctorLname, Age, gender, Email, mobile, DID)
            mycursor.execute(sql, val)
            mydb.commit()

            print(mycursor.rowcount, "record(s) affected")

    return render_template('edit-doctor-profile.html')


# ---- PATIENT PROFILE ----

@app.route("/Patient_profile", methods=['GET', 'POST'])
def Patient_profile():
    if 'loggedin' in session:
        PID = session['RID']
        sql = "SELECT * FROM patients WHERE PID = %s"
        val = (PID,)
        mycursor.execute(sql, val)
        account = mycursor.fetchone()
        return render_template("Patient_profile.html", data=account)

    return redirect(url_for('login'))

# ----------------EDIT PATIENT PROFILE--------------------------------------------------

# EDIT PERSONAL INFO


@app.route("/edit_patient_profile", methods=['GET', 'POST'])
def edit_personal_pinfo():
    if request.method == 'POST':  # check if there is post data
        if request.form.get('action') == 'update':  # All info must be filled!!!
            patientFname = request.form['fname']
            patientLname = request.form['lname']
            Age = request.form['age']
            gender = request.form['gen']
            Email = request.form['email']
            mobile = request.form['mobile']

        if 'loggedin' in session:
            PID = session['RID']
            sql = "UPDATE patients SET patientFname = %s, patientLname=%s, age=%s, gender=%s, Email=%s, mobilephone=%s WHERE PID = %s"
            val = (patientFname, patientLname, Age, gender, Email, mobile, PID)
            mycursor.execute(sql, val)
            mydb.commit()

            print(mycursor.rowcount, "record(s) affected")

    return render_template('edit_patient_profile.html')

# EDIT MEDICAL INFO


@app.route("/edit-medical-info", methods=['GET', 'POST'])
def edit_medical_pinfo():
    if request.method == 'POST':  # check if there is post data
        if request.form.get('action') == 'update':  # All info must be filled!!!
            med = request.form['med']
            sur = request.form['sur']
            bt = request.form['bt']
            v = request.form['v']
            ds = request.form['ds']

        if 'loggedin' in session:
            PID = session['RID']
            sql = "UPDATE patients SET medicine = %s, surgery=%s, bloodTransfer=%s, virusCorB=%s, disease=%s WHERE PID = %s"
            val = (med, sur, bt, v, ds, PID)
            mycursor.execute(sql, val)
            mydb.commit()

            print(mycursor.rowcount, "record(s) affected")

    return render_template('edit-medical-info.html')

# -------------------- ADD DOCTOR -----------------


@app.route('/addDoctor', methods=['GET', 'POST'])
def addDoctor():
    if request.method == 'POST':
        doctorFname = request.form['doctorFname']
        doctorLname = request.form['doctorLname']
        DID = request.form['RID']
        doctorpassword = request.form['docPassword']
        clinicname = request.form['docClinic']
        age = request.form['docAge']
        gender = request.form['Gender']
        mobilephone = request.form['docMob']
        salary = request.form['Salary']
        Email = request.form['docEmail']

        # sql = "INSERT INTO APPOINTMENT (DID) VALUES (%s)"
        # val = (DID)
        # mycursor.execute(sql, val)

        sql = "INSERT INTO DOCTORS (doctorFname , doctorLname , DID , doctorpassword ,clinicname ,age , gender , mobilephone , salary ,  Email ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (doctorFname, doctorLname, DID, doctorpassword,
               clinicname, age, gender, mobilephone, salary, Email)
        mycursor.execute(sql, val)
        mydb.commit()

    return render_template('Admin-AddDoctor.html')


# ---- Logout ----

# @app.route('/logout')
# def logout():
#     session.pop('loggedin', None)
#     session.pop('PID', None)
#     session.pop('patientpassword', None)
#     return redirect(url_for('Home'))


# ----------------- VIEW DOCTORS -----------------

@app.route('/View-doctor', methods=['POST', 'GET'])
def viewdoctor():

    mycursor.execute("SELECT doctors.DID, doctorFname, clinicname, mobilephone, Email, updatedoctor.Salary FROM doctors JOIN updatedoctor WHERE doctors.DID = updatedoctor.DID")
    myresult = mycursor.fetchall()

    return render_template('View-doctor.html', data=myresult)

# ---------------- EDIT DOCTOR INFORMATION ----------------
@app.route("/EditDoctor", methods=['GET', 'POST'])
def editDoctor():
    if request.method == 'POST':
        DIDchosen = request.form['chooseDoctor']
        mycursor.execute("SELECT doctors.DID, doctorFname, clinicname, mobilephone, Email FROM doctors WHERE doctors.DID = %s" , (DIDchosen,))
        myresult = mycursor.fetchall()

    return render_template('Admin-EditDoctor.html', data=myresult)

@app.route("/salaryEdited", methods=['GET', 'POST'])
def editDoctorSalary():
    if 'loggedin' in session:
        AID = session["RID"]
        if request.method == 'POST':
            newSalary = request.form['newSalary']
            DIDchosen = request.form['chooseDoctor']
            mycursor.execute("UPDATE updatedoctor SET Salary = %s WHERE DID = %s AND AID = %s" , (newSalary, DIDchosen, AID))
    
    return redirect(url_for('viewdoctor')) 

# --------------------------- SHOW ANALYSIS PAGE ------------------

@app.route('/Analysis', methods=['POST', 'GET'])
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
        mycursor.execute("SELECT COUNT(*) FROM COMPLAINS")
        feedbackNumbers = mycursor.fetchone()
        mycursor.execute("SELECT COUNT(*) FROM APPOINTMENT")
        appNumbers = mycursor.fetchone()

    # Get the number of appointments each day
    mycursor.execute(
        "SELECT Date, COUNT(Date) FROM APPOINTMENT group by date order by date")
    graph1 = mycursor.fetchall()
    appNum = [x[1] for x in graph1]
    alldays = [int(x[0][-2:]) for x in graph1]
    allmonths = [int(x[0][5:7]) for x in graph1]
    # Get the number of scan types
    mycursor.execute('select ClinicName, count(ClinicName) from appointment group by ClinicName')
    pie = mycursor.fetchall()
    scanName=[x[0] for x in pie]
    scanNum=[x[1] for x in pie]
    print(scanName,scanNum)

    # Get the highest doctor's salary
    #  mycursor.execute("SELECT DID, doctorFname, salary FROM doctors ORDER BY salary DESC")
    #  docdata=mycursor.fetchmany(size=3)
    return render_template('Analysis.html',scanName=scanName,scanNum=scanNum, appNum=appNum, alldays=alldays, allmonths=allmonths, adminNum=adminNumbers, doctorNum=doctorNumbers, patientNum=patientNumbers, feedbackdata=feedbackNumbers, appointmentdata=appNumbers)


# ------------------- ADD COMPLAIN -------------------

@app.route("/Add-complaints", methods=['POST', 'GET'])
def Addcomplaints():
    if 'loggedin' in session:
        PID = session['RID']
        if request.method == 'POST':
            sql = "SELECT mobilephone FROM PATIENTS WHERE PID = %s"
            val = (PID,)
            mycursor.execute(sql, val)
            patients = mycursor.fetchone()
            subject = request.form['subject']
            message = request.form['message']
            

            sql = "INSERT INTO COMPLAINS (PID, SUBJECT , MESSAGE, CONTACTNUMBER) VALUES (%s, %s, %s, %s)"
            val = (PID, subject, message, patients[0])
            mycursor.execute(sql, val)
            mydb.commit()


    return render_template('Add-complaints.html')


# ---------------------- VIEW COMPLAINT -----------------------

@app.route('/View-complaints.html', methods=['POST', 'GET'])
def Viewcomplaints():

    mycursor.execute("SELECT patientFname, patientLname, PATIENTS.Email, CONTACTNUMBER, SUBJECT, MESSAGE FROM COMPLAINS JOIN PATIENTS ON COMPLAINS.PID = Patients.PID")
    myresult = mycursor.fetchall()
    Pfnames = [x[0] for x in myresult]
    Plnames = [x[1] for x in myresult]
    names = [(Pfnames[i] + " " + Plnames[i]) for i in range(len(Pfnames))]
    print(myresult)
    myresult2 = [list(myresult[i]) for i in range(len(myresult))]
    for i in range(len(names)):
        myresult2[i][0] = names[i]

    return render_template('View-complaints.html', data=myresult2)

# -------------- RESERVE APPOINTMENTS -------------


@app.route("/Patient-reserve.html", methods=['GET', 'POST'])
def ReserveAppointment():
    if 'loggedin' in session:
        PID = session['RID']

        if request.method == 'POST':

            ClinicNAME = request.form.get('clinicChosen')
            DATE = request.form['date']
            TIME = request.form['time']

            sql = "SELECT patientFname, patientLname, mobilephone, Email FROM patients WHERE PID = %s"
            val = (PID,)
            mycursor.execute(sql, val)
            patientInfo = mycursor.fetchall()

            for x in patientInfo:
                Pfname = x[0]
                Plname = x[1]
                mobilephone = x[2]
                Pemail = x[3]

            if dateChecker(DATE, TIME, ClinicNAME):

                sql = "INSERT INTO APPOINTMENT (PFname, PLname, Date, Time, mobilephone, ClinicName, Email, DID, PID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (Pfname, Plname, DATE, TIME, mobilephone, ClinicNAME,
                       Pemail, dateChecker(DATE, TIME, ClinicNAME), PID)
                print(val)
                mycursor.execute(sql, val)
                mydb.commit()
                flash('Your appointment is reserved!')

            else:
                flash('Date has been already taken!')

    return redirect(url_for('Returningdoc'))


def dateChecker(date, time, scans):

    scanChosen = scans
    DATE = date
    TIME = time
    breakoutflag = False

    sql = "SELECT DID FROM doctors WHERE clinicname = %s"
    val = (scanChosen,)
    mycursor.execute(sql, val)
    docInfo = mycursor.fetchall()
    print(docInfo)

    for r in docInfo:
        mycursor.execute(
            "SELECT EXISTS(SELECT DID FROM APPOINTMENT WHERE DID = %s)", (r[0],))
        docChecking = mycursor.fetchall()

        for x in docChecking:
            if(x[0] == 1):
                mycursor.execute(
                    "SELECT Date, Time, APPOINTMENT.DID FROM APPOINTMENT JOIN Doctors ON APPOINTMENT.DID = %s AND Doctors.clinicname= %s ", (r[0], scanChosen,))
                dateCheck = mycursor.fetchall()

                print(dateCheck)
                for x in dateCheck:
                    Date = x[0]
                    Time = x[1]
                    DID = x[2]

                    if (Date == DATE) & (Time == TIME):
                        breakoutflag = True
                        break

                if breakoutflag:
                    break

                DocID = DID
                return DocID

            else:
                return r[0]

    return False


@app.route("/Returningdoc", methods=['GET', 'POST'])
def Returningdoc():
    mycursor.execute("SELECT DISTINCT clinicname FROM doctors")
    myresult = mycursor.fetchall()

    return render_template('Patient-reserve.html', data=myresult)


# -------------------------------- VIEW APPOINTMENT PATIENT -------------------------------------------

@app.route("/ViewAppointment-Patient", methods=['GET', 'POST'])
def viewAppointment():
    if 'loggedin' in session:
        PID = session['RID']

        sql = "SELECT APPNUMBER, PFname, Date, Time , doctors.doctorFname FROM Appointment JOIN Doctors ON Appointment.DID = Doctors.DID AND Appointment.PID = %s"
        val = (PID,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()

    return render_template('view-appointment -patient.html', data=myresult)


# -------------------------------- VIEW APPOINTMENT DOCTOR -------------------------------------------
@app.route("/ViewAppointment-Doctor", methods=['GET', 'POST'])
def viewDocAppointment():

    if 'loggedin' in session:
        DID = session['RID']

        sql = "SELECT APPNUMBER, PFname, Date, Time FROM Appointment WHERE DID = %s"
        val = (DID,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()

    return render_template('view-appointment-doctor.html', data=myresult)

 # ------------------- VIEW PATIENT --------------------


@app.route("/ViewPatient", methods=['GET', 'POST'])
def viewPatient():

    if 'loggedin' in session:
        DID = session['RID']

        sql = "SELECT DISTINCT Appointment.PID, PFname, Appointment.mobilephone, Appointment.Email FROM APPOINTMENT JOIN PATIENTS ON APPOINTMENT.PID = PATIENTS.PID AND APPOINTMENT.DID = %s"
        val = (DID,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()

    return render_template('patient-view.html', data=myresult)

# ------- VIEW DOCTORS ---------


@app.route('/viewAllReports', methods=['GET'])
def viewAllReports():
    if 'loggedin' in session:
        PID = session['RID']
        val = (PID,)
        mycursor.execute(
            "SELECT RPID, DoctorName, Diagnosis, img FROM REPORT where PID=%s", val)
        myresult = mycursor.fetchall()

    return render_template('viewAllReports.html', data=myresult)

# -------------------------- VIEW A REPORT ---------------------------


@app.route("/ViewAReport/<int:RPID>", methods=['GET'])
def viewAReport(RPID):
    sql = "SELECT * FROM REPORT WHERE RPID = %s"
    val = (RPID,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    print(myresult)

    return render_template('viewAReport.html', data=myresult[0])


# -------------------------------- WRITE A REPORT DOCTOR -------------------------------------------
allowedExtentions = {'png', 'jpg', 'jpeg'}


def alloweFiles(filename: str):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowedExtentions


@app.route('/write_report', methods=['GET', 'POST'])
def write_report():

    if 'loggedin' in session:
        DID = session['RID']

        if request.method == 'POST':

            # Get doctor name
            sql = "SELECT doctorFname,doctorLname FROM DOCTORS WHERE DID=%s"
            val = (DID,)
            mycursor.execute(sql, val)
            Doctor = mycursor.fetchall()

            # Get the data from post request
            file = request.files['file']
            Diagnosis = request.form['Diagnosis']
            PID = request.form['PatientIDChosen']

            DATE = date.today()
            Procedures = request.form['Procedures']

            # Get all patients IDs
            mycursor.execute(
                "SELECT patientFname FROM patients WHERE PID = %s", (PID,))
            Patientname = mycursor.fetchone()

            # Save the file to ./static/uploads
            if alloweFiles(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
            else:
                flash('Allowed Image types: png, jpg, jpeg')
                return redirect(url_for('ReturningPatient'))

            sql = "INSERT INTO REPORT (DoctorName , PatientName , DID, PID, Date , Diagnosis, Procedures, img) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            for x in Doctor:
                Dfname = x[0]
                Dlname = x[1]
            try:
                Finalpath = "../"+file_path
                val = (
                    Dfname+" "+Dlname, Patientname[0], DID, PID, DATE, Diagnosis, Procedures, Finalpath)
                mycursor.execute(sql, val)
                mydb.commit()

                flash("Report sent succesfully")
            except:
                flash("Report has some problems!")
                return redirect(url_for('ReturningPatient'))

    return redirect(url_for('ReturningPatient'))


@app.route("/ReturningPatient", methods=['GET', 'POST'])
def ReturningPatient():
    if 'loggedin' in session:
        DID = session['RID']
        mycursor.execute(
            "SELECT DISTINCT PID FROM APPOINTMENT WHERE APPOINTMENT.DID= %s", (DID,))
        myresult = mycursor.fetchall()

    return render_template('write_report.html', data=myresult)


if __name__ == '__main__':
    app.run(debug=True)
