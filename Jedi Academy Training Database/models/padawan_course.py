import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db

class PadawanCourses(db.Model):
    __tablename__ = "PadawanCourses"
    
    padawan_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Users.user_id'), primary_key=True)
    course_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Courses.course_id'), primary_key=True)
    enrollment_date = db.Column(db.DateTime(), nullable=True)
    completion_date = db.Column(db.DateTime(), nullable=True)
    final_score = db.Column(db.Float(), nullable=True)

    padawan = db.relationship('Users', backref='enrolled_courses')
    course = db.relationship('Courses', back_populates='padawans')

    def __init__(self, padawan_id, course_id, enrollment_date=None, completion_date=None, final_score=None):
        self.padawan_id = padawan_id
        self.course_id = course_id
        self.enrollment_date = enrollment_date 
        self.completion_date = completion_date
        self.final_score = final_score

    def new_padawan_course_obj():
        return PadawanCourses('', '', None, None, None)

class PadawanCoursesSchema(ma.Schema):
    class Meta:
        fields = ['padawan_id', 'course_id', 'enrollment_date', 'completion_date', 'final_score', 'padawan', 'course']

    padawan_id = ma.fields.UUID(required=True)
    course_id = ma.fields.UUID(required=True)
    enrollment_date = ma.fields.DateTime(allow_none=True)
    completion_date = ma.fields.DateTime(allow_none=True)
    final_score = ma.fields.Float(allow_none=True)
    padawan = ma.fields.Nested('UsersSchema', exclude=['enrolled_courses'])
    course = ma.fields.Nested('CoursesSchema', exclude=['padawans'])

padawan_course_schema = PadawanCoursesSchema()
padawan_courses_schema = PadawanCoursesSchema(many=True)