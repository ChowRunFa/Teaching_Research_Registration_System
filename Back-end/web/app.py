# -*- coding: utf-8 -*-
# @Time    : 2022/6/26 20:07
# @Author  : ChowRunFa
# @File    : app.py
# @Software: PyCharm
import datetime
from dateutil.parser import parse
from flask import Flask, jsonify, request, make_response, render_template
from flask_docs import ApiDoc

from models import *
from server import MySQLConfig
from flask_cors import CORS

app = Flask(__name__)
ApiDoc(
    app,
    title="Sample App",
    version="1.0.0",
    description="A simple app API",
)
app.config.from_object(MySQLConfig)
with app.app_context():
    db.init_app(app)
    db.create_all()

cors = CORS(app, resources={r"/*": {"origins": "*"}}) # 注册CORS, "/*" 允许访问所有api

def filter_props(obj):
    return {k: v for k, v in vars(obj).items() if not k.startswith("_sa_")}

def filter_props_date(obj):
    date_format = "%Y" # modify the date format as needed
    props = {}
    for k, v in vars(obj).items():
        if k.startswith("_sa_"):
            continue
        elif isinstance(v, datetime.date):
            props[k] = v.strftime(date_format)
        else:
            props[k] = v
    return props


@app.route('/api/teaching/<string:id>', methods=['GET'])
def get_teachings_by_course(id):
    course = Course.query.get(id)
    if not course:
        return result(400, 'Course not found.'), 404

    teachings = db.session.query(Teaching, Teacher.name, Teacher.gender, Teacher.level)\
                .join(Teacher, Teaching.workno == Teacher.workno)\
                .filter(Teaching.id == id)\
                .all()

    totalhours = Course.query.get(id).hours


    result_list = []
    for teaching, name, gender, level in teachings:
        result_list.append({
            'workno': teaching.workno,
            'name': name,
            'gender': gender,
            'level': level,
            'semester': teaching.semester,
            'year': teaching.year,
            'hours': teaching.hours
        })

    return result(200, 'Teachings found.', {'totalhours':totalhours,'teachings': result_list})

@app.route('/api/charge/<string:id>', methods=['GET'])
def get_project_charges(id):
    charges = db.session.query(Charge, Teacher.name, Teacher.gender, Teacher.level)\
                .join(Teacher, Charge.workno == Teacher.workno)\
                .filter(Charge.id == id)\
                .all()
    totalfund = Project.query.get(id).totalfund

    result_list = []
    for charge, name, gender, level in charges:
        result_list.append({
            'workno': charge.workno,
            'name': name,
            'gender': gender,
            'level': level,
            'ranking': charge.ranking,
            'fund': charge.fund
        })

    return result(200, 'Project charges found.', {'totalfund':totalfund,'charges': result_list})

@app.route('/api/add/paper', methods=['POST'])
def add_paper():
    data = request.get_json()
    id = data['id']
    title = data['title']
    source = data['source']
    # year = datetime.datetime(data['year'], 1, 1).strftime('%Y-%m-%d')
    year = parse(data['year']).strftime('%Y-%m-%d')
    type = data['type']
    level = data['level']
    authors = data['authors']
    corresponding_author = data['corresponding_author']

    # Check if the corresponding author is in the authors list
    if corresponding_author not in authors:
        return result(400,'error: The corresponding author must be one of the authors.'), 400

    # Check if author rankings are unique
    if len(set([author['ranking'] for author in authors])) != len(authors):
        return result(400, 'error: Author rankings must be unique.'), 400

    # Check if the paper type and level are valid
    valid_types = [1, 2, 3, 4]
    valid_levels = [1, 2, 3, 4, 5, 6]
    type = int(type)
    level = int(level)
    id = int(id)
    if  type not in valid_types:
        return result(400,f'error: Paper type must be one of {valid_types}.')
    if  level not in valid_levels:
        return result(400,f'error: Paper level must be one of {valid_levels}.')


# Create the paper object and save it to the database
    paper = Paper(id=id,title=title, source=source, year=year, type=type, level=level)
    db.session.add(paper)
    db.session.commit()

    # Create the publication objects and save them to the database
    for author in authors:
        publication = Publication(id=id,workno=author['workno'], ranking=author['ranking'], corresponding=(author['workno'] == corresponding_author))
        db.session.add(publication)
    db.session.commit()

    return result(200,'Paper registered successfully.'), 201

