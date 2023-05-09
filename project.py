from flask import Flask, render_template, request, redirect
from database import Transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
from datetime import datetime
from flask_bcrypt import Bcrypt
# import plotly.express as px
# from database import Vehicle
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, scoped_session
# from werkzeug.utils import secure_filename
from fraud_detection import predict
import pandas as pd
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Global Variables
logged_in = False
# logged_in_detail = None
otp = None
adminpass = None
with open(r'pwd.pwd', 'r') as f:
    adminpass = f.read()
receiver = None
loginmsg = None
alert = None
pschanged = False

# Function to reset global variables
def noneall():
    global otp
    global adminpass
    global receiver
    global loginmsg
    global pschanged
    otp = receiver = loginmsg = None
    pschanged = False

#function to load database table into a pandas dataframe
def load_data():
    engine = create_engine('sqlite:///project.sqlite').connect()    # Creating Database Engine
    df = pd.read_sql_table('transactions', engine)  # Reading Database Table into Pandas DataFrame
    print(df.head())    # Printing DataFrame
    return df   # Returning DataFrame

# Function to get database session
def getdb():
    engine = create_engine('sqlite:///project.sqlite')  # Creating Database Engine
    DBSession = sessionmaker(bind=engine)   # Creating Session for Database
    session = scoped_session(DBSession) # Creating Scoped Session for Database
    return session

@app.route('/')
def index():
    # name = "Sample Project One"     # Random Name for a Button
    print(f"Logged In : {logged_in}\nOTP : {otp}\nAdmin Pass : {adminpass}\nReceiver : {receiver}\nLogin Msg : {loginmsg}\nPassword Changed : {pschanged}")
    # return render_template('base.html', title='Home Page', logged_in=logged_in, message = loginmsg, alert=alert)
    return redirect('/homepage')

@app.route('/login', methods=['GET','POST'])
def login():
    message = None
    global alert
    alert = 'danger'
    global logged_in
    # global logged_in_detail
    global loginmsg
    global adminpass
    if request.method == "POST":
        login_email = request.form.get('login_email')
        login_password = request.form.get('login_password')
        print("Login Detail : ",login_email, login_password)
        if login_email == 'mihirsuyash7@gmail.com':
            if adminpass == login_password:
                print("Admin Login Successful")
                loginmsg = 'Admin Login Successful!'
                alert = 'success'
                logged_in = True
                # logged_in_detail = {'name':'Admin', 'email':'jaiswal.apurva.aj011@gmail.com', 'password':adminpass, 'admin':'True'}
                return redirect('/')
            else:
                print("Admin Password Not matched")
                message = 'Invalid Email or Password!'
                logged_in = False
        else:
            print("Invalid Username")
            message = 'Invalid Email or Password!'
            logged_in = False
    if not message and loginmsg:
        message = loginmsg
        alert = 'success'
        if pschanged:
            noneall()
    print(f"Logged In : {logged_in}\nOTP : {otp}\nAdmin Pass : {adminpass}\nReceiver : {receiver}\nLogin Msg : {loginmsg}\nPassword Changed : {pschanged}")
    return render_template('login1.html', title='Login', logged_in=logged_in, message=message, alert=alert)

