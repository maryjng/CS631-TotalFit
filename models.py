from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKeyConstraint
from datetime import datetime
from sqlalchemy.exc import IntegrityError, InternalError
from custom_exceptions import MemberAlreadyRegisteredError 

db = SQLAlchemy()

class Member(db.Model):
    __tablename__ = "Member"

    member_id = db.Column(db.Integer, primary_key=True)
    member_name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    registration_date = db.Column(db.DateTime)
    membership_type = db.Column(db.ForeignKey("Membership.membership_type", onupdate="CASCADE", ondelete="CASCADE"))

    @classmethod
    def signup(cls, member_name, address, membership_type):
        new_member = Member(member_name=member_name, address=address, membership_type=membership_type, registration_date=datetime.now())

        db.session.add(new_member)
        return new_member
    
class Membership(db.Model):
    __tablename__ = "Membership"

    membership_type = db.Column(db.String(50), primary_key=True)
    fee = db.Column(db.Numeric(10, 2))

class Exercise(db.Model):
    __tablename__ = "Exercise"

    exercise_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    exercise_type = db.Column(db.String(50))
    descriptor = db.Column(db.String(255))

class Room(db.Model):
    __tablename__ = "Room"

    building = db.Column(db.String(255), primary_key=True)
    room_number = db.Column(db.String(50), primary_key=True)

class Instructor(db.Model):
    __tablename__ = "Instructor"

    instructor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    employment_type = db.Column(db.String(50))

class ExternalInstructor(db.Model):
    __tablename__ = "External_Instructor"

    instructor_id = db.Column(db.ForeignKey("Instructor.instructor_id"), primary_key=True)
    name = db.Column(db.String(255))
    wage = db.Column(db.Numeric(10, 2))
    hours = db.Column(db.Integer)
    instructor = db.relationship('Instructor', backref='external_instructors', uselist=False)

class InternalInstructor(db.Model):
    __tablename__ = "Internal_Instructor"

    instructor_id = db.Column(db.ForeignKey("Instructor.instructor_id"), primary_key=True)
    name = db.Column(db.String(255))
    salary = db.Column(db.Integer)
    instructor = db.relationship('Instructor', backref='internal_instructors', uselist=False)

class ExerciseClass(db.Model):
    __tablename__ = "Class"

    class_id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.Text)
    building = db.Column(db.Text)
    instructor_id = db.Column(db.ForeignKey("Instructor.instructor_id"))
    start_time = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    max_members = db.Column(db.Integer)

    __table_args__ = (
        ForeignKeyConstraint(['building', 'room_number'], ['Room.building', 'Room.room_number']),
    )

    # Define the relationships
    room = db.relationship('Room', backref='classes', uselist=False)
    instructor = db.relationship('Instructor', backref='classes', uselist=False)

class MemberClass(db.Model):
    __tablename__ = "member_class"

    member_id = db.Column(db.Integer, db.ForeignKey("Member.member_id"), primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey("Class.class_id"), primary_key=True)
    registration_date = db.Column(db.DateTime)

    
    @classmethod
    def register_member(cls, class_id, member_id):
        """Registers a member to a class."""

        try:
            check_register = db.session.query(MemberClass).filter_by(member_id=member_id, class_id=class_id).first()

            if check_register:
                raise MemberAlreadyRegisteredError()
            else:
                member_class = MemberClass(member_id=member_id, class_id=class_id, registration_date=datetime.now())
                db.session.add(member_class)
                db.session.commit()
                return member_class
        except IntegrityError as e:
            raise e
        except InternalError as e:
            raise e

def connect_db(app):
    db.app = app
    db.init_app(app)