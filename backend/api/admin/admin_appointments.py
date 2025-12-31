from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime

from database import get_db_session
from models import (
    Appointment,
    AppointmentStatus,
    DoctorProfile,
    PatientProfile,
    MedicalRecord
)

def require_admin():
    return get_jwt().get("role", "").upper() == "ADMIN"

appt_parser = reqparse.RequestParser()
appt_parser.add_argument("doctor_id", type=int)
appt_parser.add_argument("patient_id", type=int)
appt_parser.add_argument("date")
appt_parser.add_argument("time")
appt_parser.add_argument("status")
appt_parser.add_argument("notes")

class AdminAppointments(Resource):

    @jwt_required()
    def get(self):
        if not require_admin():
            return {"message": "Admin only"}, 403

        session = get_db_session()

        appts = (
            session.query(Appointment)
            .order_by(Appointment.date.desc(), Appointment.time.desc())
            .all()
        )

        result = []
        for a in appts:
            record = a.medical_record

            result.append({
                "id": a.id,
                "date": a.date.isoformat(),
                "time": a.time.strftime("%H:%M"),
                "status": a.status.value,
                "notes": a.notes,
                "doctor": {
                    "id": a.doctor.id,
                    "name": a.doctor.full_name,
                    "specialization": (
                        a.doctor.specialization.name
                        if a.doctor.specialization else None
                    ),
                    "email": a.doctor.user.email if a.doctor.user else None
                } if a.doctor else None,
                "patient": {
                    "id": a.patient.id,
                    "name": a.patient.user.name if a.patient.user else None,
                    "email": a.patient.user.email if a.patient.user else None,
                    "age": a.patient.age,
                    "gender": a.patient.gender,
                    "phone": a.patient.phone
                } if a.patient else None,
                "record": {
                    "id": record.id if record else None,
                    "visit_type": record.visit_type if record else None,
                    "tests": record.tests_done if record else None,
                    "diagnosis": record.diagnosis if record else None,
                    "medicines": record.medicines if record else None,
                    "prescription": record.prescription if record else None,
                    "notes": record.notes if record else None,
                } if record else None
            })

        return result, 200

    @jwt_required()
    def post(self):
        if not require_admin():
            return {"message": "Admin only"}, 403

        session = get_db_session()
        data = appt_parser.parse_args()

        missing = [
            k for k in ["doctor_id", "patient_id", "date", "time"]
            if not data.get(k)
        ]
        if missing:
            return {"message": f"Missing fields: {', '.join(missing)}"}, 400

        doctor = session.query(DoctorProfile).get(data["doctor_id"])
        if not doctor:
            return {"message": "Doctor does not exist"}, 404

        patient = session.query(PatientProfile).get(data["patient_id"])
        if not patient:
            return {"message": "Patient does not exist"}, 404

        try:
            appt_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
            appt_time = datetime.strptime(data["time"], "%H:%M").time()
        except ValueError:
            return {"message": "Invalid date or time format"}, 400

        status = data["status"] or "PENDING"
        try:
            status_enum = AppointmentStatus(status.lower())
        except ValueError:
            return {"message": "Invalid status"}, 400

        appt = Appointment(
            doctor_id=doctor.id,
            patient_id=patient.id,
            date=appt_date,
            time=appt_time,
            status=status_enum,
            notes=data.get("notes")
        )

        session.add(appt)
        session.commit()

        return {"message": "Appointment created", "id": appt.id}, 201

class AdminAppointmentDetail(Resource):

    @jwt_required()
    def put(self, appt_id):
        if not require_admin():
            return {"message": "Admin only"}, 403

        session = get_db_session()
        data = appt_parser.parse_args()

        appt = session.query(Appointment).get(appt_id)
        if not appt:
            return {"message": "Appointment not found"}, 404

        if data["doctor_id"]:
            doctor = session.query(DoctorProfile).get(data["doctor_id"])
            if not doctor:
                return {"message": "Doctor does not exist"}, 404
            appt.doctor_id = doctor.id

        if data["patient_id"]:
            patient = session.query(PatientProfile).get(data["patient_id"])
            if not patient:
                return {"message": "Patient does not exist"}, 404
            appt.patient_id = patient.id

        if data["date"]:
            try:
                appt.date = datetime.strptime(data["date"], "%Y-%m-%d").date()
            except ValueError:
                return {"message": "Invalid date"}, 400

        if data["time"]:
            try:
                appt.time = datetime.strptime(data["time"], "%H:%M").time()
            except ValueError:
                return {"message": "Invalid time"}, 400

        if data["status"]:
            try:
                appt.status = AppointmentStatus(data["status"].lower())
            except ValueError:
                return {"message": "Invalid status"}, 400

        if data["notes"] is not None:
            appt.notes = data["notes"]

        session.commit()
        return {"message": "Appointment updated"}, 200

    @jwt_required()
    def delete(self, appt_id):
        if not require_admin():
            return {"message": "Admin only"}, 403

        session = get_db_session()
        appt = session.query(Appointment).get(appt_id)

        if not appt:
            return {"message": "Appointment not found"}, 404

        session.delete(appt)
        session.commit()

        return {"message": "Appointment deleted"}, 200

class AdminAppointmentStatus(Resource):

    @jwt_required()
    def put(self, appt_id):
        if not require_admin():
            return {"message": "Admin only"}, 403

        session = get_db_session()
        data = reqparse.RequestParser()
        data.add_argument("status", required=True)
        args = data.parse_args()

        appt = session.query(Appointment).get(appt_id)
        if not appt:
            return {"message": "Appointment not found"}, 404

        try:
            appt.status = AppointmentStatus(args["status"].lower())
        except ValueError:
            return {"message": "Invalid status"}, 400

        session.commit()

        return {"message": "Status updated successfully"}, 200
