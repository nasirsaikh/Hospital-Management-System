from database import db
from datetime import datetime


class MedicalRecord(db.Model):
    __tablename__ = "medical_records"

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey(
        "appointments.id"), nullable=False)

    visit_type = db.Column(db.String(100))
    tests_done = db.Column(db.Text)
    diagnosis = db.Column(db.Text)
    medicines = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    appointment = db.relationship(
        "Appointment", back_populates="medical_record")

    def to_dict(self):
        return {
            "id": self.id,
            "appointment_id": self.appointment_id,
            "visit_type": self.visit_type,
            "tests_done": self.tests_done,
            "diagnosis": self.diagnosis,
            "medicines": self.medicines,
            "prescription": self.prescription,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
