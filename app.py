import joblib
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from db import db  # Import the db instance from db.py
from models import User, Prediction  # Import User and Prediction models
from forms import RegistrationForm, LoginForm, PredictionForm  # Import forms
import pandas as pd

# Flask app init
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# init db
db.init_app(app)

model = joblib.load('model/loan_pipe.pkl')
# Setup Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login' 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# home route
@app.route('/')
def index():
    return render_template('index.html')

# register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')
    return render_template('login.html', form=form)

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Loan Prediction route
@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    form = PredictionForm()
    if form.validate_on_submit():
        print("Form is valid!") 
        print(f"Coapplicant Income: {form.coapplicant_income.data}")  
        
        # form data for the model
        df = pd.DataFrame([{
            'Gender': form.gender.data,
            'Married': form.married.data,
            'Dependents': form.dependents.data,
            'Education': form.education.data,
            'Self_Employed': form.self_employed.data,
            'ApplicantIncome': form.applicant_income.data,
            'CoapplicantIncome': form.coapplicant_income.data,
            'LoanAmount': form.loan_amount.data,
            'Loan_Amount_Term': form.loan_term.data,
            'Credit_History': form.credit_history.data,
            'Property_Area': form.property_area.data
        }])

        print(df)

        result = model.predict(df)[0]
        print(f'Prediction result: {result}')

        prediction = Prediction(
            result=result,
            user_id=current_user.id
        )
        db.session.add(prediction)
        db.session.commit()
        flash(f'Loan Prediction: {result}', 'success')

        return redirect(url_for('dashboard'))
    else:
        print("Form is not valid!")
        print(form.errors)
    return render_template('prediction.html', form=form)

# dashboard route
@app.route('/dashboard')
@login_required
def dashboard():
    predictions = Prediction.query.filter_by(user_id=current_user.id).all()
    print(predictions)  # Check if predictions are retrieved
    return render_template('dashboard.html', predictions=predictions)


# init the database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

