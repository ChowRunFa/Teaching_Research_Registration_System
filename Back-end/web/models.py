# -*- coding: utf-8 -*-
# @Time    : 2022/6/26 16:22
# @Author  : ChowRunFa
# @File    : models.py
# @Software: PyCharm
from flask_sqlalchemy import SQLAlchemy
import simplejson as json#pip install simplejson 或者 pip install python-simplejson
from server import Connection

db = SQLAlchemy()

def result(code=200, msg = 'success',d={}):
    data = dict()#object.__dict__
    data['code'] = code
    data['msg'] = msg
    data['data'] = d
    return json.dumps(data,ensure_ascii=False)


# def result(code=200,d={}):
#     data = dict()#object.__dict__
#     data['code'] = code
#     data['data'] = d
#     return json.dumps(data,ensure_ascii=False)

class Charge(db.Model):
    __tablename__ = 'charge'
    workno = db.Column(db.String(5), db.ForeignKey('teacher.workno'), primary_key=True)
    id = db.Column(db.String(255), db.ForeignKey('project.id'), primary_key=True)
    ranking = db.Column(db.Integer)
    fund = db.Column(db.Float)

    __table_args__ = (
        db.CheckConstraint('ranking > 0'),
        db.CheckConstraint('fund >= 0'),
        {'comment': '发表论文和承担项目中的排名：1-表示排名第一，以此类推。论文排名第一即为第一作者，承担项目排名第一即为项目负责人。'}
    )

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    property = db.Column(db.Integer, nullable=False)
    __table_args__ = (
        db.CheckConstraint('hours > 0'),
    )

class Paper(db.Model):
    __tablename__ = 'paper'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(256), nullable=False)
    source = db.Column(db.String(256), nullable=False)
    year = db.Column(db.Date, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        {'comment': '论文类型为整数：1-full paper，2-short paper，3-poster paper，4-demo paper'}
    )

class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    source = db.Column(db.String(256), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    totalfund = db.Column(db.Float, nullable=False)
    startyear = db.Column(db.Integer, nullable=False)
    endyear = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.CheckConstraint('type in (1, 2, 3, 4, 5)'),
        db.CheckConstraint('totalfund >= 0'),
        db.CheckConstraint('startyear <= endyear'),
        {'comment': '项目类型为整数：1-国家级项目，2-省部级项目，3-市厅级项目，4-企业合作项目，5-其它类型项目。'}
    )

class Publication(db.Model):
    __tablename__ = 'publication'
    id = db.Column(db.Integer, db.ForeignKey('paper.id', ondelete='CASCADE'), primary_key=True)
    workno = db.Column(db.String(5), db.ForeignKey('teacher.workno'), primary_key=True)
    ranking = db.Column(db.Integer)
    corresponding = db.Column(db.Boolean)

    __table_args__ = (
        db.CheckConstraint('ranking > 0'),
        {'comment': '发表论文和承担项目中的排名：1-表示排名第一，以此类推。论文排名第一即为第一作者，承担项目排名第一即为项目负责人。'}
    )

class Teacher(db.Model):
    __tablename__ = 'teacher'
    workno = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.CheckConstraint('gender in (1, 2)'),
        db.CheckConstraint('level > 0'),
        {'comment': '性别为整数，1-男，2-女\n\n教师职称为整数：1-博士后，2-助教，3-讲师，4-副教授，5-'}
    )

class Teaching(db.Model):
    __tablename__ = 'teaching'
    workno = db.Column(db.String(5), db.ForeignKey('teacher.workno'), primary_key=True)
    id = db.Column(db.String(255), db.ForeignKey('course.id'), primary_key=True)
    year = db.Column(db.Integer)
    semester = db.Column(db.Integer)
    hours = db.Column(db.Integer)

    __table_args__ = (
        db.CheckConstraint('year > 1957'),
        db.CheckConstraint('hours > 0'),
        {'comment': '主讲课程中的学期取值为：1-春季学期，2-夏季学期，3-秋季学期。'}
    )