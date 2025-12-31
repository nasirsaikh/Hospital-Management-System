from flask_restful import Resource
from flask import request
from flask_jwt_extended import get_jwt_identity
from datetime import date, datetime, timedelta, time

from database import get_db_session
from models import DoctorProfile, DoctorAvailability
from utils.auth import role_required

MORNING_START = time(8, 0)
MORNING_END = time(12, 0)

EVENING_START = time(14, 0)
EVENING_END = time(20, 0)

def is_30min_step(t: time):
    return (t.minute % 30) == 0

def generate_30min_slots(start: time, end: time):
    slots = []
    current = datetime.combine(date.today(), start)
    end_dt = datetime.combine(date.today(), end)

    while current < end_dt:
        slots.append(current.time().strftime("%H:%M"))
        current += timedelta(minutes=30)

    return slots

def check_within_window(slot_type, start, end):
    if slot_type == "morning":
        return MORNING_START <= start <= MORNING_END and MORNING_START <= end <= MORNING_END
    else:
        return EVENING_START <= start <= EVENING_END and EVENING_START <= end <= EVENING_END

class DoctorAvailabilityList(Resource):

    @role_required("doctor")
    def get(self):
        session = get_db_session()
        user_id = int(get_jwt_identity())

        doctor = session.query(DoctorProfile).filter_by(user_id=user_id).first()
        if not doctor:
            return {"message": "Doctor not found"}, 404

        today = date.today()
        days = [today + timedelta(days=i) for i in range(8)]

        response = []

        for d in days:
            slots = session.query(DoctorAvailability).filter_by(
                doctor_id=doctor.id, date=d
            ).all()

            slot_map = {s.slot_type: s for s in slots}

            def serialize(slot_type):
                slot = slot_map.get(slot_type)

                start_time = slot.start_time if slot else None
                end_time = slot.end_time if slot else None

                return {
                    "id": slot.id if slot else None,
                    "slot_type": slot_type,
                    "is_available": slot.is_available if slot else False,
                    "start_time": start_time.strftime("%H:%M") if start_time else None,
                    "end_time": end_time.strftime("%H:%M") if end_time else None,
                    "timeslots": (
                        generate_30min_slots(start_time, end_time)
                        if slot and slot.is_available and start_time and end_time
                        else []
                    )
                }

            response.append({
                "date": d.isoformat(),
                "morning": serialize("morning"),
                "evening": serialize("evening"),
            })

        return response, 200

    @role_required("doctor")
    def post(self):
        session = get_db_session()
        data = request.json or {}

        required = ["date", "slot_type"]
        for r in required:
            if r not in data:
                return {"message": f"{r} is required"}, 400

        try:
            slot_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        except:
            return {"message": "Invalid date format"}, 400

        slot_type = data["slot_type"].lower()
        if slot_type not in ("morning", "evening"):
            return {"message": "Invalid slot_type"}, 400

        user_id = int(get_jwt_identity())
        doctor = session.query(DoctorProfile).filter_by(user_id=user_id).first()

        slot = session.query(DoctorAvailability).filter_by(
            doctor_id=doctor.id, date=slot_date, slot_type=slot_type
        ).first()

        if not slot:
            slot = DoctorAvailability(
                doctor_id=doctor.id,
                date=slot_date,
                slot_type=slot_type
            )
            session.add(slot)

        slot.is_available = bool(data.get("is_available", False))

        if slot.is_available:
            try:
                start = datetime.strptime(data["start_time"], "%H:%M").time()
                end = datetime.strptime(data["end_time"], "%H:%M").time()
            except:
                return {"message": "Invalid start/end time"}, 400

            if not (is_30min_step(start) and is_30min_step(end)):
                return {"message": "Time must be in 30-minute intervals"}, 400

            if start >= end:
                return {"message": "start_time must be before end_time"}, 400

            if not check_within_window(slot_type, start, end):
                return {"message": f"{slot_type} slot must be inside allowed window"}, 400

            slot.start_time = start
            slot.end_time = end
        else:
            slot.start_time = None
            slot.end_time = None

        session.commit()
        return {"message": "Availability updated"}, 200


class DoctorAvailabilityDetail(Resource):

    @role_required("doctor")
    def put(self, slot_id):
        session = get_db_session()

        slot = session.query(DoctorAvailability).get(slot_id)
        if not slot:
            return {"message": "Availability slot not found"}, 404

        data = request.json or {}

        if "is_available" in data:
            slot.is_available = bool(data["is_available"])

        if "start_time" in data:
            slot.start_time = datetime.strptime(data["start_time"], "%H:%M").time()

        if "end_time" in data:
            slot.end_time = datetime.strptime(data["end_time"], "%H:%M").time()

        session.commit()
        return {"message": "Slot updated"}, 200

    @role_required("doctor")
    def delete(self, slot_id):
        session = get_db_session()

        slot = session.query(DoctorAvailability).get(slot_id)
        if not slot:
            return {"message": "Availability slot not found"}, 404

        session.delete(slot)
        session.commit()

        return {"message": "Slot deleted"}, 200
