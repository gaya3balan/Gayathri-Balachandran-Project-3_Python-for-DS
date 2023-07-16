from sklearn.preprocessing import StandardScaler

ss = StandardScaler()
from flask import Flask
from flask import render_template, url_for, request, redirect, flash, session
import pickle
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# open and load the pickle file provided in read mode.
model = pickle.load(open('model.pkl', 'rb'))

import pymysql

pymysql.install_as_MySQLdb()

app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['FLASK_ENV'] = 'development'
app.config['SECRET_KEY'] = 'ItShouldBeALongStringOfRandomCharacters'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/loan_prediction_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))

    def __str__(self):
        return f"{self.username} is registered successfully"


db.create_all()


# This is the Home page for the application
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


# This is to register new user details by inserting entries on DB
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("Register.html")

    elif request.method == 'POST':
        validated_username = \
            User.query.filter(User.username == request.form.get('username')).first()

        if validated_username:
            flash('Username is already existing ! ', 'error')
            return redirect(url_for('register'))
        else:
            new_credential = User(username=request.form.get('username'),
                                  password=request.form.get('password'))

            db.session.add(new_credential)
            db.session.commit()

            flash('User registered successfully', 'success')
            url1 = url_for("register")
            print(url1)
            return redirect(url1)


# This is to login into the Loan Prediction application page
@app.route('/userlogin', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("Login.html")

    elif request.method == 'POST':
        validated_user_details = \
            User.query.filter_by(username=request.form.get('username'), password=request.form.get('password')).first()
        if validated_user_details is not None:
            session['logged_in'] = True
            session['username'] = request.form.get('username')
            url1 = url_for("input_data")
            print(url1)
            return redirect(url1)
        else:
            flash('Username or Password is Invalid, please enter correct credentials')
            return redirect(url_for('login'))


# This is the logout from Prediction page
@app.route('/userlogout')
def logout():
    session['logged_in'] = False
    session['username'] = ''
    return redirect(url_for('login'))


# This is for rendering Prediction page for getting user details
@app.route('/input_data', methods=['GET'])
def input_data():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template("predict.html")


# Predict function to read the values from the UI and predict the loan approval value.
@app.route('/predictresults', methods=['GET', 'POST'])
def predict():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template("predict.html")

    elif request.method == 'POST':
        Gender = request.form["gender"]
        Married = request.form["married"]
        Dependents = float(request.form["dependents"])
        Education = request.form["education"]
        Self_employed = request.form["self_employed"]
        Applicant_Income = int(request.form["applicantincome"])
        Coapplicant_Income = float(request.form["coapplicantincome"])
        Loan_Amount = float(request.form["loanamount"])
        Loan_Amount_Term = float(request.form["loan_amount_term"])
        Credit_History = float(request.form["credit_history"])
        Property_Area = request.form["property_area"]

        prediction = model.predict(
            [
                [
                    Gender,
                    Married,
                    Dependents,
                    Education,
                    Self_employed,
                    Applicant_Income,
                    Coapplicant_Income,
                    Loan_Amount,
                    Loan_Amount_Term,
                    Credit_History,
                    Property_Area,
                ]
            ]
        )
        print(prediction)
        output = round(prediction[0], 1)
        print(output)
        if output >= 0.5:
            return render_template(
                "predict.html",
                prediction_text="Congrats!! You are eligible for the loan.".format(
                    output
                ),
            )
        else:
            return render_template(
                "predict.html",
                prediction_text="Sorry, You are not eligible for the loan.".format(
                    output
                ),
            )


if __name__ == "__main__":
    app.run(debug=True)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
