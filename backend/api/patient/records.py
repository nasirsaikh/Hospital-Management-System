from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from utils.auth import role_required
from models import Appointment, MedicalRecord, PatientProfile
from database import get_db_session


class PatientMedicalRecordsAPI(Resource):

    @role_required("patient")
    def get(self):
        session = get_db_session()
        user_id = int(get_jwt_identity())

        patient = session.query(PatientProfile).filter_by(
            user_id=user_id).first()

        appointments = (
            session.query(Appointment)
            .filter_by(patient_id=patient.id)
            .all()
        )

        records = []
        for a in appointments:
            if a.medical_record:
                r = a.medical_record.to_dict()
                r["doctor"] = {
                    "id": a.doctor.id,
                    "name": a.doctor.full_name,
                    "specialization": a.doctor.specialization.name if a.doctor.specialization else None
                }
                r["date"] = a.date.isoformat()
                records.append(r)

        return records, 200
