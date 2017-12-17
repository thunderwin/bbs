from flask import Blueprint

front_bp = Blueprint('front',__name__) #前台页面不需要加前缀，

@front_bp.route('/')
def front():
    return 'front index'
