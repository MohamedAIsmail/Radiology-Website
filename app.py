from flask import Flask, redirect, url_for, request, render_template, session, flash, jsonify

import database
from werkzeug.utils import secure_filename

mycursor, mydb = database.connect()

app = Flask(__name__)
app.secret_key = "super secret key"


@app.route('/')
def Home():
    return render_template('Home.html')


@app.route('/Login.html', methods=['POST', 'GET'])
def Register():
    if request.method == 'POST':  ##check if there is post data
        patientFname = request.form['patientFname']
        patientLname = request.form['patientLname']
        PID = request.form['PID']
        patientpassword = request.form['patientpassword']
        sql = "INSERT INTO patients (patientFname, patientLname, PID, patientpassword) VALUES(%s,%s,%s,%s)"
        val = (patientFname, patientLname, PID, patientpassword)
        mycursor.execute(sql, val)
        mydb.commit()
        msg = 'You have successfully registered !'
        return render_template('Login.html', msg=msg)

    return render_template('Login.html')


# ---- Patient Login ----


@app.route('/Login', methods=['POST', 'GET'])
def login():
    msg = ''
    if request.method == 'POST' and 'PID' in request.form and 'patientpassword' in request.form:
        PID = request.form['PID']
        patientpassword = request.form['patientpassword']
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute(
            'SELECT * FROM PATIENTS WHERE PID = %s AND patientpassword = %s', (PID, patientpassword))
        account = mycursor.fetchone()
        mydb.commit()
        print(PID, patientpassword)

        if account:
            session['loggedin'] = True
            session['PID'] = account[2]
            session['patientpassword'] = account[3]
            return redirect(url_for('patientProfile'))
        else:
            msg = 'Incorrect username/password!'

    return render_template('Login.html', msg=msg)


# ---- Doctor_login ----


@app.route('/Login', methods=['POST', 'GET'])
def doctorlogin():
    msg = ''
    if request.method == 'POST' and 'DID' in request.form and 'doctorpassword' in request.form:
        DID = request.form['DID']
        doctorpassword = request.form['doctorpassword']
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute(
            'SELECT * FROM DOCTORS WHERE DID=%s AND doctorpassword=%s', (DID, doctorpassword))
        account = mycursor.fetchone()
        mydb.commit()
        print(DID, doctorpassword)

        if account:
            session['loggedin'] = True
            session['DID'] = account[2]
            session['doctorpassword'] = account[3]
            return redirect(url_for('doctorProfile'))
        else:
            msg = 'Incorrect username/password!'

    return render_template('doctor-login.html', msg=msg)


# ---- Admin-Login ----


@app.route('/adminlogin', methods=['POST', 'GET'])
def adminlogin():
    msg = ''
    if request.method == 'POST' and 'AID' in request.form and 'adminpassword' in request.form:
        AID = request.form['AID']
        adminpassword = request.form['adminpassword']
        #   mycursor = mydb.cursor (buffered=True)
        mycursor.execute('SELECT * FROM ADMINS WHERE AID=%s AND adminpassword=%s', (AID, adminpassword,))
        account = mycursor.fetchone()

        if account:
            session['loggedin'] = True
            session['AID'] = account[2]
            session['adminpassword'] = account[3]
            return redirect(url_for('adminProfile'))
        else:
            msg = 'Incorrect username/password!'

    return render_template('admin-login.html', msg=msg)


# ---- Logout ----

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('PID', None)
    session.pop('patientpassword', None)
    return redirect(url_for('Home'))


# ---- Doctor profile ----

@app.route("/doctorProfile", methods=['GET', 'POST'])
def doctorProfile():
    if 'loggedin' in session:
        if request.method == 'POST':
            doctorFname = request.form['doctorFname']
            doctorLname = request.form['doctorLname']
            doctorpassword = request.form['doctorpassword']
            Age = request.form['Age']
            clinicname = request.form['clinicname']
            Gender = request.form['Gender']
            mobilephone = request.form['mobilephone']
            salary = request.form['salary']
            Email = request.form['Email']
            DID = session['DID']
            sql = "UPDATE doctors SET doctorFname =%s, doctorLname=%s, doctorpassword=%s, Age=%s, mobilephone=%s, Gender=%s, salary=%s,clinicname=%s,Email=%s   WHERE DID =%s"
            val = (doctorFname, doctorLname, doctorpassword, Age, mobilephone, Gender, salary, clinicname, Email, DID)
            mycursor.execute(sql, val)
            mydb.commit()
        DID = session['DID']
        sql = "SELECT * FROM doctors WHERE DID = %s"
        val = (DID,)
        mycursor.execute(sql, val)
        account = mycursor.fetchone()
        return render_template("Doctor/doctorProfile.html", account=account)
    return redirect(url_for('doctor-login'))


