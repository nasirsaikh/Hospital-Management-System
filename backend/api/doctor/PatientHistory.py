from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from utils.auth import role_required
from models import Appointment, MedicalRecord, DoctorProfile
from database import get_db_session

class DoctorPatientHistoryAPI(Resource):

    @role_required("doctor")
    def get(self, patient_id):
        """
        Fetch ALL medical records for a specific patient,
        but only those belonging to THIS doctor.
        """
        session = get_db_session()
        user_id = int(get_jwt_identity())

        doctor = session.query(DoctorProfile).filter_by(user_id=user_id).first()
        if not doctor:
            return {"message": "Doctor profile missing"}, 404

        appts = (
            session.query(Appointment)
            .join(MedicalRecord, MedicalRecord.appointment_id == Appointment.id)
            .filter(
                Appointment.patient_id == patient_id,
                Appointment.doctor_id == doctor.id
            )
            .order_by(Appointment.date.desc(), Appointment.time.desc())
            .all()
        )

        if not appts:
            return [], 200

        records = []
        for appt in appts:
            r = appt.medical_record

            records.append({
                "id": r.id,
                "doctor": {
                    "name": doctor.full_name,
                    "specialization": doctor.specialization.name,
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
