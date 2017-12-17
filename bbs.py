from flask import Flask
import config #导入配置文件
#引入三个蓝图
from apps.cms import cms_bp
from apps.common import common_bp
from apps.front import front_bp
from exts import db,mail
from flask_wtf import CSRFProtect


def create_app():  #定义一个工厂函数
    app = Flask(__name__)
    app.config.from_object(config)

    # 注册三个蓝图
    app.register_blueprint(cms_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(front_bp)

    db.init_app(app) #绑定数据库和app，不然数据库无法连接。
    mail.init_app(app)  #为APP增加mail
    CSRFProtect(app)

    return app




if __name__ == '__main__':
    app = create_app()
    app.run()
