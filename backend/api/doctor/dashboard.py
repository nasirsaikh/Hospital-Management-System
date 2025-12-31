from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from datetime import date

from database import get_db_session
from models import (
    DoctorProfile,
    Appointment,
    AppointmentStatus,
    PatientProfile,
    DoctorAvailability,
)
from utils.auth import role_required

class DoctorDashboard(Resource):

    @role_required("doctor")
    def get(self):
        session = get_db_session()

        user_id = int(get_jwt_identity())
        doctor = session.query(DoctorProfile).filter_by(user_id=user_id).first()

        if not doctor:
            return {"message": "Doctor profile not found"}, 404

        total_patients = (
            session.query(Appointment.patient_id)
            .filter(Appointment.doctor_id == doctor.id)
            .distinct()
            .count()
        )

        upcoming_count = (
            session.query(Appointment)
            .filter(Appointment.doctor_id == doctor.id)
            .filter(Appointment.date >= date.today())
            .filter(Appointment.status != AppointmentStatus.CANCELLED)
            .filter(Appointment.status != AppointmentStatus.COMPLETED)
            .count()
        )

        today = date.today()

        today_slots = []
        today_availability = (
            session.query(DoctorAvailability)
            .filter(DoctorAvailability.doctor_id == doctor.id)
            .filter(DoctorAvailability.date == today)
            .filter(DoctorAvailability.is_available.is_(True))
            .all()
        )

        for slot in today_availability:
            today_slots.append({
                "id": slot.id,
                "date": slot.date.isoformat(),
                "slot_type": slot.slot_type,
                "start_time": slot.start_time.strftime("%H:%M") if slot.start_time else None,
                "end_time": slot.end_time.strftime("%H:%M") if slot.end_time else None,
            })

        next_upcoming = (
            session.query(Appointment)
            .filter(Appointment.doctor_id == doctor.id)
            .filter(Appointment.date >= today)
            .filter(Appointment.status != AppointmentStatus.CANCELLED)
            .filter(Appointment.status != AppointmentStatus.COMPLETED)
            .order_by(Appointment.date.asc(), Appointment.time.asc())
            .limit(5)
            .all()
        )

        upcoming_list = []
        for a in next_upcoming:
            patient = session.query(PatientProfile).get(a.patient_id)
            upcoming_list.append({
                "id": a.id,
                "date": a.date.isoformat(),
                "time": a.time.strftime("%H:%M"),
                "status": a.status.value,
                "patient_name": patient.user.name if patient and patient.user else None,
            })

        return {
            "doctor": {
                "id": doctor.id,
                "full_name": doctor.full_name,
                "email": doctor.user.email,
                "specialization": doctor.specialization.name if doctor.specialization else None,
                "photo_url": getattr(doctor, "photo_url", None),
            },
            "stats": {
                "total_patients": total_patients,
                "upcoming_appointments": upcoming_count,
                "is_verified": doctor.is_verified,
                "is_active": doctor.is_active,
            },
            "today_availability": today_slots,
            "upcoming_appointments": upcoming_list,
        }, 200
