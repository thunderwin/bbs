from wtforms import Form,StringField,IntegerField
from wtforms.validators import Email,InputRequired,Length,EqualTo
from apps.forms import BaseForm

class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式')])
    password = StringField(validators=[Length(6,20,message='请输入正确的格式的密码')])
    remember = IntegerField() #因为这个值可传，可不传，无需验证


class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6,20,message='请输入正确格式的密码')])
    newpwd = StringField(validators=[Length(6,20,message='请输入正确格式的密码')])
    newpwd2 = StringField(validators=[EqualTo('newpwd',message='新密码设置不一样')])