# Function to generate and send customised email while resetting password
def send_mail(cpass):
    sender = 'jaiswal.apurva.aj011@gmail.com'
    subject = 'FraudSense Account Password Reset OTP Mail'
    global otp
    # companypass = cpass
    otp = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    msg = '''<h4 style='color: #292b2c;'>FraudSense Account</h4>
        <big><h1 style='color: #0275d8;'>Password reset code</h1></big>
        <p>Please use this code to reset the password for the FraudSense account with email ''' + receiver + '''.</p><br>
        <p>Here is your code : <big><b>''' + otp + '''</b></big><br><br>Thanks.<br>The FraudSense Team</p>'''
    success = False
    m = MIMEMultipart('alternative')
    m['From'] = sender
    m['To'] = receiver
    m['Subject'] = subject
    m.attach(MIMEText(msg,'html'))
    print(f'sender : {sender}\nReceiver : {receiver}\nOTP : {otp}\nMessage : {msg}\nSuccess : {success}\nMIME Content : {m}')

    # con = smtplib.SMTP('smtp.gmail.com', 587)
    con = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    print('Connected to SMTP Server')
    # con.starttls()
    # print('TLS Encryption Enabled')
    try:
        con.login(sender, cpass)
        print('Logged In by Company Email')
        msg_content = m.as_string()
        print('Message Created for the Mail to be Sent : \n',msg_content)
        # con.sendmail(sender, receiver, 'Subject: So long.\nDear Alice, so long and thanks for all the fish. Sincerely, Bob')
        con.sendmail(sender, receiver, msg_content)
        print('Mail Sent')
        success = True
    except smtplib.SMTPAuthenticationError:
        print('Wrong Company Password Entered!')
        otp = None
        success = False
    finally:
        con.quit()
        print('Logged out of the Company Mail')
        print('Sending Process Ended')
        return success

@app.route('/forgotpassword', methods=['GET','POST'])
def forgotpassword():
    message=None
    global logged_in
    global receiver
    if request.method == "POST":
        receiver = request.form.get('receiver')
        # admin_pass = request.form.get('admin_pass')
        with open('E:\Fraud Detection Documents\EMAIL_PASS.pwd', 'r') as f:
            comp_pass = f.read()
        print("Mail Receiver : ",receiver," Company Password : ", comp_pass)
        # x = Users.find_one({'email': receiver})
        # print('Receiver Data : ',receiver)
        # if x:
        if send_mail(comp_pass):
            print(f'Mail Sent to Receiver {receiver} with OTP : {otp}')
            return redirect('/OTPVerification')
        else:
            message = 'Sender\'s Password is Wrong!'
        # else:
        #     message = 'No User for given Email Found!'
    print(f"Logged In : {logged_in}")
    return render_template('forgotpassword.html', title='Forgot Password', message=message)

@app.route('/OTPVerification', methods=['GET','POST'])
def otpverification():
    if request.method == "POST":
        verify = request.form.get('otp')
        if verify == otp:
            print('OTP Matched!')
            return redirect('/ChangePassword')
        else:
            print('Wrong OTP Entered!')
    return render_template('otpverification.html', title='OTP Verification', otp=otp)

@app.route('/ChangePassword', methods=['GET','POST'])
def changepassword():
    global loginmsg
    global adminpass
    if request.method == "POST":
        np = request.form.get('newpass')
        cp = request.form.get('confpass')
        print('New Password : ',np)
        print('Confirm Password : ',cp)
        if np == cp:
            print('New Pasword Matched!')
            print('Receiver Data whose Password is to be changed : ',receiver)
            with open(r'pwd.pwd', 'w') as f:
                f.write(np)
                adminpass = np
            print(f'Password Changed Successfully! for user {receiver}\n')
            # send_confirmation()
            global pschanged
            pschanged = True
            loginmsg = 'Password Changed Successfully. You can login to your account now.'
            return redirect('/login')
        else:
            print('New Password did not match! Re-Enter Passwords.')
    return render_template('changepassword.html', title='Change Password')

@app.route('/logout')
def logout():
    global logged_in
    logged_in = False
    global alert
    alert = None
    global loginmsg
    loginmsg = None
    print(f"Logged in : {logged_in}")
    return redirect('/login')

