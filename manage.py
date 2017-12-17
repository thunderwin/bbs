from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate #注意大小写
from bbs import create_app
from exts import db
from apps.cms import models as cms_models

CMSUser = cms_models.CMSUser # 实例化一个后台用户模型
app = create_app()  #实例化一个包装后的 app

manager = Manager(app)
Migrate(app,db)
manager.add_command('db',MigrateCommand)   # 把来自 flask_migrate 的值添加进去

#接下来写需要手动增加后台用户的脚本
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_cms_user(username,password,email):
    user = CMSUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    print('cms用户添加成功！')

if __name__ == '__main__':
    manager.run()
