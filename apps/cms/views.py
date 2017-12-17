from flask import Blueprint,views,render_template,request,session,redirect,url_for,g,jsonify
from .forms import LoginForm,ResetpwdForm #平级别引用 前面加.
from .models import CMSUser
from .decoraters import login_required
import config
from exts import db
from utils import restful

cms_bp = Blueprint('cms',__name__,url_prefix='/cms') #创建蓝图对象

@cms_bp.route('/')
@login_required
def index():
    # g.cms_user
    return render_template('cms/cms_index.html')

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
        pass

cms_bp.add_url_rule('/resetemail/',view_func=ResetEmailView.as_view('resetemail'))
