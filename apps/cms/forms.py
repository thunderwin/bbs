from wtforms import Form,StringField,IntegerField
from wtforms.validators import Email,InputRequired,Length,EqualTo
from apps.forms import BaseForm
from utils import cache
from wtforms import ValidationError
from flask import g

class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式')])
    password = StringField(validators=[Length(6,20,message='请输入正确的格式的密码')])
    remember = IntegerField() #因为这个值可传，可不传，无需验证


class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6,20,message='请输入正确格式的密码')])
    newpwd = StringField(validators=[Length(6,20,message='请输入正确格式的密码')])
    newpwd2 = StringField(validators=[EqualTo('newpwd',message='新密码设置不一样')])


class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式')])
    captcha = StringField(validators=[Length(min=6,max=6,message='请输入正确长度的验证码！')])

    #还要验证是不是和内存里的值一样, 写一个函数来验证
    def validate_captcha(self,field):
        captcha = field.data  # 这里不明白，这里是怎么拿到 captcha 的值,field 哪里来的。  这里原来是写错了！
        email = self.email.data
        captcha_cache = cache.get(email)
        if not captcha_cache or captcha.lower() == captcha_cache.lower():
            raise ValidationError('邮箱验证码错误！')

    def validate_email(self,field):
        email = field.data # 这里为什么一定是拿到邮箱，上面和这个一样的，为什么一定是拿到 captcha
        user = g.cms_user
        if user.email == email:
            raise ValidationError('请使用不同的邮箱！')





