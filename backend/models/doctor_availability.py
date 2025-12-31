from database import db
from datetime import date, time


class DoctorAvailability(db.Model):
    __tablename__ = "doctor_daily_availability"

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey(
        "doctor_profiles.id"), nullable=False)

    date = db.Column(db.Date, nullable=False)

    slot_type = db.Column(db.String(20), nullable=False)

    is_available = db.Column(db.Boolean, default=False)

    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)

    doctor = db.relationship("DoctorProfile", back_populates="availability")

    def __repr__(self):
        return f"<DailyAvailability {self.date} {self.slot_type}>"