# patientProfile
@app.route("/patientProfile", methods=['GET', 'POST'])
def patientProfile():
    if 'loggedin' in session:
        if request.method == 'POST':
            patientFname = request.form['patientFname']
            patientLname = request.form['patientLname']
            patientpassword = request.form['patientpassword']
            Age = request.form['Age']
            mobilephone = request.form['mobilephone']
            Gender = request.form['Gender']
            M1 = request.form['M1']
            M2 = request.form['M1']
            M3 = request.form['M1']
            M4 = request.form['M1']
            M5 = request.form['M1']
            PID = session['PID']
            sql = "UPDATE patients SET  patientFname =%s, patientLname=%s, patientpassword=%s, Age=%s, mobilephone=%s, Gender=%s, M1=%s, M2=%s, M3=%s, M4=%s, M5=%s WHERE PID =%s"
            val = (patientFname, patientLname, patientpassword, Age, mobilephone, Gender, M1, M2, M3, M4, M5, PID)
            mycursor.execute(sql, val)
            mydb.commit()
        PID = session['PID']
        sql = "SELECT * FROM patients WHERE PID = %s"
        val = (PID,)
        mycursor.execute(sql, val)
        account = mycursor.fetchone()
        return render_template("patientProfile.html", account=account)
    return redirect(url_for('login'))


# Admin Profile
@app.route("/adminProfile", methods=['GET', 'POST'])
def adminProfile():
    if 'loggedin' in session:
        if request.method == 'POST':
            adminFname = request.form['adminFname']
            adminLname = request.form['adminLname']
            adminpassword = request.form['adminpassword']
            Age = request.form['Age']
            clinicname = request.form['clinicname']
            Gender = request.form['Gender']
            mobilephone = request.form['mobilephone']
            salary = request.form['salary']
            Email = request.form['Email']
            AID = session['AID']
            sql = "UPDATE admins SET adminFname =%s, adminLname=%s, adminpassword=%s, Age=%s, mobilephone=%s, Gender=%s, salary=%s,clinicname=%s,Email=%s   WHERE AID =%s"
            val = (adminFname, adminLname, adminpassword, Age, mobilephone, Gender, salary, clinicname, Email, AID)
            mycursor.execute(sql, val)
            mydb.commit()
        AID = session['AID']
        sql = "SELECT * FROM admins WHERE AID = %s"
        val = (AID,)
        mycursor.execute(sql, val)
        account = mycursor.fetchone()
        return render_template("adminProfile.html", account=account)
    return redirect(url_for('admin-login'))


# patient

@app.route('/addPatient', methods=['GET', 'POST'])
def addPatient():
    if request.method == 'POST':
        PatientName = request.form['name']
        PID = request.form['PID']
        Age = request.form['Age']
        print(PatientName, PID, Age)
        sql = "INSERT INTO Patients (PatientName,PID,Age) VALUES (%s, %s, %s)"
        val = (PatientName, PID, Age)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('View Patient.html')
    else:
        return render_template('Add Patient.html')


@app.route('/viewPatient')
def viewPatient():
    if session['DID']:
        DID = session['DID']
        sql = "SELECT patientFname,patientLname,PID,Age,mobilephone,Gender FROM patients WHERE DID = %s"
        val = (DID,)
        mycursor.execute(sql, val)
        data = mycursor.fetchall()
        return render_template("viewPatient.html", data=data)
    else:
        return render_template("doctor-login.html")

    # Appointment


@app.route('/addAppointment', methods=['GET', 'POST'])
def addAppointment():
    if request.method == 'POST':
        clinicname = request.form['clinicname']
        doctorFname = request.form['doctorFname']
        appointmentdate = request.form['appointmentdate']
        appointmenttime = request.form['appointmenttime']
        patientName = request.form['patientName']
        mobilephone = request.form['mobilephone']

        sql = "INSERT INTO appointment (doctorFname, appointmentdate , appointmenttime , patientName, mobilephone) VALUES (%s, %s,%s,%s,%s)"
        val = (doctorFname, appointmentdate, appointmenttime, patientName, mobilephone)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('Home.html')

    else:
        return redirect(url_for('addAppointment'))


@app.route('/ViewAppointmentpatient')
def ViewAppointmentpatient():
    if request.method == 'POST':
        return redirect(url_for('addAppointment'))
    else:
        PID = session['PID']
        sql = "SELECT PID,patientName,clinicname,doctorFname,appointmentdate,appointmenttime FROM appointment WHERE PID = %s"
        val = (PID,)
        mycursor.execute(sql, val)
        Appointmentdata = mycursor.fetchall()
        return render_template('ViewAppointment-patient.html', Data=Appointmentdata)


@app.route('/ViewAppointmentdoctor')
def ViewAppointmentdoctor():
    if request.method == 'POST':
        return redirect(url_for('addAppointment'))
    else:
        DID = session['DID']
        sql = "SELECT doctorFname,patientName,appointmentdate,appointmenttime FROM appointment WHERE DID = %s"
        val = (DID,)
        mycursor.execute(sql, val)
        Appointmentdata = mycursor.fetchall()
        return render_template('ViewAppointment-doctor.html', Data=Appointmentdata)


# Compliants
@app.route('/addCompliants', methods=['GET', 'POST'])
def addCompliants():
    if request.method == 'POST':
        Name = request.form['Name']
        email = request.form['email']
        subject = request.form['subject']
        yourcompliants = request.form['yourcompliants']
        sql = "INSERT INTO compliants (Name , email , subject , yourcompliants) VALUES (%s, %s, %s, %s)"
        val = (Name, email, subject, yourcompliants)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('Home.html')
    else:
        return redirect(url_for('addCompliants'))


