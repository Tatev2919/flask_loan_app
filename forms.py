from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    confirm_password = StringField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PredictionForm(FlaskForm):
    gender = StringField('Gender', validators=[DataRequired()])
    married = StringField('Married', validators=[DataRequired()])
    dependents = StringField('Dependents', validators=[DataRequired()])
    education = StringField('Education', validators=[DataRequired()])
    self_employed = StringField('Self Employed', validators=[DataRequired()])
    applicant_income = FloatField('Applicant Income', validators=[DataRequired()])
    coapplicant_income = FloatField('Coapplicant Income', validators=[DataRequired()])

    loan_amount = FloatField('Loan Amount', validators=[DataRequired()])
    loan_term = FloatField('Loan Term', validators=[DataRequired()])
    credit_history = FloatField('Credit History', validators=[DataRequired()])
    property_area = StringField('Property Area', validators=[DataRequired()])
    submit = SubmitField('Predict')
