import os

SECRET_KEY = os.urandom(24)
DEBUG = True

DB_NAME = 'bbs'
DB_USERNAME = 'root'
DB_PASSWORD = '123456'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'


DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False # 不需要每次都通知

CMS_USER_ID = 'gfgregh34hh53h5h5h'