@app.route('/ViewCompliants')
def ViewCompliants():
    if request.method == 'POST':
        return redirect(url_for('addCompliants'))
    else:
        mycursor.execute("SELECT * FROM compliants")
        compliants = mycursor.fetchall()
        return render_template('ViewCompliants.html', Data=compliants)


#
# ADMINS
#

# ADD DOCTOR
@app.route('/Add Doctor', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        doctorFname = request.form['doctorFname']
        doctorLname = request.form['doctorLname']
        DID = request.form['DID']
        doctorpassword = request.form['doctorpassword']
        Age = request.form['Age']
        clinicname = request.form['clinicname']
        Gender = request.form['Gender']
        mobilephone = request.form['mobilephone']
        salary = request.form['salary']
        Email = request.form['Email']
        sql = "INSERT INTO doctors (doctorFname, doctorLname,DID, doctorpassword, Age, mobilephone, Gender, salary,clinicname,Email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
        val = (doctorFname, doctorLname, DID, doctorpassword, Age, mobilephone, Gender, salary, clinicname, Email)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('Add Doctor.html', msg="Doctor is added")


    else:
        return render_template('Add Doctor.html', msg="Somthing wrong")


# VIEW DOCTOR
@app.route('/View Doctors')
def view_doctors():
    mycursor.execute("SELECT * FROM doctors")
    myresult = mycursor.fetchall()
    return render_template('View Doctors.html', DoctorData=myresult)


# DELETE DOCTOR
@app.route('/DeleteDoctor/<string:id>', methods=["GET"])
def delete_doctor(id):
    try:
        mycursor.execute("DELETE FROM doctors WHERE DID = %s", (id,))
        mydb.commit()
        return redirect(url_for('view_doctors'))
    except:
        return render_template('View Doctors.html', mssg="Somthing wrong")


# EDIT DOCTOR
@app.route('/EditDoctor/<int:id>', methods=["GET", "POST"])
def editdoctor(id):
    sql = "SELECT * FROM doctors WHERE DID=%s"
    mycursor.execute(sql, (id,))
    account = mycursor.fetchone()
    mydb.commit()
    return render_template("Update doctor.html", datas=account)


# UPDATE DOCTOR
@app.route('/UpdateDoctor/<id>', methods=["POST"])
def update_doctor(id):
    if request.method == 'POST':
        try:
            doctorFName = request.form['doctorFname']
            doctorLname = request.form['doctorLname']
            clinicname = request.form['clinicname']
            Age = request.form['Age']
            mobilephone = request.form['mobilephone']
            Email = request.form['Email']
            sql = "UPDATE doctors SET doctorFname=%s doctorLname=%s clinicname=%s Age=%s mobilephone=%s Email=%s where DID=%s"
            mycursor.execute(sql, (doctorFName, doctorLname, clinicname, Age, mobilephone, Email, id))
            mydb.commit()
            return redirect(url_for('view_doctors'))
        except:
            return render_template("View Doctors.html")


# =========

# stats
@app.route('/stats', methods=['POST', 'GET'])
def stats():
    if request.method == 'POST':
        return render_template('adminProfile.html')
    else:
        mycursor.execute("SELECT doctorFname,doctorLname,DID,salary FROM doctors ORDER BY salary DESC LIMIT 5;")
        datastats = mycursor.fetchall()
        return render_template('stats.html', data=datastats)


@app.route('/Avarage', methods=['POST', 'GET'])
def Avarage():
    if request.method == 'POST':
        return render_template('adminProfile.html')
    else:
        mycursor.execute("SELECT AVG(salary) AS 'Salaries Avarage'FROM doctors;")
        dataavg = mycursor.fetchall()
        return render_template('stats.html', data=dataavg)


@app.route('/Count-doctors', methods=['POST', 'GET'])
def Countdoctors():
    if request.method == 'POST':
        return render_template('adminProfile.html')
    else:
        mycursor.execute("SELECT COUNT(DID) AS 'Doctors'FROM doctors;")
        datacountd = mycursor.fetchall()
        return render_template('stats.html', data=datacountd)


@app.route('/Count-patients', methods=['POST', 'GET'])
def Countpatients():
    if request.method == 'POST':
        return render_template('adminProfile.html')
    else:
        mycursor.execute("SELECT COUNT(PID) AS 'Patients'FROM patients;")
        datacountp = mycursor.fetchall()
        return render_template('stats.html', data=datacountp)


# *********************************** REPORT SECTION *******************************************
@app.route('/upload', methods=['POST'])
def upload():
    scan = request.files['scan']
    if not scan:
        return 'No scan uploaded', 400
    filename = secure_filename(scan.filename)
    mimtype = scan.mimetype
    # img = Img(img=scan.read(), mimtype=mimtype, name=filename)


@app.route('/Write_Report', methods=['POST', 'GET'])
def write_report():
    pass


if __name__ == '__main__':
    app.run(debug=True)