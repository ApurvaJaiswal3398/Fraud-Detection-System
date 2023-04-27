from flask import Flask, render_template, request, redirect
from database import Transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session  
# import plotly.express as px
# from database import Vehicle
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, scoped_session
# from werkzeug.utils import secure_filename


logged_in = False
logged_in_detail = None
otp = None
adminpass = '12345678'
receiver = None
loginmsg = None
alert = None
pschanged = False
admincount = 0

def noneall():
    global otp
    global adminpass
    global receiver
    global loginmsg
    global pschanged
    otp = adminpass = receiver = loginmsg = None
    pschanged = False

app = Flask(__name__)

def getdb():
    engine = create_engine('sqlite:///project.sqlite')  # Creating Database Engine
    DBSession = sessionmaker(bind=engine)   # Creating Session for Database
    session = scoped_session(DBSession)
    return session

@app.route('/')
def index():
    # name = "Sample Project One"     # Random Name for a Button
    print(f"Logged In : {logged_in}\nOTP : {otp}\nAdmin Pass : {adminpass}\nReceiver : {receiver}\nLogin Msg : {loginmsg}\nPassword Changed : {pschanged}")
    return render_template('base.html', title='Home Page', logged_in=logged_in, message = loginmsg, alert=alert)

@app.route('/login', methods=['GET','POST'])
def login():
    message = None
    global alert
    alert = 'danger'
    global logged_in
    global logged_in_detail
    global loginmsg
    if request.method == "POST":
        login_email = request.form.get('login_email')
        login_password = request.form.get('login_password')
        print("Login Detail : ",login_email, login_password)
        if login_email == 'admin@fraud.com':
            if login_password == adminpass:
                print("Admin Login Successful")
                loginmsg = 'Admin Login Successful!'
                alert = 'success'
                logged_in = True
                logged_in_detail = {'name':'Admin', 'email':'admin@fraud.com', 'password':adminpass, 'admin':'True'}
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
    return render_template('login.html', title='Login', logged_in=logged_in, user=logged_in_detail, message=message, alert=alert)

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

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    # graph = create_plot()
    # ids,graphJSON = index()
    # User_cursor = Users.find().sort("username").limit(8)
    # Cart_cursor = Carts.find().sort("_id").limit(8)
    # Product_cursor = Products.find().sort("_id")
    # Customer_cart_cursor = Customer_Cart.find().sort("used_date").limit(8)
    # Billing_cursor = Billing.find().sort("_id")
    # billing_chart_data = Billing.find().sort("date")
    global loginmsg
    loginmsg = None
    global alert
    if request.method == 'POST':
        # if request.form['submit_button'] == 'Submit':
        trans_type=request.form.get('trans_type') 
        trans_amt=request.form.get('trans_amt')
        trans_nameOrig=request.form.get('trans_nameOrig')
        trans_oldbalanceOrig=request.form.get('trans_oldbalanceOrg')
        trans_newbalanceOrig=request.form.get('trans_newbalanceOrig')
        trans_nameDest=request.form.get('trans_nameDest')
        trans_oldbalanceDest=request.form.get('trans_oldbalanceOrg')
        trans_newbalanceDest=request.form.get('trans_newbalanceOrig')

        db = getdb()
        db.add(Transaction(type=trans_type, amount=trans_amt, nameOrig=trans_nameOrig, oldbalanceOrig=trans_oldbalanceOrig, newbalanceOrig=trans_newbalanceOrig, nameDest=trans_nameDest, oldbalanceDest=trans_oldbalanceDest, newbalanceDest=trans_newbalanceDest))
        db.commit()
        db.close()
        print('Data Saved Successfully')
        alert = 'success'
        loginmsg = 'Data Saved Successfully!'
        return redirect('/dashboard')
    print(f"Logged In : {logged_in}")
    return render_template('dashboard.html', title='Dashboard', logged_in=logged_in, message = loginmsg, alert=alert)#, graphJSON=graphJSON, ids=ids)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8000, debug=True)
    app.run(host='127.0.0.1', port=8000, debug=True)