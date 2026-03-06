from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

DATABASE_URL = "sqlite:///virtual_clerk.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Lawyer(Base):
    __tablename__ = "lawyers"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)

class Advocate(Base):
    __tablename__ = "advocates"

    id = Column(Integer, primary_key=True)
    lawyer_id = Column(Integer)
    advocate_name = Column(String)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    case_no = Column(String)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(engine)
