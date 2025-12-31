from flask_restful import Resource
from flask import request
from utils.auth import role_required
from flask_jwt_extended import get_jwt_identity

from models import Appointment, MedicalRecord, PatientProfile, DoctorProfile
from database import get_db_session


class DoctorMedicalRecordAPI(Resource):

    @role_required("doctor")
    def post(self):
        session = get_db_session()
        user_id = int(get_jwt_identity())

        doctor = session.query(DoctorProfile).filter_by(user_id=user_id).first()
        if not doctor:
            return {"message": "Doctor profile missing"}, 404

        data = request.json or {}
        appointment_id = data.get("appointment_id")

        if not appointment_id:
            return {"message": "appointment_id is required"}, 400

        appointment = session.query(Appointment).get(appointment_id)
        if not appointment or appointment.doctor_id != doctor.id:
            return {"message": "Appointment not found"}, 404

        record = appointment.medical_record
        is_new = False

        if not record:
            record = MedicalRecord(appointment_id=appointment.id)
            is_new = True

        record.visit_type = data.get("visit_type")
        record.tests_done = data.get("tests")
        record.diagnosis = data.get("diagnosis")
        record.medicines = data.get("medicines")
        record.prescription = data.get("prescription")
        record.notes = data.get("notes")

        session.add(record)
        session.commit()

        return {
            "message": "Record created" if is_new else "Record updated",
            "record": record.to_dict(),
        }, 201 if is_new else 200

    @role_required("doctor")
    def get(self, appointment_id):
        session = get_db_session()
        user_id = int(get_jwt_identity())

        doctor = session.query(DoctorProfile).filter_by(user_id=user_id).first()

        appt = (
            session.query(Appointment)
            .filter_by(id=appointment_id, doctor_id=doctor.id)
            .first()
        )

        if not appt:
            return {"message": "Appointment not found"}, 404

        if not appt.medical_record:
            return {"message": "No record available"}, 404

        return appt.medical_record.to_dict(), 200
