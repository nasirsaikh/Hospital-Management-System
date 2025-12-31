

from flask_restful import Resource
from flask import request
from flask_jwt_extended import get_jwt_identity

from datetime import datetime, date, timedelta


from database import get_db_session
from models import (
    User,
    DoctorProfile,
    Specialization,
    DoctorAvailability,
    Appointment,
    AppointmentStatus,
    PatientProfile,
)
from utils.auth import role_required

from sqlalchemy import or_, func

from cache.cache_utils import cache_get, cache_set


class PatientDoctorListAPI(Resource):

    @role_required("patient")
    def get(self):
        session = get_db_session()

        search = request.args.get("search", "", type=str).strip()
        specialization_id = request.args.get("specialization", type=int)
        sort = request.args.get("sort", "", type=str)

        use_cache = (not search) and (not specialization_id) and (not sort)
        cache_key = "patient:doctors:all"

        if use_cache:
            cached = cache_get(cache_key)
            if cached is not None:
                return cached, 200

        q = (
            session.query(DoctorProfile)
            .join(User, DoctorProfile.user_id == User.id)
            .outerjoin(Specialization, DoctorProfile.specialization_id == Specialization.id)
            .filter(DoctorProfile.is_active.is_(True))
            .filter(DoctorProfile.is_verified.is_(True))
        )

        if search:
            like = f"%{search.lower()}%"
            q = q.filter(
                or_(
                    func.lower(DoctorProfile.full_name).like(like),
                    func.lower(User.name).like(like),
                    func.lower(Specialization.name).like(like),
                )
            )

        if specialization_id:
            q = q.filter(DoctorProfile.specialization_id == specialization_id)

        if sort == "fees_low":
            q = q.order_by(DoctorProfile.consultation_fee.asc())
        elif sort == "fees_high":
            q = q.order_by(DoctorProfile.consultation_fee.desc())
        elif sort == "exp_high":
            q = q.order_by(DoctorProfile.experience_years.desc())
        elif sort == "exp_low":
            q = q.order_by(DoctorProfile.experience_years.asc())

        doctors = q.all()

        result = []
        for d in doctors:
            result.append({
                "id": d.id,
                "name": d.full_name,
                "specialization": d.specialization.name if d.specialization else None,
                "fees": d.consultation_fee or 0.0,
                "experience": d.experience_years or 0,
                "bio": d.bio or "",
                "photo": getattr(d, "photo_url", None),
            })

        if use_cache:
            cache_set(cache_key, result, ttl=60)

        return result, 200


class PatientDoctorDetailAPI(Resource):

    @role_required("patient")
    def get(self, doctor_id):
        session = get_db_session()

        d = (
            session.query(DoctorProfile)
            .join(User, DoctorProfile.user_id == User.id)
            .outerjoin(Specialization, DoctorProfile.specialization_id == Specialization.id)
            .filter(DoctorProfile.id == doctor_id)
            .filter(DoctorProfile.is_active.is_(True))
            .filter(DoctorProfile.is_verified.is_(True))
            .first()
        )

        if not d:
            return {"message": "Doctor not found"}, 404

        return {
            "id": d.id,
            "name": d.full_name,
            "email": d.user.email,
            "phone": d.phone,
            "gender": d.gender,
            "age": d.age,
            "specialization": d.specialization.name if d.specialization else None,
            "experience": d.experience_years or 0,
            "fees": d.consultation_fee or 0.0,
            "qualification": d.qualification,
            "bio": d.bio or "",
            "photo": getattr(d, "photo_url", None),
        }, 200


class PatientDoctorAvailabilityAPI(Resource):

    @role_required("patient")
    def get(self, doctor_id):
        session = get_db_session()

        doctor = session.query(DoctorProfile).get(doctor_id)
        if not doctor or not doctor.is_active or not doctor.is_verified:
            return {"message": "Doctor not found or not available"}, 404

        today = date.today()
        end_date = today + timedelta(days=7)

        avail_rows = (
            session.query(DoctorAvailability)
            .filter(DoctorAvailability.doctor_id == doctor_id)
            .filter(DoctorAvailability.date >= today)
            .filter(DoctorAvailability.date <= end_date)
            .filter(DoctorAvailability.is_available.is_(True))
            .all()
        )

        slots = []

        for row in avail_rows:
            if not row.start_time:
                continue

            conflict = (
                session.query(Appointment)
                .filter(Appointment.doctor_id == doctor_id)
                .filter(Appointment.date == row.date)
                .filter(Appointment.time == row.start_time)
                .filter(Appointment.status != AppointmentStatus.CANCELLED)
                .first()
            )

            if conflict:
                continue

            slots.append({
                "id": row.id,
                "date": row.date.isoformat(),
                "time": row.start_time.strftime("%H:%M"),
            })

        return slots, 200


