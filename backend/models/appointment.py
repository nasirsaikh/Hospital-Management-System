from database import db
import enum
from datetime import datetime


class AppointmentStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(db.Integer, db.ForeignKey(
        "patient_profiles.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey(
        "doctor_profiles.id"), nullable=False)

    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    status = db.Column(db.Enum(AppointmentStatus),
                       default=AppointmentStatus.PENDING)

    notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    patient = db.relationship("PatientProfile", back_populates="appointments")
    doctor = db.relationship("DoctorProfile", back_populates="appointments")
    medical_record = db.relationship(
        "MedicalRecord",
        uselist=False,
        back_populates="appointment",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Appointment {self.id} {self.date} {self.time}>"
