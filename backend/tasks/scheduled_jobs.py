

from datetime import date, datetime, timedelta

from .celery_app import celery
from database import get_db_session
from models import (
    Appointment,
    AppointmentStatus,
    PatientProfile,
    DoctorProfile,
    MedicalRecord,
)
from utils.notifications import send_email


@celery.task(name="tasks.daily_appointment_reminder")
def send_daily_appointment_reminders():
    session = get_db_session()

    today = date.today()

    appts = (
        session.query(Appointment)
        .filter(Appointment.date == today)
        .filter(Appointment.status != AppointmentStatus.CANCELLED)
        .all()
    )

    for a in appts:
        if not a.patient or not a.patient.user or not a.patient.user.email:
            continue

        subject = "Appointment Reminder"
        body = f"""
        <p>Dear {a.patient.user.name},</p>
        <p>This is a reminder for your appointment today.</p>
        <ul>
            <li><strong>Doctor:</strong> {a.doctor.full_name}</li>
            <li><strong>Time:</strong> {a.time.strftime("%H:%M")}</li>
            <li><strong>Date:</strong> {a.date.isoformat()}</li>
        </ul>
        <p>Please reach 10 minutes early.</p>
        """

        send_email(a.patient.user.email, subject, body)

    return f"Sent reminders for {len(appts)} appointments"


@celery.task(name="tasks.monthly_doctor_report")
def send_monthly_doctor_reports():
    """
    This will be scheduled monthly via Celery beat.
    If you schedule it daily, add a guard: only run on day == 1.
    """
    session = get_db_session()

    today = date.today()

    first_day_this_month = today.replace(day=1)
    last_month_end = first_day_this_month - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)

    doctors = session.query(DoctorProfile).all()

    for doc in doctors:
        if not doc.user or not doc.user.email:
            continue

        appts = (
            session.query(Appointment)
            .filter(Appointment.doctor_id == doc.id)
            .filter(Appointment.date >= last_month_start)
            .filter(Appointment.date <= last_month_end)
            .all()
        )

        rows = []
        for a in appts:

            record = getattr(a, "medical_record", None) or getattr(
                a, "treatment", None)

            rows.append({
                "patient": a.patient.user.name if a.patient and a.patient.user else "",
                "date": a.date.isoformat(),
                "time": a.time.strftime("%H:%M"),
                "diagnosis": getattr(record, "diagnosis", "") if record else "",
                "prescription": getattr(record, "prescription", "") if record else "",
                "notes": getattr(record, "notes", "") if record else "",
            })

        html_rows = "".join(
            f"<tr>"
            f"<td>{r['patient']}</td>"
            f"<td>{r['date']} {r['time']}</td>"
            f"<td>{r['diagnosis']}</td>"
            f"<td>{r['prescription']}</td>"
            f"<td>{r['notes']}</td>"
            f"</tr>"
            for r in rows
        )

        html_body = f"""
        <h2>Monthly Activity Report for Dr. {doc.full_name}</h2>
        <p>Period: {last_month_start} → {last_month_end}</p>
        <table border='1' cellpadding='6'>
            <tr>
                <th>Patient</th><th>Date & Time</th>
                <th>Diagnosis</th><th>Prescription</th><th>Notes</th>
            </tr>
            {html_rows}
        </table>
        """

        send_email(doc.user.email, "Monthly Activity Report", html_body)

    return "Monthly doctor reports sent"
