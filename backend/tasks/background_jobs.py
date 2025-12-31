

import csv
import io

from .celery_app import celery
from database import get_db_session
from models import Appointment, PatientProfile, MedicalRecord
from utils.notifications import send_email


@celery.task(name="tasks.export_patient_treatments_csv")
def export_patient_treatments_csv(patient_user_id: int):
    session = get_db_session()

    patient = (
        session.query(PatientProfile)
        .filter_by(user_id=patient_user_id)
        .first()
    )

    if not patient or not patient.user or not patient.user.email:
        return "Patient/email not found"

    appts = (
        session.query(Appointment)
        .join(MedicalRecord, MedicalRecord.appointment_id == Appointment.id)
        .filter(Appointment.patient_id == patient.id)
        .order_by(Appointment.date.asc(), Appointment.time.asc())
        .all()
    )

    record_columns = [col.name for col in MedicalRecord.__table__.columns]

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(
        ["patient_user_id", "patient_name", "doctor_name", "date", "time"]
        + record_columns
    )

    for a in appts:
        record = a.medical_record

        writer.writerow(
            [
                patient.user.id,
                patient.user.name,
                a.doctor.full_name if a.doctor else "",
                a.date.isoformat(),
                a.time.strftime("%H:%M"),
            ]
            + [getattr(record, col) for col in record_columns]
        )

    csv_bytes = output.getvalue().encode("utf-8")
    output.close()

    email_html = f"""
        <p>Hello {patient.user.name},</p>

        <p>Your complete treatment history has been exported successfully.</p>

        <p>
            The CSV file containing all your medical records is attached to this email.  
            You can download it and open it in Excel, Google Sheets, or any compatible software.
        </p>

        <p>If you did not request this export, please contact support immediately.</p>

        <br>
        <p>Regards,<br><strong>Smart Hospital</strong></p>
    """

    send_email(
        to=patient.user.email,
        subject="Your Treatment History – CSV Export",
        body=email_html,
        attachments=[("treatment_records.csv", csv_bytes, "text/csv")],
    )

    return "Export complete"
