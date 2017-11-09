from ..models import User, Team
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

class NewTeam(FlaskForm):
    name = StringField('TEAM NAME', validators=[InputRequired("Required")])
    city = StringField('CITY', validators=[InputRequired("Required")])
    submit = SubmitField('Add New Team')
