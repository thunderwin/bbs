from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class CMSUser(db.Model):
    __tablename__ = 'cms_user'  #why？
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(50),nullable=False)
    _password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(50),nullable=False,unique=True)  #注意这里的 unique ,email 必须是唯一的
    join_time = db.Column(db.DateTime,default=datetime.now)

    #以下代码全是为了不明文存储密码
    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self,raw_password):
        result = check_password_hash(self.password,raw_password)
        return result

#密码对外的字段名叫password 对内叫_password
