from flask import Flask, render_template, request, redirect
# import plotly.express as px
# from database import Vehicle
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, scoped_session
# from werkzeug.utils import secure_filename

app = Flask(__name__)

# def getdb():
#     engine = create_engine('sqlite:///project.sqlite')  # Creating Database Engine
#     DBSession = sessionmaker(bind=engine)   # Creating Session for Database
#     session = scoped_session(DBSession)
#     return session

@app.route('/')
def index():
    # name = "Sample Project One"     # Random Name for a Button
    return render_template('index.html')


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8000, debug=True)
    app.run(host='127.0.0.1', port=8000, debug=True)