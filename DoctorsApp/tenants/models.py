from django.core.validators import MinLengthValidator
from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Settings(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Tenant(TenantMixin):
    MIN_SUBDOMAIN_LENGTH = 5
    MIN_TENANTNAME_LENGTH = 5
    MAX_TENANTNAME_LENGTH = 55
    name = models.CharField(
        null=False,
        blank=False,
        max_length=MAX_TENANTNAME_LENGTH,
        validators=[
            MinLengthValidator(MIN_TENANTNAME_LENGTH),
        ]
    )
    email = models.EmailField(
        blank=False,
        null=False,
    )
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)

    auto_create_schema = True

    def __str__(self):
        return self.name

class Domain(DomainMixin):
    auto_create_schema = True


