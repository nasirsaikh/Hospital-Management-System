from database import db


class PatientProfile(db.Model):
    __tablename__ = "patient_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id"), unique=True, nullable=False)

    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    appointments = db.relationship("Appointment", back_populates="patient")
