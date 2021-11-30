#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from sqlalchemy import Column, String, Float, Integer, DATETIME, and_
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from sqlalchemy.dialects.mysql import DOUBLE
from ServerConfig import DatabaseURL
from ServerConfig import default_app_list
app = Flask(__name__)
# 設定資料庫位置，並建立 app
#path為3條線///
app.config['SQLALCHEMY_DATABASE_URI'] = DatabaseURL
#由於SQLALCHEMY_TRACK_MODIFICATIONS預設為None, 因此我們須給True or False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app)

db = SQLAlchemy(app)

# 创建对象的基类:
# Base = declarative_base()

class icon_define_table(db.Model):
    # 表的名字:
    __tablename__ = 'icon_define_table'

    # 表的结构:
    number = Column(Integer, primary_key=True)
    app = Column(String(100))
    kind = Column(Integer)
    mobility = Column(String(100))
    icon = Column(String(100))
    picture = Column(String(500))
    visual = Column(String(100))
    color_min = Column(Integer)
    color_max = Column(Integer)
    quick_access = Column(Integer)


class static_icon_table(db.Model):
    # 表的名字:
    __tablename__ = 'static_icon_table'

    # 表的结构:
    number = Column(Integer, primary_key=True)
    app_num = Column(Integer)
    name = Column(String(100))
    lat = Column(DOUBLE)
    lng = Column(DOUBLE)
    description = Column(String(500))


# 定义User对象:
class data_pull_from_iottalk(db.Model):
    # 表的名字:
    __tablename__ = 'data_pull_from_iottalk'

    # 表的结构:
    number = Column(Integer, primary_key=True)
    app_num = Column(Integer)
    lat = Column(DOUBLE)
    lng = Column(DOUBLE)
    name = Column(String(100))#Column(Integer)
    value = Column(String(500))
    time = Column(DATETIME)


class iottalk_data_latest_record(db.Model):
    # 表的名字:
    __tablename__ = 'iottalk_data_latest_record'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    app_num = Column(Integer)
    lat = Column(DOUBLE)
    lng = Column(DOUBLE)
    name = Column(String(100))
    value = Column(String(500))
    time = Column(DATETIME)


# 初始化数据库连接:
#engine = create_engine('sqlite:///Dog.db', echo=True)
# 創建表（如果表已經存在，則不會創建）
db.create_all()


# 创建DBSession类型:
#DBSession = sessionmaker(bind=engine)

# insert default application
if __name__ == '__main__':
    for row in default_app_list:
        new_data = icon_define_table(app=row['app'], kind=row['kind'], mobility=row['mobility'], icon=row['icon'], picture=row['picture'], visual=row['visual'], color_min=row['color_min'], color_max=row['color_max'], quick_access=row['quick_access'])
        db.session.add(new_data)
        db.session.commit()