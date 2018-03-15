__author__ = 'milad'
from flask import request, g
from flask_restful import Resource

from Controllers.LoginController import auth2
from Models.Model import ChoiceCourse


class List(Resource):
    @auth2.login_required
    def get(self):
        choice_courses = ChoiceCourse.select().where(ChoiceCourse.Student_student_number_id == g.user.student_number)
        ls = [
            dict(
                id=choice_course.id,
                Student_student_number=choice_course.Student_student_number_id.student_number,
                status=choice_course.status,
                status_pay=choice_course.status_pay,
                score=choice_course.score,
                semeter=choice_course.semeter,
                Group_Course_code_course_id=[dict(
                    id=choice_course.Group_Course_code_course_id.id,
                    group_number=choice_course.Group_Course_code_course_id.group_number,
                    semester=choice_course.Group_Course_code_course_id.semester,
                    guest_semester=choice_course.Group_Course_code_course_id.guest_semester,
                    date_exam=choice_course.Group_Course_code_course_id.date_exam,
                    time_exam=choice_course.Group_Course_code_course_id.time_exam,
                    term=choice_course.Group_Course_code_course_id.term,
                    capacity=choice_course.Group_Course_code_course_id.capacity,
                    min_capacity=choice_course.Group_Course_code_course_id.min_capacity,
                    Course_id=[dict(
                        id=choice_course.Group_Course_code_course_id.Course_id.id,
                        presentation=choice_course.Group_Course_code_course_id.Course_id.presentation,
                        type=choice_course.Group_Course_code_course_id.Course_id.type,
                        status_prerequisite=choice_course.Group_Course_code_course_id.Course_id.status_prerequisite,
                        name=choice_course.Group_Course_code_course_id.Course_id.name,
                        unit_number=choice_course.Group_Course_code_course_id.Course_id.unit_number,
                        price=choice_course.Group_Course_code_course_id.Course_id.price,
                        list_prerequisite=choice_course.Group_Course_code_course_id.Course_id.list_prerequisite,
                    )],
                    professor_id=[dict(
                        id=choice_course.Group_Course_code_course_id.professor_id.id,
                        firstname=choice_course.Group_Course_code_course_id.professor_id.firstname,
                        lastname=choice_course.Group_Course_code_course_id.professor_id.lastname,
                        # father=choice_course.Group_Course_code_course_id.professor_id.father,
                        # sex=choice_course.Group_Course_code_course_id.professor_id.sex,
                        # national_code=choice_course.Group_Course_code_course_id.professor_id.national_code,
                        # birthday=choice_course.Group_Course_code_course_id.professor_id.birthday,
                        # location_brith=choice_course.Group_Course_code_course_id.professor_id.location_brith,
                        # phone=choice_course.Group_Course_code_course_id.professor_id.phone,
                        # mobile=choice_course.Group_Course_code_course_id.professor_id.mobile,
                        # password=choice_course.Group_Course_code_course_id.professor_id.password,
                        # address=choice_course.Group_Course_code_course_id.professor_id.address,
                        # img=choice_course.Group_Course_code_course_id.professor_id.img,
                    )],
                    Time_Course_id=[dict(
                        id=choice_course.Group_Course_code_course_id.Time_Course_id.id,
                        days=choice_course.Group_Course_code_course_id.Time_Course_id.days,
                        time=choice_course.Group_Course_code_course_id.Time_Course_id.time,
                        classes=choice_course.Group_Course_code_course_id.Time_Course_id.classes,
                        rotatory=choice_course.Group_Course_code_course_id.Time_Course_id.rotatory,
                        day_rotatory=choice_course.Group_Course_code_course_id.Time_Course_id.day_rotatory,
                    )]
                )],
            ) for choice_course in choice_courses
        ]
        return dict(courses=ls)


class Store(Resource):
    @auth2.login_required
    def post(self):
        request_json = request.get_json()
        choice_course = ChoiceCourse()
        # choicecourse.id = request_json['id']
        choice_course.Student_student_number_id = request_json['Student_student_number_id']
        choice_course.status = request_json['status']
        choice_course.status_pay = request_json['status_pay']
        choice_course.score = request_json['score']
        choice_course.semeter = request_json['semeter']
        choice_course.Group_Course_code_course_id = request_json['Group_Course_code_course_id']

        return dict(
            status=choice_course.save()
        )


class Destroy(Resource):
    @auth2.login_required
    def delete(self, choice_course_id):
        try:
            choice_course = ChoiceCourse.get(id=choice_course_id)
        except ChoiceCourse.DoesNotExist:
            return None, 404
        choice_course.delete_instance()
        return dict(status=True, id=choice_course_id), 200
