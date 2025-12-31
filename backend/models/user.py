from database import db
from enum import Enum


class UserRole(Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    PATIENT = "patient"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    role = db.Column(db.Enum(UserRole), nullable=False)

    patient_profile = db.relationship(
        "PatientProfile", backref="user", uselist=False)
    doctor_profile = db.relationship(
        "DoctorProfile", backref="user", uselist=False)

    def __repr__(self):
        return f"<User {self.email}>"
