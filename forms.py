from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length

class MemberRegistration(FlaskForm):
    """Form for registering new members."""

    name = StringField('Username', validators=[DataRequired()])
    address = StringField('Username', validators=[DataRequired()])
    membership_type = SelectField('Membership Type', choices=[('vip', 'VIP'), ('senior', 'Senior'), ('ordinary', 'Ordinary'), ('family', 'Family')], validators=[DataRequired()])


class ClassSignup(FlaskForm):
    """Form for members to signup for classes."""

    member_id = StringField('Member ID', validators=[DataRequired()])
    class_id = SelectField('Class')
