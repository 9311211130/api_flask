from Controllers import LoginController, CourseController, ChoiceCourseController, ScheduleController

__author__ = 'milad'
from flask import Flask
from flask_restful import Api


app = Flask(__name__)


api = Api(app)

api.add_resource(LoginController.Login, '/login')
api.add_resource(CourseController.List, '/courses')
api.add_resource(ChoiceCourseController.List, '/choicecourses', endpoint='choicecourselist')
api.add_resource(ChoiceCourseController.Store, '/choicecourse')
api.add_resource(ChoiceCourseController.Destroy, '/choicecourses/<int:choice_course_id>')
api.add_resource(ScheduleController.List, '/schedule', endpoint='schedule')

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, True)
