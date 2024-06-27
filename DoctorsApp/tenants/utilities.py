from django_tenants.utils import schema_context
from DoctorsApp.tenants.models import Member, Doctor
import logging

logger = logging.getLogger(__name__)
def get_doctor(user):
    try:
        doctor = Doctor.objects.get(user=user)
        return doctor.tenant
    except Doctor.DoesNotExist:
        return None
def get_patients_for_doctor(doctor):
    with schema_context(doctor.tenant.schema_name):
        return Member.objects.filter(doctor=doctor)
