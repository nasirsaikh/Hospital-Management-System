from flask_restful import Resource
from flask_jwt_extended import get_jwt, jwt_required
from database import get_db_session
from models import Appointment, MedicalRecord, DoctorProfile

def require_admin():
    return get_jwt().get("role", "").upper() == "ADMIN"

class AdminPatientHistoryAPI(Resource):
    @jwt_required()
    def get(self, patient_id):
        """Admin sees ALL medical records for a specific patient."""
        
        if not require_admin():
            return {"message": "Admin only"}, 403

        session = get_db_session()

        appts = (
            session.query(Appointment)
            .join(MedicalRecord, MedicalRecord.appointment_id == Appointment.id)
            .filter(Appointment.patient_id == patient_id)
            .order_by(Appointment.date.desc(), Appointment.time.desc())
            .all()
        )

        if not appts:
            return [], 200

        records = []
        for appt in appts:
            r = appt.medical_record
            doc = appt.doctor

            records.append({
                "id": r.id,
                "doctor": {
                    "id": doc.id,
                    "name": doc.full_name,
                    "specialization": doc.specialization.name if doc.specialization else None,
                },
                "date": appt.date.isoformat(),
                "time": appt.time.strftime("%H:%M"),
                "visit_type": r.visit_type,
                "tests": r.tests_done,
                "diagnosis": r.diagnosis,
                "medicines": r.medicines,
                "prescription": r.prescription,
                "notes": r.notes,
            })

        return records, 200