# Define the API endpoints for project registration
@app.route('/api/add/project', methods=['POST'])
def add_project():
    data = request.get_json()
    id = data['id']
    name = data['name']
    source = data['source']
    type = data['type']
    totalfund = data['totalfund']
    startyear = data['startyear']
    endyear = data['endyear']
    charges = data['charges']

    # Check if charge rankings are unique
    if len(set([charge['ranking'] for charge in charges])) != len(charges):
        # return jsonify({'error': 'Charge rankings must be unique.'}), 400
        return result(400,'error: Charge rankings must be unique.',{})

    # Check if the total fund is equal to the sum of charges
    if totalfund != sum([charge['fund'] for charge in charges]):
        return result(400,'error: The total fund must be equalto the sum of charges.',{})

    # Check if the project type is valid
    valid_types = [1, 2, 3, 4, 5]
    if type not in valid_types:
        return result(400, f'error: Project type must be one of {valid_types}.',{})

    # Create the project object and save it to the database
    project = Project(id=id,name=name, source=source, type=type, totalfund=totalfund, startyear=startyear, endyear=endyear)
    db.session.add(project)
    db.session.commit()

    # Create the charge objects and save them to the database
    for charge in charges:
        charge_obj = Charge(workno=charge['workno'], id=project.id, ranking=charge['ranking'], fund=charge['fund'])
        db.session.add(charge_obj)
    db.session.commit()

    return result(200, 'Project registered successfully.',{})

@app.route('/api/new/course', methods=['POST'])
def new_course():
    data = request.get_json()
    id = int(data['id'])
    name = data['name']
    hours = data['hours']
    property = data['property']

    if Course.query.filter_by(id=id).first() is not None:
        return result(400,'error :Course with id {} already exists'.format(id))


    course = Course(id=id, name=name, hours=hours, property=property)
    db.session.add(course)
    db.session.commit()

    return result(200,'Course {} Created Successfully'.format(name))
    # db.session.add(course)
    # db.session.commit()

# Define the API endpoints for course registration
@app.route('/api/add/course', methods=['POST'])
def add_course():
    data = request.get_json()
    id = data['id']
    name = data['name']
    hours = data['hours']
    property = data['property']
    teachings = data['teachings']

    # Check if the total hours is equal to the sum of teachings
    if hours != sum([teaching['hours'] for teaching in teachings]):
        return result(100,'The total hours must be equal to the sum of teachings.',{})

    # Check if the semester is valid
    valid_semesters = [1, 2, 3]
    for teaching in teachings:
        if teaching['semester'] not in valid_semesters:
            return result(400, f'Teaching semester must be one of {valid_semesters}.',{}), 400

    # Create the course object and save it to the database
    course = Course(id=id, name=name, hours=hours, property=property)
    # db.session.add(course)
    # db.session.commit()

    # Create the teaching objects and save them to the database
    for teaching in teachings:
        teaching_obj = Teaching(workno=teaching['workno'], id=course.id, year=teaching['year'], semester=teaching['semester'], hours=teaching['hours'])
        db.session.add(teaching_obj)
    db.session.commit()

    return result(200,'Course registered successfully.',{}), 201

# Define the API endpoints for paper deletion
@app.route('/api/del/paper/<int:id>', methods=['DELETE'])
def delete_paper(id):
    publications = Publication.query.filter_by(id=id).all()
    if  publications:
        for publication in publications:
            db.session.delete(publication)
        db.session.commit()

    paper = Paper.query.get(id)
    if paper is None:
        return result(400,'Paper not found.')

    db.session.delete(paper)
    db.session.commit()

    return result(200, 'Paper deleted successfully')

# Define the API endpoints for project deletion
@app.route('/api/del/project/<string:id>', methods=['DELETE'])
def delete_project(id):
    charges = Charge.query.filter_by(id=id).all()
    if not charges:
        for charge in charges:
            db.session.delete(charge)
        db.session.commit()


    project = Project.query.get(id)
    if project is None:
        return result(400,'Project not found.')

    db.session.delete(project)
    db.session.commit()

    return result(200,'Project deleted successfully.')

# Define the API endpoints for course deletion
@app.route('/api/del/course/<string:id>', methods=['DELETE'])
def delete_course(id):
    teachings = Teaching.query.filter_by(id=id).all()
    if not teachings:
        for teaching in teachings:
            db.session.delete(teaching)
        db.session.commit()

    course = Course.query.get(id)
    if course is None:
        return result(400,'Course not found.'), 404

    db.session.delete(course)
    db.session.commit()

    return result(200,'Course deleted successfully.')

