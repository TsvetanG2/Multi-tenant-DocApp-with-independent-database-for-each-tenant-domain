
from django.dispatch import receiver
from django_tenants.models import TenantMixin
from django_tenants.signals import post_schema_sync
from django_tenants.utils import tenant_context
from DoctorsApp.tenants.models import Settings

@receiver(post_schema_sync, sender=TenantMixin)
def generate_settings(sender, **kwargs):
    tenant = kwargs["tenant"]

    # If post_schema_sync runs against public schema will throw
    if tenant.schema_name == "public":
        pass
    else:
        with tenant_context(tenant):
            settings = Settings()
            settings.save()
            print(f"Generated Users Settings for [{tenant.schema_name}]")
