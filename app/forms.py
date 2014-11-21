from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, FileField
from wtforms.validators import DataRequired

class LoginForm(Form):
    #openid = StringField('openid', validators=[DataRequired()])
    #remember_me = BooleanField('remember_me', default=False)
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    wishlist = FileField('wishlist', validators=[DataRequired()])