# @app.route('/insert', methods=['GET','POST'])
# def insert():
#     global logged_in
#     global loginmsg
#     global alert
#     df = load_data()
#     if request.method == 'POST':
#         # df = df.to_html()
#         return render_template('dashboard.html', title='Dashboard', result = df.to_html(), logged_in=logged_in, message=loginmsg, alert=alert)
#     return render_template('dashboard.html', title='Dashboard', result = df.to_html(), logged_in=logged_in, message=loginmsg, alert=alert)

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    global loginmsg
    loginmsg = data = None
    global alert
    df = load_data()
    if request.method == 'POST':
        # if request.form['submit_button'] == 'Submit':
        trans_type=request.form.get('trans_type') 
        trans_amt=request.form.get('trans_amt')
        trans_nameOrig=request.form.get('trans_nameOrig')
        trans_oldbalanceOrig=request.form.get('trans_oldbalanceOrg')
        trans_newbalanceOrig=request.form.get('trans_newbalanceOrig')
        trans_nameDest=request.form.get('trans_nameDest')
        trans_oldbalanceDest=request.form.get('trans_oldbalanceDest')
        trans_newbalanceDest=request.form.get('trans_newbalanceDest')
        
        # Creting dictionary for extracted data
        data = {'type': trans_type, 'amount': trans_amt, 'srcacc': trans_nameOrig, 'srcold': trans_oldbalanceOrig, 'srcnew': trans_newbalanceOrig, 'destacc': trans_nameDest, 'destold': trans_oldbalanceDest, 'destnew': trans_newbalanceDest, 'datetime': datetime.now(), 'isFraud': 0}
        if trans_type and trans_amt and trans_nameOrig and trans_oldbalanceOrig and trans_newbalanceOrig and trans_nameDest and trans_oldbalanceDest and trans_newbalanceDest:
            tdata = pd.DataFrame({'step': [1],
                     'type': [trans_type],
                     'amount': [trans_amt],
                     'name_orig': [trans_nameOrig],
                     'oldbalanceOrg': [trans_oldbalanceOrig],
                     'newbalanceOrig': [trans_newbalanceOrig],
                     'name_dest': [trans_nameDest],
                     'oldbalanceDest': [trans_oldbalanceDest],
                     'newbalanceDest': [trans_newbalanceDest],
                     'datetime': datetime.now(),
                     'is_Fraud': 0
                    })
            print(f'DataFrame => {tdata}')
            model_path = r'models\v1\ann_fraud_detection.h5'
            pp_path = r'models\v1\ann_fraud_detection_preprocessor.jb'
            out = predict(model_path, pp_path, tdata)
            print(out[0][0] > 0.5)
            if out[0][0] > 0.5:
                print('Fraud')
                data['isFraud'] = isFraud = 1
            else:
                print('Not Fraud')
                data['isFraud'] = isFraud = 0
            db = getdb()
            db.add(Transaction(type=trans_type, amount=trans_amt, nameOrig=trans_nameOrig, oldbalanceOrig=trans_oldbalanceOrig, newbalanceOrig=trans_newbalanceOrig, nameDest=trans_nameDest, oldbalanceDest=trans_oldbalanceDest, newbalanceDest=trans_newbalanceDest, date_time=datetime.now(), is_Fraud=isFraud))
            db.commit()
            db.close()
            print('Data Saved Successfully')
            alert = 'success'
            loginmsg = 'Data Saved Successfully!'
            # return redirect('/dashboard')
        else:
            print('Data Not Saved')
            alert = 'danger'
            loginmsg = 'Data Not Saved!'
            # return redirect('/dashboard')
    print(f"Logged In : {logged_in}")
    print(f"Data : {data}")
    return render_template('dashboard.html', title='Dashboard', logged_in=logged_in, message = loginmsg, alert=alert, result = df.to_html(), data=data)

@app.route('/homepage')
def homepage():
    return render_template('homepage1.html', title="Home", logged_in=logged_in, message = loginmsg, alert=alert)

@app.route('/predict/fraud/<int:id>/record', methods=['GET', 'POST'])
def predict_fraud(id):
    db = getdb()
    transaction = db.query(Transaction).filter_by(id=id).first()
    if transaction:
        # convert to data frame
        df = pd.DataFrame([transaction.__dict__])
        # drop the id column
        df = df.drop(['id'], axis=1)
        pp = r'models\\v1\\ann_fraud_detection_preprocessor.jb'
        mp = r'models\\v1\\ann_fraud_detection.h5'
        result = predict(model_path=mp, prepro_path=pp, data_dict=df)
        print(result)
        return render_template('predict_fraud.html', title="Predict Fraud", logged_in=logged_in, message = loginmsg, alert=alert, result=result)
    else:
        return redirect('/dashboard')


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8000, debug=True)
    app.run(host='127.0.0.1', port=8000, debug=True)