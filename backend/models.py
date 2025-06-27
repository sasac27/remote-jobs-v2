from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey, create_engine, DateTime, Text
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from flask_login import UserMixin

Base = declarative_base()

# --------------------------
# Subscription Table
# --------------------------
class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="subscriptions")

    email = Column(String, nullable=False, unique=True)
    category = Column(String)
    location = Column(String)
    keyword = Column(String)

# --------------------------
# User Table
# --------------------------
class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)

    subscriptions = relationship("Subscription", back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"

    def get_id(self):
        return str(self.id)  # Explicitly return ID as string for Flask-Login

# --------------------------
# JobPost Table
# --------------------------
class JobPost(Base):
    __tablename__ = 'job_posts'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    category = Column(String, index=True)
    job_type = Column(String)
    location = Column(String, index=True)
    url = Column(String)
    tags = Column(ARRAY(String), default=list)  # safer than default=[]
    salary = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    source = Column(String)
    hash = Column(String, unique=True, nullable=False, index=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "salary": self.salary,
            "category": self.category,
            "job_type": self.job_type,
            "created": self.created_at.isoformat(),
            "source": self.source,
            "tags": self.tags,
            "url": self.url
        }


# --------------------------
# DB Engine and Session
# --------------------------
engine = create_engine('postgresql://jobuser:2600@localhost/jobsdb')
SessionLocal = sessionmaker(bind=engine)
