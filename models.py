#models.py
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from flask_login import UserMixin
Base = declarative_base()

class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="subscriptions")
    email = Column(String, nullable=False, unique=True)
    category = Column(String)
    location = Column(String)
    keyword = Column(String)


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)

    subscriptions = relationship("Subscription", back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"

    def get_id(self):
        return str(self.id)  # ✅ Explicitly return ID as string

class JobPost(Base):
    __tablename__ = 'job_posts'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    company = Column(String)
    category = Column(String)
    job_type = Column(String)
    location = Column(String)
    salary = Column(String)
    created_at = Column(DateTime)
    source = Column(String)
    hash = Column(String, unique=True)


#set up the engine and session
engine = create_engine('sqlite:///subscriptions.db', echo=True)
SessionLocal = sessionmaker(bind=engine)