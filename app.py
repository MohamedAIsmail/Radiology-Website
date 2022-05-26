from flask import Flask, redirect, url_for, request, render_template, session, flash, jsonify

import database
from werkzeug.utils import secure_filename

mycursor, mydb = database.connect()

app = Flask(__name__)
app.secret_key = "super secret key"


@app.route('/')
def Home():
    return render_template('Home.html')

# ---- Registering ----

@app.route('/Login', methods=['POST', 'GET'])
def Register():
    if request.method == 'POST':  ##check if there is post data
        patientFname = request.form['patientFname']
        patientLname = request.form['patientLname']
        Email = request.form['patientEmail']
        patientpassword = request.form['patientpassword']
        sql = "INSERT INTO patients (patientFname, patientLname, Email, patientpassword) VALUES(%s,%s,%s,%s)"
        val = (patientFname, patientLname, Email, patientpassword)
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

    return render_template('Login.html', msg=msg)


# ---- Admin-Login ----


@app.route('/Login', methods=['POST', 'GET'])
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

    return render_template('Login.html', msg=msg)


# ---- Logout ----

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('PID', None)
    session.pop('patientpassword', None)
    return redirect(url_for('Home'))




if __name__ == '__main__':
    app.run(debug=True)