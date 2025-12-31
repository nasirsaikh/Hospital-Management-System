from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from datetime import date

from database import get_db_session
from models import (
    User, UserRole,
    Appointment, AppointmentStatus,
    DoctorProfile, PatientProfile
)

def require_admin():
    claims = get_jwt()
    role = claims.get("role")
    return role and role.upper() == "ADMIN"

class AdminDashboard(Resource):

    @jwt_required()
    def get(self):
        if not require_admin():
            return {"message": "Admin access only"}, 403

        session = get_db_session()

        total_doctors = (
            session.query(User)
            .filter(User.role == UserRole.DOCTOR)
            .count()
        )

        total_patients = (
            session.query(User)
            .filter(User.role == UserRole.PATIENT)
            .count()
        )

        total_appointments = session.query(Appointment).count()

        completed_appointments = (
            session.query(Appointment)
            .filter(Appointment.status == AppointmentStatus.COMPLETED)
            .count()
        )

        today_appointments = (
            session.query(Appointment)
            .filter(Appointment.date == date.today())
            .count()
        )

        pending_verifications = (
            session.query(DoctorProfile)
            .filter(DoctorProfile.is_verified == False)
            .count()
        )

        recent = (
            session.query(Appointment)
            .order_by(Appointment.date.desc(), Appointment.time.desc())
            .limit(10)
            .all()
        )

        recent_list = []
        for a in recent:
            doctor = session.query(DoctorProfile).get(a.doctor_id)
            patient = session.query(PatientProfile).get(a.patient_id)

            recent_list.append({
                "id": a.id,
                "doctor": doctor.full_name if doctor else None,
                "patient": patient.user.name if patient and patient.user else None,
                "date": a.date.isoformat(),
                "time": a.time.strftime("%H:%M"),
                "status": a.status.value,
            })

        return {
            "stats": {
                "doctors": total_doctors,
                "patients": total_patients,
                "appointments": total_appointments,
                "completed": completed_appointments,
                "pendingVerifications": pending_verifications,
                "today": today_appointments,
            },
            "recentAppointments": recent_list,
        }, 200
