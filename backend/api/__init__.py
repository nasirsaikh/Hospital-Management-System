# ============================
# AUTH ENDPOINTS
# ============================
from .auth import Register, Login

# ============================
# ADMIN ENDPOINTS
# ============================
from .admin.admin_dashboard import AdminDashboard
from .admin.admin_appointments import (
    AdminAppointments,
    AdminAppointmentDetail,
    AdminAppointmentStatus,
)
from .admin.admin_doctors import (
    AdminDoctors,
    AdminDoctorDetail,
    AdminDoctorVerify,
    AdminDoctorToggleActive,
    AdminDoctorAvailability,
    AdminDoctorAvailabilityDetail,
)
from .admin.admin_specialization import (
    AdminSpecializations,
    AdminSpecializationDetail,
)
from .admin.admin_patient import (
    AdminPatients,
    AdminPatientDetail,
    AdminPatientToggle,
)
from .admin.task import *
from .admin.AdminPatientHistory import AdminPatientHistoryAPI

# ============================
# DOCTOR ENDPOINTS
# ============================
from .doctor.dashboard import DoctorDashboard
from .doctor.availibility import (
    DoctorAvailabilityList,
    DoctorAvailabilityDetail,
)
from .doctor.appointments import (
    DoctorAppointments,
    DoctorAppointmentDetail,
)
from .doctor.profile import DoctorProfileMe
from .doctor.patients import DoctorPatients
from .doctor.PatientHistory import DoctorPatientHistoryAPI
from .doctor.records import DoctorMedicalRecordAPI

# ============================
# PATIENT ENDPOINTS
# ============================
from .patient.dashboard import PatientDashboard
from .patient.appointment import *
from .patient.records import PatientMedicalRecordsAPI
from .patient.profile import PatientProfileAPI
from .patient.export import PatientExportTreatmentsAPI

# ============================
# TEST ENDPOINTS
# ============================
from .test_email import TestEmail


def register_routes(api):

    # ============================
    # TEST
    # ============================
    api.add_resource(TestEmail, "/test-email")

    # ============================
    # AUTH
    # ============================
    api.add_resource(Register, "/auth/register")
    api.add_resource(Login, "/auth/login")

    # ============================
    # ADMIN
    # ============================
    api.add_resource(AdminDashboard, "/admin/dashboard")
    api.add_resource(TaskLogsAPI, "/admin/tasks/<string:task_id>")

    api.add_resource(AdminSpecializations, "/admin/specializations")
    api.add_resource(
        AdminSpecializationDetail,
        "/admin/specializations/<int:spec_id>",
    )

    api.add_resource(AdminDoctors, "/admin/doctors")
    api.add_resource(AdminDoctorDetail, "/admin/doctors/<int:doc_id>")
    api.add_resource(AdminDoctorVerify, "/admin/doctors/<int:doc_id>/verify")
    api.add_resource(
        AdminDoctorToggleActive,
        "/admin/doctors/<int:doc_id>/toggle-status",
    )

    api.add_resource(
        AdminDoctorAvailability,
        "/admin/doctors/<int:doc_id>/availability",
    )
    api.add_resource(
        AdminDoctorAvailabilityDetail,
        "/admin/doctors/<int:doc_id>/availability/<int:slot_id>",
    )

    api.add_resource(AdminAppointments, "/admin/appointments")
    api.add_resource(
        AdminAppointmentDetail,
        "/admin/appointments/<int:appt_id>",
    )
    api.add_resource(
        AdminPatientHistoryAPI,
        "/admin/patients/<int:patient_id>/records",
    )
    api.add_resource(
        AdminAppointmentStatus,
        "/admin/appointments/<int:appt_id>/status",
    )

    api.add_resource(AdminPatients, "/admin/patients")
    api.add_resource(
        AdminPatientDetail,
        "/admin/patients/<int:patient_id>",
    )
    api.add_resource(
        AdminPatientToggle,
        "/admin/patients/<int:patient_id>/toggle",
    )

    # ============================
    # DOCTOR
    # ============================
    api.add_resource(DoctorDashboard, "/doctor/dashboard")
    api.add_resource(DoctorProfileMe, "/doctor/profile")

    api.add_resource(DoctorAvailabilityList, "/doctor/availability")
    api.add_resource(
        DoctorAvailabilityDetail,
        "/doctor/availability/<int:slot_id>",
    )

    api.add_resource(DoctorAppointments, "/doctor/appointments")
    api.add_resource(
        DoctorAppointmentDetail,
        "/doctor/appointments/<int:appointment_id>",
    )

    api.add_resource(DoctorPatients, "/doctor/patients")
    api.add_resource(
        DoctorMedicalRecordAPI,
        "/doctor/records",
        "/doctor/records/<int:appointment_id>",
    )
    api.add_resource(
        DoctorPatientHistoryAPI,
        "/doctor/patients/<int:patient_id>/records",
    )

    # ============================
    # PATIENT
    # ============================
    api.add_resource(PatientDashboard, "/patient/dashboard")
    api.add_resource(PatientMedicalRecordsAPI, "/patient/records")
    api.add_resource(PatientProfileAPI, "/patient/profile")
    api.add_resource(PatientExportTreatmentsAPI, "/patient/export-treatments")

    api.add_resource(PatientDoctorListAPI, "/patient/doctors")
    api.add_resource(
        PatientDoctorDetailAPI,
        "/patient/doctors/<int:doctor_id>",
    )
    api.add_resource(
        PatientDoctorAvailabilityAPI,
        "/patient/doctors/<int:doctor_id>/availability",
    )

    api.add_resource(PatientAppointmentsAPI, "/patient/appointments")
    api.add_resource(
        PatientAppointmentDetailAPI,
        "/patient/appointments/<int:appointment_id>",
    )
    api.add_resource(
        PatientCancelAppointmentAPI,
        "/patient/appointments/<int:appointment_id>/cancel",
    )
