from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt
from database import get_db_session
from models import User, UserRole, PatientProfile

def require_admin():
    return get_jwt().get("role", "").upper() == "ADMIN"

patient_parser = reqparse.RequestParser()
patient_parser.add_argument("name")
patient_parser.add_argument("email")
patient_parser.add_argument("age", type=int)
patient_parser.add_argument("gender")
patient_parser.add_argument("phone")
patient_parser.add_argument("address")

class AdminPatients(Resource):
    @jwt_required()
    def get(self):
        if not require_admin():
            return {"message": "Admin only"}, 403

        session = get_db_session()

        patients = (
            session.query(PatientProfile)
            .join(User, PatientProfile.user_id == User.id)
            .all()
        )

        data = [
            {
                "id": p.id,
                "user_id": p.user_id,
                "user": {
                    "name": p.user.name,
                    "email": p.user.email,
                    "is_active": p.user.is_active
                },
                "age": p.age,
                "gender": p.gender,
                "phone": p.phone,
                "address": p.address,
            }
            for p in patients
        ]

        return data, 200

class AdminPatientDetail(Resource):
    @jwt_required()
    def get(self, patient_id):
        if not require_admin():
            return {"message": "Admin only"}, 403

        session = get_db_session()

        p = session.query(PatientProfile).get(patient_id)
        if not p:
            return {"message": "Patient not found"}, 404

        return {
            "id": p.id,
            "user_id": p.user_id,
            "user": {
                "name": p.user.name,
                "email": p.user.email,
                "is_active": p.user.is_active
            },
            "age": p.age,
            "gender": p.gender,
            "phone": p.phone,
            "address": p.address,
        }, 200

    @jwt_required()
    def put(self, patient_id):
        if not require_admin():
            return {"message": "Admin only"}, 403

        session = get_db_session()
        p = session.query(PatientProfile).get(patient_id)

        if not p:
            return {"message": "Patient not found"}, 404

        data = patient_parser.parse_args()

        if data.get("name"):
            p.user.name = data["name"]

        if data.get("email"):
            existing_user = session.query(User).filter(User.email == data["email"]).first()
            if existing_user and existing_user.id != p.user.id:
                return {"message": "Email already exists"}, 400
            p.user.email = data["email"]

        for field in ["age", "gender", "phone", "address"]:
            value = data.get(field)
            if value is not None:
                setattr(p, field, value)

        session.commit()
        return {"message": "Updated"}, 200

    @jwt_required()
    def delete(self, patient_id):
        if not require_admin():
            return {"message": "Admin only"}, 403

        session = get_db_session()
        p = session.query(PatientProfile).get(patient_id)
        ac = session.query(User).get(p.user_id)

        if not p:
            return {"message": "Patient not found"}, 404
        session.delete(ac)

        session.delete(p)
        session.commit()

        return {"message": "Patient deleted"}, 200

class AdminPatientToggle(Resource):
    @jwt_required()
    def put(self, patient_id):
        if not require_admin():
            return {"message": "Admin only"}, 403

        session = get_db_session()

        p = session.query(PatientProfile).get(patient_id)
        if not p:
            return {"message": "Not found"}, 404

        p.user.is_active = not p.user.is_active
        session.commit()

        return {
            "message": "Status updated",
            "is_active": p.user.is_active
        }, 200
