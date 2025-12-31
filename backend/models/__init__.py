

from database import db


from .user import User, UserRole
from .patient import PatientProfile
from .doctor import DoctorProfile
from .specialization import Specialization
from .doctor_availability import DoctorAvailability
from .appointment import Appointment, AppointmentStatus
from .medical_record import MedicalRecord

__all__ = [
    "db",
    "User",
    "UserRole",
    "PatientProfile",
    "DoctorProfile",
    "Specialization",
    "DoctorAvailability",
    "Appointment",
    "AppointmentStatus",
    "Treatment",
    "Prescription",
    "MedicalRecord",
]
