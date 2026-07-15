from sqlalchemy import Column, Integer, String

from database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(String(120), unique=True, nullable=False)

    phone = Column(String(20), nullable=False)

    gender = Column(String(20), nullable=False)

    blood_group = Column(String(10), nullable=False)

    dob = Column(String(30), nullable=True)

    address = Column(String(250), nullable=True)

    emergency_contact = Column(String(20), nullable=True)

    profile_image = Column(String(500), nullable=True)