class PatientAppointmentsAPI(Resource):

    @role_required("patient")
    def post(self):
        """
        Body JSON:
        {
            "doctor_id": int,
            "date": "YYYY-MM-DD",
            "time": "HH:MM"
        }
        """
        session = get_db_session()
        user_id = int(get_jwt_identity())

        patient = session.query(PatientProfile).filter_by(
            user_id=user_id).first()
        if not patient:
            return {"message": "Patient profile not found"}, 404

        data = request.json or {}

        doctor_id = data.get("doctor_id")
        date_str = data.get("date")
        time_str = data.get("time")

        if not doctor_id or not date_str or not time_str:
            return {"message": "doctor_id, date and time are required"}, 400

        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            time_obj = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            return {"message": "Invalid date or time format"}, 400

        doctor = session.query(DoctorProfile).get(doctor_id)
        if not doctor or not doctor.is_active or not doctor.is_verified:
            return {"message": "Doctor not found or not available"}, 404

        avail = (
            session.query(DoctorAvailability)
            .filter_by(doctor_id=doctor_id, date=date_obj)
            .filter(DoctorAvailability.is_available.is_(True))
            .filter(DoctorAvailability.start_time == time_obj)
            .first()
        )

        if not avail:
            return {"message": "Selected time is not available"}, 400

        conflict = (
            session.query(Appointment)
            .filter_by(doctor_id=doctor_id, date=date_obj, time=time_obj)
            .filter(Appointment.status != AppointmentStatus.CANCELLED)
            .first()
        )
        if conflict:
            return {"message": "This time slot is already booked"}, 409

        appt = Appointment(
            patient_id=patient.id,
            doctor_id=doctor_id,
            date=date_obj,
            time=time_obj,
            status=AppointmentStatus.PENDING,
        )
        session.add(appt)
        session.commit()

        return {"message": "Appointment booked", "appointment_id": appt.id}, 201

    @role_required("patient")
    def get(self):
        session = get_db_session()
        user_id = int(get_jwt_identity())

        patient = session.query(PatientProfile).filter_by(
            user_id=user_id).first()
        if not patient:
            return {"message": "Patient profile not found"}, 404

        appts = (
            session.query(Appointment)
            .filter(Appointment.patient_id == patient.id)
            .order_by(Appointment.date.desc(), Appointment.time.desc())
            .all()
        )

        result = []
        for a in appts:
            result.append({
                "id": a.id,
                "date": a.date.isoformat(),
                "time": a.time.strftime("%H:%M"),
                "status": a.status.value,
                "doctor": {
                    "id": a.doctor.id,
                    "name": a.doctor.full_name,
                    "specialization": a.doctor.specialization.name if a.doctor.specialization else None,

                },
            })

        return {"appointments": result}, 200


class PatientAppointmentDetailAPI(Resource):

    @role_required("patient")
    def get(self, appointment_id):
        session = get_db_session()
        user_id = int(get_jwt_identity())

        patient = session.query(PatientProfile).filter_by(
            user_id=user_id).first()
        if not patient:
            return {"message": "Patient profile not found"}, 404

        appt = session.query(Appointment).get(appointment_id)
        if not appt or appt.patient_id != patient.id:
            return {"message": "Appointment not found"}, 404

        return {
            "id": appt.id,
            "date": appt.date.isoformat(),
            "time": appt.time.strftime("%H:%M"),
            "status": appt.status.value,
            "notes": appt.notes,
            "doctor": {
                "id": appt.doctor.id,
                "name": appt.doctor.full_name,
                "specialization": appt.doctor.specialization.name if appt.doctor.specialization else None,
                "experience": appt.doctor.experience,
                "fees": appt.doctor.fees,
            }
        }, 200


class PatientCancelAppointmentAPI(Resource):

    @role_required("patient")
    def put(self, appointment_id):
        session = get_db_session()
        user_id = int(get_jwt_identity())

        patient = session.query(PatientProfile).filter_by(
            user_id=user_id).first()
        if not patient:
            return {"message": "Patient profile not found"}, 404

        appt = session.query(Appointment).get(appointment_id)
        if not appt or appt.patient_id != patient.id:
            return {"message": "Appointment not found"}, 404

        if appt.status == AppointmentStatus.CANCELLED:
            return {"message": "Already cancelled"}, 400

        appt.status = AppointmentStatus.CANCELLED
        session.commit()

        return {"message": "Appointment cancelled"}, 200
