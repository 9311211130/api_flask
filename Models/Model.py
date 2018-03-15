from passlib.handlers.bcrypt import bcrypt

__author__ = 'milad'
from peewee import Model, MySQLDatabase, Field, SQL, PrimaryKeyField, IntegerField, CharField, TextField, \
    ForeignKeyField, FloatField
import env
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
mysql_db = MySQLDatabase('qurandb', user='root', password='',
                         host='127.0.0.1', port=3306)


class BaseModel(Model):
    class Meta:
        database = mysql_db


class EnumField(Field):
    db_field = "enum"

    def pre_field_create(self, model):
        field = "e_%s" % self.name

        self.get_database().get_conn().cursor().execute(
            "DROP TYPE IF EXISTS %s;" % field
        )

        query = self.get_database().get_conn().cursor()

        tail = ', '.join(["'%s'"] * len(self.choices)) % tuple(self.choices)
        q = "CREATE TYPE %s AS ENUM (%s);" % (field, tail)
        query.execute(q)

    def post_field_create(self, model):
        self.db_field = "e_%s" % self.name

    def coerce(self, value):
        if value not in self.choices:
            raise Exception("Invalid Enum Value `%s`", value)
        return str(value)

    def get_column_type(self):
        return "enum"

    def __ddl_column__(self, ctype):
        return SQL("e_%s" % self.name)


class TimeCourse(BaseModel):
    id = PrimaryKeyField()
    days = IntegerField(30)
    time = IntegerField(30)
    classes = IntegerField(30)
    rotatory = EnumField(choices=['1', '2'])
    day_rotatory = EnumField(choices=['zoj', 'fard'])

    class Meta:
        db_table = "time_course"


class Professor(BaseModel):
    id = PrimaryKeyField()
    firstname = CharField(45)
    lastname = CharField(45)
    father = CharField(45)
    sex = EnumField(choices=["male", "female"])
    national_code = CharField(unique=True)
    birthday = CharField(45)
    location_brith = CharField(45)
    phone = CharField(45)
    mobile = CharField(45)
    password = TextField()
    address = TextField()
    img = CharField(45)

    class Meta:
        db_table = "professor"


class Course(BaseModel):
    id = PrimaryKeyField()
    presentation = EnumField(choices=["practical", "theoretic"])
    type = EnumField(choices=["professional", "basic", "prime", "public"])
    status_prerequisite = EnumField(choices=["yes", "no"])
    name = CharField(30)
    unit_number = IntegerField(30)
    price = IntegerField(30)
    list_prerequisite = CharField()

    class Meta:
        db_table = "course"


class GroupCourse(BaseModel):
    id = PrimaryKeyField()
    group_number = CharField(45)
    semester = CharField(45)
    guest_semester = CharField(45)
    date_exam = CharField(45)
    time_exam = CharField(45)
    term = CharField(45)
    capacity = IntegerField(11)
    min_capacity = IntegerField(11)
    Course_id = ForeignKeyField(Course, backref='group_course')
    professor_id = ForeignKeyField(Professor, backref='group_course')
    Time_Course_id = ForeignKeyField(TimeCourse, backref='group_course')

    class Meta:
        db_table = "group_course"


class Student(BaseModel):
    firstname = CharField()
    lastname = CharField()
    father = CharField(default='test')
    brithday = CharField(default='test')
    location_brith = CharField(default='test')
    phone = CharField(default='test')
    mobile = CharField(default='test')
    national_code = CharField(default='1234')
    status = EnumField(choices=['active', 'non_active', 'expulsion', 'alumnus'])
    entry_semester = CharField(default='2')
    img = CharField(default='test')
    address = TextField(default='test')
    student_number = PrimaryKeyField(unique=True)
    id = CharField(11)
    password = CharField(100)

    class Meta:
        db_table = "student"
        order_by = ('student_number',)

    def hash_password(self, password):
        self.password = bcrypt.hash(password)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(env.secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(env.secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        try:
            user = Student.get(Student.id == data['id'])
            return user
        except:
            return None


class ChoiceCourse(BaseModel):
    id = PrimaryKeyField()
    Student_student_number_id = ForeignKeyField(Student, backref='choice_course')
    status = EnumField(choices=["accept", "non_accept"])
    status_pay = EnumField(choices=["yes", "on"])
    score = FloatField()
    semeter = CharField(45)
    Group_Course_code_course_id = ForeignKeyField(GroupCourse, backref='choice_course')

    class Meta:
        db_table = "choice_course"
