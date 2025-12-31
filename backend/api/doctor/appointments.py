from flask_restful import Resource
from flask import request
from flask_jwt_extended import get_jwt_identity
from datetime import datetime, date

from database import get_db_session
from models import DoctorProfile, Appointment, AppointmentStatus, PatientProfile, MedicalRecord
from utils.auth import role_required

class DoctorAppointments(Resource):

    @role_required("doctor")
    def get(self):
        """
        Optional query params:
        - status: pending / confirmed / completed / cancelled
        - date_from: YYYY-MM-DD
        - date_to: YYYY-MM-DD
        """
        session = get_db_session()
        user_id = int(get_jwt_identity())

        doctor = session.query(DoctorProfile).filter_by(user_id=user_id).first()
        if not doctor:
            return {"message": "Doctor profile not found"}, 404

        q = session.query(Appointment).filter(Appointment.doctor_id == doctor.id)

        status = request.args.get("status")
        if status:
            try:
                st = AppointmentStatus(status.lower())
            except ValueError:
                return {"message": "Invalid status"}, 400
            q = q.filter(Appointment.status == st)

        df = request.args.get("date_from")
        dt = request.args.get("date_to")

        if df:
            try:
                df_val = datetime.strptime(df, "%Y-%m-%d").date()
                q = q.filter(Appointment.date >= df_val)
            except ValueError:
                return {"message": "Invalid date_from"}, 400

        if dt:
            try:
                dt_val = datetime.strptime(dt, "%Y-%m-%d").date()
                q = q.filter(Appointment.date <= dt_val)
            except ValueError:
                return {"message": "Invalid date_to"}, 400

        q = q.order_by(Appointment.date.asc(), Appointment.time.asc())
        appointments = q.all()

        result = []
        for a in appointments:
            patient = session.query(PatientProfile).get(a.patient_id)
            result.append({
                "id": a.id,
                "date": a.date.isoformat(),
                "time": a.time.strftime("%H:%M"),
                "status": a.status.value,
                "notes": a.notes,
                "patient": {
                    "id": patient.id if patient else None,
                    "name": patient.user.name if patient and patient.user else None,
                    "age": patient.age if patient else None,
                    "gender": patient.gender if patient else None,
                    "phone": patient.phone if patient else "Not Available",
                }
            })

        return result, 200


class DoctorAppointmentDetail(Resource):

    @role_required("doctor")
    def get(self, appointment_id):
        session = get_db_session()
        user_id = int(get_jwt_identity())

        doctor = session.query(DoctorProfile).filter_by(user_id=user_id).first()
        if not doctor:
            return {"message": "Doctor profile not found"}, 404

        a = session.query(Appointment).get(appointment_id)
        if not a or a.doctor_id != doctor.id:
            return {"message": "Appointment not found"}, 404

        patient = session.query(PatientProfile).get(a.patient_id)

        return {
            "id": a.id,
            "date": a.date.isoformat(),
            "time": a.time.strftime("%H:%M"),
            "status": a.status.value,
            "notes": a.notes,
            "patient": {
                "id": patient.id if patient else None,
                "name": patient.user.name if patient and patient.user else None,
                "age": patient.age if patient else None,
                "gender": patient.gender if patient else None,
                "phone": patient.phone if patient else "Not Available",
            }
        }, 200

    @role_required("doctor")
    def put(self, appointment_id):
        """
        Doctor can update:
        - status (confirmed | completed | cancelled)
        - notes
        """
        session = get_db_session()
        user_id = int(get_jwt_identity())

        doctor = session.query(DoctorProfile).filter_by(user_id=user_id).first()
        if not doctor:
            return {"message": "Doctor profile not found"}, 404

        a = session.query(Appointment).get(appointment_id)
        if not a or a.doctor_id != doctor.id:
            return {"message": "Appointment not found"}, 404

        data = request.json or {}

        if "status" in data:
            new_status = data["status"].lower()

            if new_status not in ["pending", "confirmed", "completed", "cancelled"]:
                return {"message": "Invalid status"}, 400

            if a.status == AppointmentStatus.CANCELLED:
                return {"message": "Cannot update a cancelled appointment"}, 400

            if a.status == AppointmentStatus.COMPLETED:
                return {"message": "Appointment is already completed"}, 400

            if new_status == "completed":
                record = (
                    session.query(MedicalRecord)
                    .filter_by(appointment_id=appointment_id)
                    .first()
                )

            a.status = AppointmentStatus(new_status)

        if "notes" in data:
            a.notes = data["notes"]

        session.commit()

        return {"message": "Appointment updated"}, 200
