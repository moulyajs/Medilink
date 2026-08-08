from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class Profile(Base):
    __tablename__ = "profiles"

    patient_id = Column(
        UUID(as_uuid=True),
        ForeignKey("patients.patient_id", ondelete="CASCADE"),
        primary_key=True,
    )

    name = Column(String(100), nullable=False)

    phone = Column(String(20), nullable=True)

    dob = Column(Date, nullable=True)

    gender = Column(String(20), nullable=True)

    blood_group = Column(String(10), nullable=True)

    address = Column(String(250), nullable=True)

    emergency_contact = Column(String(20), nullable=True)

    profile_image = Column(String(500), nullable=True)

    patient = relationship("Patient", back_populates="profile")