@app.route("/api/teacherInfo",methods=["GET"])
def getteacherInfo():
        Teachers = Teacher.query.all()
        items = []
        for teacher in Teachers:
            teacherno = teacher.workno
            teacher = teacher.__dict__
            del teacher['_sa_instance_state']
            #老师的基础信息

            # 获取老师教授的所有课程号和学期信息
            teaching_list = Teaching.query.filter(Teaching.workno == teacherno).all()
            course_semester = {teaching.id: teaching.semester for teaching in teaching_list}
            course_year = {teaching.id: teaching.year for teaching in teaching_list}

            # 根据课程号获取对应的课程信息
            courseIds = [teaching.id for teaching in teaching_list]
            courses = Course.query.filter(Course.id.in_(courseIds)).all()

            courses_dict = []
            if len(courses) > 0:
                for course in courses:
                    course_dict = filter_props(course)
                    if course.id in course_semester:
                        course_dict["semester"] = course_semester[course.id]
                        course_dict["year"] = course_year[course.id]
                    del course_dict['property']
                    courses_dict.append(course_dict)

            # 获取老师教授的所有科研号和排名、是否通讯作者信息
            publication_list = Publication.query.filter(Publication.workno == teacherno).all()
            paper_ranking = {publication.id: publication.ranking for publication in publication_list}
            paper_correspond = {publication.id: publication.corresponding for publication in publication_list}

            # 根据论文号获取对应的论文信息
            paperIds = [publication.id for publication in publication_list]
            papers = Paper.query.filter(Paper.id.in_(paperIds)).all()

            papers_dict = []
            if len(papers) > 0:
                for paper in papers:
                    paper_dict = filter_props_date(paper)
                    if paper.id in paper_ranking:
                        paper_dict["rank"] = paper_ranking[paper.id]
                    if paper.id in paper_correspond:
                        paper_dict["corressponding"] = paper_correspond[paper.id]
                    papers_dict.append(paper_dict)

            # 获取老师负责的所有项目号
            charge_list = Charge.query.filter(Charge.workno == teacherno and Charge.ranking == 1).all()
            project_fund = {charge.id: charge.fund for charge in charge_list}

            # 根据项目号获取对应的项目信息
            projectIds = [charge.id for charge in charge_list]
            projects = Project.query.filter(Project.id.in_(projectIds)).all()

            projects_dict = []
            if len(projects) > 0:
                for project in projects:
                    project_dict = filter_props_date(project)
                    if project.id in project_fund:
                        project_dict["fund"] = project_fund[project.id]
                    projects_dict.append(project_dict)

            #将该教师教授的课程信息添加到一个新属性courseInfo中
            teacher.update({'courseInfo':courses_dict})
            teacher.update({'paperInfo':papers_dict})
            teacher.update({'projectInfo':projects_dict})

            items.append(teacher)

        return result(200,'success',{'items':items,'total':len(items)})

@app.route("/api/teachers",methods=["GET"])
def getTeacherList():
    Teachers = Teacher.query.all()
    items = []
    for teacher in Teachers:
        teacher = filter_props(teacher)
        items.append(teacher)

    return result(200, 'success',{'items': items, 'total': len(items)})

@app.route("/api/papers",methods=["GET"])
def getPaperList():
    Papers = Paper.query.all()
    items = []
    for paper in Papers:
        temp = filter_props_date(paper)
        # paper的基础信息
        items.append(temp)

    return result(200, 'success',{'items': items, 'total': len(items)})

@app.route("/api/courses",methods=["GET"])
def getCourseList():
    Courses = Course.query.all()
    items = []
    for course in Courses:
        course = filter_props(course)
        # course的基础信息
        items.append(course)

    return result(200, 'success',{'items': items, 'total': len(items)})\

@app.route("/api/projects",methods=["GET"])
def getProjectList():
    Projects = Project.query.all()
    items = []
    for project in Projects:
        project = filter_props(project)
        # Project的基础信息
        items.append(project)

    return result(200, 'success',{'items': items, 'total': len(items)})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    workno = data['workno']
    name = data['name']
    teacher = Teacher.query.get(workno)
    teacher_dict = filter_props(teacher)
    trueName = teacher.name
    if teacher and str(name) == str(trueName) :
       return result(200, 'success',{'user': teacher_dict})
    else:
       return result(400, 'success',{})

if __name__ == "__main__":
    app.run(debug=True)


