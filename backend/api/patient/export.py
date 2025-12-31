from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from utils.auth import role_required
from tasks.background_jobs import export_patient_treatments_csv


class PatientExportTreatmentsAPI(Resource):

    @role_required("patient")
    def post(self):
        """
        POST /patient/export-treatments
        Triggers async CSV export and email.
        """
        user_id = int(get_jwt_identity())

        export_patient_treatments_csv(user_id)
        return {
            "message": "Export started. You will receive an email once it's ready."
        }, 202
