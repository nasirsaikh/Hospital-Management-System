from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity

from database import get_db_session
from models import DoctorProfile, User
from utils.auth import role_required

profile_parser = reqparse.RequestParser()
profile_parser.add_argument("full_name")
profile_parser.add_argument("phone")
profile_parser.add_argument("gender")
profile_parser.add_argument("age", type=int)
profile_parser.add_argument("qualification")
profile_parser.add_argument("bio")
profile_parser.add_argument("consultation_fee", type=float)

class DoctorProfileMe(Resource):

    @role_required("doctor")
    def get(self):
        session = get_db_session()
        user_id = int(get_jwt_identity())

        doc = session.query(DoctorProfile).filter_by(user_id=user_id).first()
        if not doc:
            return {"message": "Doctor profile not found"}, 404

        user: User = doc.user

        return {
            "id": doc.id,
            "user_id": user.id,
            "full_name": doc.full_name,
            "email": user.email,
            "phone": doc.phone,
            "gender": doc.gender,
            "age": doc.age,
            "specialization_id": doc.specialization_id,
            "specialization": doc.specialization.name if doc.specialization else None,
            "qualification": doc.qualification,
            "bio": doc.bio,
            "experience_years": doc.experience_years,
            "consultation_fee": doc.consultation_fee,
            "is_active": doc.is_active,
            "is_verified": doc.is_verified,
        }, 200

    @role_required("doctor")
    def put(self):
        session = get_db_session()
        user_id = int(get_jwt_identity())

        doc = session.query(DoctorProfile).filter_by(user_id=user_id).first()
        if not doc:
            return {"message": "Doctor profile not found"}, 404

        data = profile_parser.parse_args()

        if data.get("full_name"):
            doc.full_name = data["full_name"]
            doc.user.name = data["full_name"]

        for field in ["phone", "gender", "age", "qualification", "bio", "consultation_fee"]:
            value = data.get(field)
            if value is not None:
                setattr(doc, field, value)

        session.commit()

        return {"message": "Profile updated"}, 200
