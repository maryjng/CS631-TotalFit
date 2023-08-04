from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import sessionmaker, relationship, declarative_base


# Step 1: Import the necessary modules

# Step 2: Establish a database connection
# Replace 'your_database_url' with the URL of your database
database_url = "postgresql://postgres:kitty@localhost:5432/totalfit1"
engine = create_engine(database_url)
#will return engine instance
Base = declarative_base()

# Step 3: Define your data model

class Member(Base):
    __tablename__ = "Member"

    member_id = Column(Integer, primary_key=True)
    member_name = Column(String(255))
    address = Column(String(255))
    registration_date = Column(DateTime)
    membership_type = Column(String(50))
    membership = relationship('Membership', backref='memberships', uselist=False)
    
class Membership(Base):
    __tablename__ = "Membership"

    membership_type = Column(String(50), primary_key=True)
    fee = Column(Numeric(10, 2))

class Exercise(Base):
    __tablename__ = "Exercise"

    exercise_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    exercise_type = Column(String(50))
    descriptor = Column(String(255))

class Room(Base):
    __tablename__ = "Room"

    building = Column(String(255), primary_key=True)
    room_number = Column(String(50), primary_key=True)

class Instructor(Base):
    __tablename__ = "Instructor"

    instructor_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    employment_type = Column(String(50))

class ExternalInstructor(Base):
    __tablename__ = "External_Instructor"

    instructor_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    wage = Column(Numeric(10, 2))
    hours = Column(Integer)
    instructor = relationship('Instructor', backref='external_instructors', uselist=False)

class InternalInstructor(Base):
    __tablename__ = "Internal_Instructor"

    instructor_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    salary = Column(Integer)
    instructor = relationship('Instructor', backref='internal_instructors', uselist=False)

class ExerciseClass(Base):
    __tablename__ = "Class"

    class_id = Column(Integer, primary_key=True)
    room_number = Column(String(255))
    building = Column(String(255))
    instructor_id = Column(Integer)
    start_time = Column(DateTime)
    duration = Column(Integer)
    max_members = Column(Integer)
    room = relationship('Room', backref='classes', uselist=False)
    instructor = relationship('Instructor', backref='classes', uselist=False)

class MemberClass(Base):
    __tablename__ = "Member_Class"

    member_id = Column(Integer, ForeignKey("Member.member_id"), primary_key=True)
    class_id = Column(Integer, ForeignKey("Class.class_id"), primary_key=True)
    registration_date = Column(DateTime)


# Step 4: Create the database tables
Base.metadata.create_all(engine)

# # Step 5: Insert data into the database
# Session = sessionmaker(bind=engine)
# session = Session()

# # Example: Inserting a new user into the database
# new_user = User(username='Sandy', email='sandy@gmail.com', password='cool-password')
# session.add(new_user)
# session.commit()

# # Step 6: Query data from the database
# # Example: Querying all users from the database
# all_users = session.query(User).all()

# # Example: Querying a specific user by their username
# user = session.query(User).filter_by(username='Sandy').first()

# # Step 7: Close the session
# session.close()