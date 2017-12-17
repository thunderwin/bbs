from flask import Blueprint,views,render_template,request,session,redirect,url_for,g,jsonify
from .forms import LoginForm,ResetpwdForm,ResetEmailForm #平级别引用 前面加.
from .models import CMSUser
from .decoraters import login_required
import config
from exts import db,mail
from utils import restful,cache
from flask_mail import Message
import string
import random

cms_bp = Blueprint('cms',__name__,url_prefix='/cms') #创建蓝图对象

@cms_bp.route('/')
@login_required
def index():
    # g.cms_user
    return render_template('cms/cms_index.html')

@cms_bp.route('/email_captcha/')
def email_carptcha():
    email = request.args.get('email')
    if not email:
        return restful.params_error('请输入邮箱！')

    source  = list(string.ascii_letters) #获取随机的字母列表
    source.extend(map(lambda x:str(x),range(0,10))) # 获取随机数字列表，并转化为字符串类型
    captcha = "".join(random.sample(source,6)) #在生成的随机列表中选出6位字符

    message = Message('BBS论坛修改邮箱验证码',recipients=[email],body='您的验证码是%s' % captcha)
    try:
        mail.send(message)
    except:
        return restful.server_error()
    cache.set(email,captcha) #把邮箱和验证码存到内存中，memcache
    return restful.success()



@cms_bp.route('/email/')
def send_mail():
    message = Message('邮件测试',recipients=['985684077@qq.com'],body='测试以下')
    mail.send(message)
    return 'sucess'



@cms_bp.route('/logout/')
@login_required  #注销前判断你是不是登录了
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))

@cms_bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/profile.html')

class RestPwdView(views.MethodView):  #重制密码
    decorators = [login_required] #加装饰器
    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()

                return restful.success()
            else:
                return restful.params_error('旧密码错误！')

        else:
            return restful.params_error(form.get_error())


cms_bp.add_url_rule('/resetpwd/',view_func=RestPwdView.as_view('resetpwd'))

class LoginView(views.MethodView):
    def get(self,message=None):
        return render_template('cms/cms_login.html',message=message)
    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            print('email')
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):  #如果有这个用户，而且用户密码一样
                session[config.CMS_USER_ID] = user.id
                if remember:
                    session.permanent = True #默认cookie 31天
                return redirect(url_for('cms.index')) #这里反转的时候不能直接写index, 必须加 cms.index 必须加蓝图的名字
            else:
                return self.get(message='邮箱或者密码错误')


        else:
            form.get_error()


cms_bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))

class ResetEmailView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_restemail.html')
    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate(): #如果验证通过
            email = form.email.data
            g.cms_user.email  = email  # 为什么修改g 对象，却能修改数据库里面的值？
            db.session.commit() # 这里为什么能直接提交数据库？
            return restful.success()
        else:
            return restful.params_error(form.get_error())


cms_bp.add_url_rule('/resetemail/',view_func=ResetEmailView.as_view('resetemail'))
