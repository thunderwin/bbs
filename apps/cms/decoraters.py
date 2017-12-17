from flask import session,redirect,url_for
from functools import wraps #写装饰器必须引入
import config

def login_required(func):

    @wraps(func)
    def inner(*args,**kwargs):
        if config.CMS_USER_ID in session:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('cms.login'))
    return inner  #这里不能带 inner()


