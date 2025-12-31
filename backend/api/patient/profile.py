from flask_restful import Resource
from flask import request
from flask_jwt_extended import get_jwt_identity
from utils.auth import role_required
from database import get_db_session

from models import User, PatientProfile


class PatientProfileAPI(Resource):

    @role_required("patient")
    def get(self):
        """Return patient + user profile data"""
        session = get_db_session()
        user_id = int(get_jwt_identity())

        user = session.query(User).get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        patient = session.query(PatientProfile).filter_by(
            user_id=user_id).first()
        if not patient:
            return {"message": "Patient profile not found"}, 404

        return {
            "id": patient.id,
            "name": user.name,
            "age": patient.age,
            "gender": patient.gender,
            "phone": patient.phone,
            "address": patient.address,
        }, 200

    @role_required("patient")
    def put(self):
        """Update patient + user profile data"""

        session = get_db_session()
        user_id = int(get_jwt_identity())

        user = session.query(User).get(user_id)
        patient = session.query(PatientProfile).filter_by(
            user_id=user_id).first()

        if not user or not patient:
            return {"message": "Profile not found"}, 404

        data = request.json or {}

        if "name" in data:
            user.name = data["name"]

        if "age" in data:
            patient.age = data["age"]

        if "gender" in data:
            patient.gender = data["gender"]

        if "phone" in data:
            patient.phone = data["phone"]

        if "address" in data:
            patient.address = data["address"]

        session.commit()

        return {"message": "Profile updated successfully"}, 200
