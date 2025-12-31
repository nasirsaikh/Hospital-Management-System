from flask_restful import Resource, reqparse, request
from flask_jwt_extended import jwt_required, get_jwt
from database import get_db_session
from models import DoctorProfile, User, UserRole, Specialization, DoctorAvailability
from werkzeug.security import generate_password_hash

def require_admin():
    return get_jwt().get("role", "").upper() == "ADMIN"

doctor_parser = reqparse.RequestParser()
doctor_parser.add_argument("full_name", type=str)
doctor_parser.add_argument("email", type=str)
doctor_parser.add_argument("password", type=str)
doctor_parser.add_argument("phone", type=str)
doctor_parser.add_argument("gender", type=str)
doctor_parser.add_argument("age", type=int)
doctor_parser.add_argument("specialization_id", type=int)
doctor_parser.add_argument("experience_years", type=int)
doctor_parser.add_argument("qualification", type=str)
doctor_parser.add_argument("bio", type=str)
doctor_parser.add_argument("consultation_fee", type=float)

class AdminDoctors(Resource):

    @jwt_required()
    def get(self):
        if not require_admin():
            return {"message": "Admin only"}, 403

        session = get_db_session()
        docs = session.query(DoctorProfile).all()

        result = []
        for d in docs:
            result.append({
                "id": d.id,
                "full_fullname": d.full_name,
                "full_name": d.full_name,
                "email": d.user.email,
                "phone": d.phone,
                "documents": d.documents if hasattr(d, "documents") else None,
                "specialization_id": d.specialization_id,
                "specialization": d.specialization.name if d.specialization else "",
                "experience_years": d.experience_years,
                "qualification": d.qualification,
                "bio": d.bio,
                "consultation_fee": d.consultation_fee,
                "is_verified": d.is_verified,
                "is_active": d.is_active,
            })

        return result, 200

    @jwt_required()
    def post(self):
        if not require_admin():
            return {"message": "Admin only"}, 403

        data = doctor_parser.parse_args()
        session = get_db_session()

        if not data["email"] or not data["password"]:
            return {"message": "Email and password required"}, 400

        if session.query(User).filter_by(email=data["email"]).first():
            return {"message": "Email already exists"}, 400

        user = User(
            name=data["full_name"],
            email=data["email"],
            password=generate_password_hash(data["password"]),
            role=UserRole.DOCTOR
        )
        session.add(user)
        session.flush()

        doc = DoctorProfile(
            user_id=user.id,
            full_name=data["full_name"],
            phone=data["phone"],
            gender=data["gender"],
            age=data["age"],
            specialization_id=data["specialization_id"],
            experience_years=data["experience_years"] or 0,
            qualification=data["qualification"],
            bio=data["bio"],
            consultation_fee=data["consultation_fee"] or 0.0,
        )

        session.add(doc)
        session.commit()

        return {"message": "Doctor created", "id": doc.id}, 201

class AdminDoctorDetail(Resource):

    @jwt_required()
    def get(self, doc_id):
        if not require_admin():
            return {"message": "Admin only"}, 403

        session = get_db_session()
        d = session.query(DoctorProfile).get(doc_id)

        if not d:
            return {"message": "Not found"}, 404

        return {
            "id": d.id,
            "full_name": d.full_name,
            "email": d.user.email,
            "phone": d.phone,
            "gender": d.gender,
            "age": d.age,
            "specialization_id": d.specialization_id,
            "specialization": d.specialization.name if d.specialization else "",
            "qualification": d.qualification,
            "bio": d.bio,
            "experience_years": d.experience_years,
            "consultation_fee": d.consultation_fee,
            "is_verified": d.is_verified,
            "is_active": d.is_active,
            "documents": d.documents if hasattr(d, "documents") else None
        }, 200

    @jwt_required()
    def put(self, doc_id):
        if not require_admin():
            return {"message": "Admin only"}, 403

        session = get_db_session()
        doc = session.query(DoctorProfile).get(doc_id)

        if not doc:
            return {"message": "Not found"}, 404

        data = doctor_parser.parse_args()

        if data["email"]:
            doc.user.email = data["email"]

        if data["full_name"]:
            doc.full_name = data["full_name"]
            doc.user.name = data["full_name"]

        if data["password"]:
            doc.user.password = generate_password_hash(data["password"])

        for field in [
            "phone", "gender", "age", "specialization_id",
            "experience_years", "qualification", "bio",
            "consultation_fee"
        ]:
            value = data.get(field)
            if value is not None:
                setattr(doc, field, value)

        session.commit()
        return {"message": "Doctor updated"}, 200

    @jwt_required()
    def delete(self, doc_id):
        if not require_admin():
            return {"message": "Admin only"}, 403

        session = get_db_session()
        doc = session.query(DoctorProfile).get(doc_id)

        if not doc:
            return {"message": "Not found"}, 404

        session.delete(doc.user)
        session.commit()

        return {"message": "Doctor deleted"}, 200

class AdminDoctorVerify(Resource):

    @jwt_required()
    def put(self, doc_id):
        if not require_admin():
            return {"message": "Admin only"}, 403

        session = get_db_session()
        doc = session.query(DoctorProfile).get(doc_id)

        if not doc:
            return {"message": "Not found"}, 404

        doc.is_verified = True
        session.commit()

        return {"message": "Doctor verified"}, 200

class AdminDoctorToggleActive(Resource):

    @jwt_required()
    def put(self, doc_id):
        if not require_admin():
            return {"message": "Admin only"}, 403

        session = get_db_session()
        doc = session.query(DoctorProfile).get(doc_id)

        if not doc:
            return {"message": "Not found"}, 404

        doc.is_active = not doc.is_active
        session.commit()

        return {"message": "Status updated", "is_active": doc.is_active}, 200

class AdminDoctorAvailability(Resource):

    @jwt_required()
    def get(self, doc_id):
        if not require_admin():
            return {"message": "Admin only"}, 403

        session = get_db_session()
        doc = session.query(DoctorProfile).get(doc_id)

        if not doc:
            return {"message": "Not found"}, 404

        return [{
            "id": a.id,
            "day": a.day,
            "start": str(a.start),
            "end": str(a.end),
        } for a in doc.availability], 200

    @jwt_required()
    def post(self, doc_id):
        if not require_admin():
            return {"message": "Admin only"}, 403

        data = request.json
        session = get_db_session()

        new_slot = DoctorAvailability(
            doctor_id=doc_id,
            day=data["day"],
            start=data["start"],
            end=data["end"]
        )

        session.add(new_slot)
        session.commit()

        return {"message": "Slot added"}, 201

class AdminDoctorAvailabilityDetail(Resource):

    @jwt_required()
    def delete(self, doc_id, slot_id):
        if not require_admin():
            return {"message": "Admin only"}, 403

        session = get_db_session()
        slot = session.query(DoctorAvailability).get(slot_id)

        if not slot:
            return {"message": "Not found"}, 404

        session.delete(slot)
        session.commit()

        return {"message": "Slot deleted"}, 200
