from database import db


class Specialization(db.Model):
    __tablename__ = "specializations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(255), default="")

    doctors = db.relationship("DoctorProfile", back_populates="specialization")

    def __repr__(self):
        return f"<Specialization {self.name}>"
