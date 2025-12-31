from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt
from database import get_db_session
from models import Specialization

def require_admin():
    return get_jwt().get("role", "").upper() == "ADMIN"

spec_parser = reqparse.RequestParser()
spec_parser.add_argument("name", type=str, required=True)
spec_parser.add_argument("description", type=str, required=False)

class AdminSpecializations(Resource):

    @jwt_required()
    def get(self):
        session = get_db_session()
        specs = session.query(Specialization).all()

        return [
            {
                "id": s.id,
                "name": s.name,
                "description": s.description,
            }
            for s in specs
        ], 200

    @jwt_required()
    def post(self):
        if not require_admin():
            return {"message": "Admin only"}, 403

        data = spec_parser.parse_args()
        session = get_db_session()

        spec = Specialization(
            name=data["name"],
            description=data.get("description", "")
        )

        session.add(spec)
        session.commit()

        return {"message": "Specialization created", "id": spec.id}, 201

class AdminSpecializationDetail(Resource):

    @jwt_required()
    def put(self, spec_id):
        if not require_admin():
            return {"message": "Admin only"}, 403

        session = get_db_session()
        spec = session.query(Specialization).get(spec_id)

        if not spec:
            return {"message": "Not found"}, 404

        data = spec_parser.parse_args()

        spec.name = data["name"]
        spec.description = data.get("description", "")

        session.commit()

        return {"message": "Updated"}, 200

    @jwt_required()
    def delete(self, spec_id):
        if not require_admin():
            return {"message": "Admin only"}, 403

        session = get_db_session()
        spec = session.query(Specialization).get(spec_id)

        if not spec:
            return {"message": "Not found"}, 404

        session.delete(spec)
        session.commit()

        return {"message": "Deleted"}, 200
