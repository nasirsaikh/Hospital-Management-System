from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from datetime import date

from database import get_db_session
from models import DoctorProfile, Appointment, PatientProfile
from utils.auth import role_required

class DoctorPatients(Resource):

    @role_required("doctor")
    def get(self):
        session = get_db_session()
        user_id = int(get_jwt_identity())

        doctor = session.query(DoctorProfile).filter_by(user_id=user_id).first()
        if not doctor:
            return {"message": "Doctor profile not found"}, 404

        patient_ids = (
            session.query(Appointment.patient_id)
            .filter(Appointment.doctor_id == doctor.id)
            .distinct()
            .all()
        )
        patient_ids = [pid for (pid,) in patient_ids]

        if not patient_ids:
            return [], 200

        patients = (
            session.query(PatientProfile)
            .filter(PatientProfile.id.in_(patient_ids))
            .all()
        )

        last_visits = {
            pid: session.query(Appointment)
                .filter(Appointment.doctor_id == doctor.id, Appointment.patient_id == pid)
                .order_by(Appointment.date.desc(), Appointment.time.desc())
                .first()
            for pid in patient_ids
        }

        result = []
        for p in patients:
            lv = last_visits.get(p.id)
            result.append({
                "id": p.id,
                "name": p.user.name if p.user else None,
                "email": p.user.email if p.user else None,
                "age": p.age,
                "gender": p.gender,
                "phone": p.phone,
                "last_visit_date": lv.date.isoformat() if lv else None,
            })

        return result, 200
