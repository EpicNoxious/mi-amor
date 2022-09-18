from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email
from wtforms import StringField, SubmitField, PasswordField, SelectField, SelectMultipleField, DateField, DecimalField
from wtforms.widgets import ListWidget, CheckboxInput


# custom field for checkbox
class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class GetStarted(FlaskForm):
    begin = SubmitField("Get Started")


class SignUp(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    gender = SelectField("Gender", choices=['Male', 'Female', 'Other'], validators=[DataRequired()])
    dob = DateField("Date Of Birth", validators=[DataRequired()])
    height = DecimalField("Height", validators=[DataRequired()])
    profession = StringField("Profession", validators=[DataRequired()])
    interest = SelectField("Interest", choices=['Male', 'Female'], validators=[DataRequired()])
    category = MultiCheckboxField("Category", choices=['music', 'problem solving', 'cook', 'botany', 'photography', 'guitar', 'sketch', 'shop', 'act', 'game', 'exercise', 'dance'])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    signup = SubmitField("Sign Up")


class SignIn(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    signin = SubmitField("Sign In")


class SignOut(FlaskForm):
    signout = SubmitField("Sign Out")
    find_match = SubmitField("Find Match")
