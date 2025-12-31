from flask_restful import Resource
from flask import request
from models import User, UserRole, PatientProfile, DoctorProfile
from database import get_db_session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta


class Register(Resource):
    def post(self):
        data = request.json or {}
        session = get_db_session()

        required = ["name", "email", "password",
                    "age", "gender", "phone", "address"]
        missing = [f for f in required if not data.get(f)]

        if missing:
            return {"message": f"Missing fields: {', '.join(missing)}"}, 400

        email = data["email"].strip().lower()
        if session.query(User).filter_by(email=email).first():
            return {"message": "Email already exists"}, 400

        user = User(
            name=data["name"].strip(),
            email=email,
            password=generate_password_hash(data["password"]),
            role=UserRole.PATIENT,
        )
        session.add(user)
        session.flush()

        profile = PatientProfile(
            user_id=user.id,
            age=int(data["age"]),
            gender=data["gender"],
            phone=data["phone"],
            address=data["address"],
        )
        session.add(profile)
        session.commit()

        token = create_access_token(
            identity=str(user.id), expires_delta=timedelta(days=7)
        )

        return {
            "message": "Patient registered successfully",
            "token": token,
            "role": user.role.value,
        }, 201


class Login(Resource):
    def post(self):
        data = request.json
        session = get_db_session()

        email = data.get("email")
        password = data.get("password")
        requested_role = data.get("role")

        if not email or not password or not requested_role:
            return {"message": "Missing fields"}, 400

        user = session.query(User).filter_by(email=email).first()

        if not user:
            return {"message": "User does not exist"}, 404

        if not check_password_hash(user.password, password):
            return {"message": "Incorrect password"}, 400

        if user.role.value != requested_role:
            return {"message": f"Invalid login for {requested_role} portal"}, 403
        if not user.is_active:
            return {"message": f"Your account is not active!"}, 403

        if user.role == UserRole.DOCTOR:
            doctor = session.query(DoctorProfile).filter_by(
                user_id=user.id).first()
            if not doctor:
                return {"message": "Doctor profile missing"}, 400
            if not doctor.is_active:
                return {"message": "Doctor account inactive"}, 403
            if not doctor.is_verified:
                return {"message": "Doctor not verified by admin"}, 403

        token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.role.value}
        )

        user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.value
        }

        return {
            "token": token,
            "role": user.role.value,
            "user": user_data
        }, 200
