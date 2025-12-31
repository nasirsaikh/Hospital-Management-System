

from flask_restful import Resource
from datetime import date
from flask_jwt_extended import get_jwt_identity

from database import get_db_session

from models import (
    PatientProfile,
    Appointment,
    AppointmentStatus,
    MedicalRecord,
    DoctorProfile
)

from utils.auth import role_required


class PatientDashboard(Resource):

    @role_required("patient")
    def get(self):
        session = get_db_session()

        user_id = int(get_jwt_identity())

        patient = session.query(PatientProfile).filter_by(
            user_id=user_id).first()
        if not patient:
            return {"message": "Patient profile not found"}, 404

        total_appointments = (
            session.query(Appointment)
            .filter(Appointment.patient_id == patient.id)
            .count()
        )

        completed_appointments = (
            session.query(Appointment)
            .filter(Appointment.patient_id == patient.id)
            .filter(Appointment.status == AppointmentStatus.COMPLETED)
            .count()
        )

        upcoming_count = (
            session.query(Appointment)
            .filter(Appointment.patient_id == patient.id)
            .filter(Appointment.date >= date.today())
            .filter(Appointment.status != AppointmentStatus.CANCELLED)
            .filter(Appointment.status != AppointmentStatus.COMPLETED)
            .count()
        )

        upcoming_appt = (
            session.query(Appointment)
            .filter(Appointment.patient_id == patient.id)
            .filter(Appointment.date >= date.today())
            .filter(Appointment.status != AppointmentStatus.CANCELLED)
            .filter(Appointment.status != AppointmentStatus.COMPLETED)
            .order_by(Appointment.date.asc(), Appointment.time.asc())
            .first()
        )

        upcoming_data = None
        if upcoming_appt:
            doctor = session.query(DoctorProfile).get(upcoming_appt.doctor_id)

            upcoming_data = {
                "id": upcoming_appt.id,
                "date": upcoming_appt.date.isoformat(),
                "time": upcoming_appt.time.strftime("%H:%M"),
                "status": upcoming_appt.status.value,
                "doctor": {
                    "id": doctor.id,
                    "name": doctor.full_name,
                    "specialization": doctor.specialization.name if doctor.specialization else None,
                }
            }

        recent_appts = (
            session.query(Appointment)
            .filter(Appointment.patient_id == patient.id)
            .order_by(Appointment.date.desc(), Appointment.time.desc())
            .limit(5)
            .all()
        )

        recent_appointments = []
        for ap in recent_appts:
            doctor = session.query(DoctorProfile).get(ap.doctor_id)

            recent_appointments.append({
                "id": ap.id,
                "date": ap.date.isoformat(),
                "time": ap.time.strftime("%H:%M"),
                "status": ap.status.value,
                "doctor": {
                    "id": doctor.id,
                    "name": doctor.full_name,
                    "specialization": doctor.specialization.name if doctor.specialization else None,
                }
            })

        recent_records_q = (
            session.query(MedicalRecord)
            .join(Appointment, MedicalRecord.appointment_id == Appointment.id)
            .filter(Appointment.patient_id == patient.id)
            .order_by(MedicalRecord.created_at.desc())
            .limit(5)
            .all()
        )

        recent_records = []
        for rec in recent_records_q:
            ap = session.query(Appointment).get(rec.appointment_id)
            doctor = session.query(DoctorProfile).get(ap.doctor_id)

            recent_records.append({
                "id": rec.id,
                "visit_type": rec.visit_type,
                "tests": rec.tests_done,
                "diagnosis": rec.diagnosis,
                "medicines": rec.medicines,
                "prescription": rec.prescription,
                "notes": rec.notes,
                "date": ap.date.isoformat(),
                "doctor": {
                    "id": doctor.id,
                    "name": doctor.full_name,
                    "specialization": doctor.specialization.name if doctor.specialization else None,
                }
            })

        return {
            "stats": {
                "upcoming": upcoming_count,
                "total": total_appointments,
                "completed": completed_appointments,
            },
            "upcomingAppointment": upcoming_data,
            "recentAppointments": recent_appointments,
            "recentRecords": recent_records
        }, 200
