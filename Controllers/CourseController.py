__author__ = 'milad'
from flask_restful import Resource

from Controllers.LoginController import auth2
from Models.Model import GroupCourse


class List(Resource):
    @auth2.login_required
    def get(self):
        groupcourses = GroupCourse.select()
        ls = [
            dict(
                id=groupcourse.id,
                group_number=groupcourse.group_number,
                semester=groupcourse.semester,
                guest_semester=groupcourse.guest_semester,
                date_exam=groupcourse.date_exam,
                time_exam=groupcourse.time_exam,
                term=groupcourse.term,
                capacity=groupcourse.capacity,
                min_capacity=groupcourse.min_capacity,
                Course_id=dict(
                    id=groupcourse.Course_id.id,
                    presentation=groupcourse.Course_id.presentation,
                    type=groupcourse.Course_id.type,
                    status_prerequisite=groupcourse.Course_id.status_prerequisite,
                    name=groupcourse.Course_id.name,
                    unit_number=groupcourse.Course_id.unit_number,
                    price=groupcourse.Course_id.price,
                    list_prerequisite=groupcourse.Course_id.list_prerequisite,
                ),
                professor_id=dict(
                    firstname=groupcourse.professor_id.firstname,
                    lastname=groupcourse.professor_id.lastname,
                ),
                Time_Course_id=dict(
                    id=groupcourse.Time_Course_id.id,
                    days=groupcourse.Time_Course_id.days,
                    time=groupcourse.Time_Course_id.time,
                    classes=groupcourse.Time_Course_id.classes,
                    rotatory=groupcourse.Time_Course_id.rotatory,
                    day_rotatory=groupcourse.Time_Course_id.day_rotatory,
                )
            ) for groupcourse in groupcourses
        ]
        return dict(courses=ls)
