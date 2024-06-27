from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from DoctorsApp.tenants.models import Tenant, Domain


# Register the Tenant model with the admin panel
class TenantAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address', 'city', 'state', 'zipcode')
    search_fields = ('name', 'email')

    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new tenant
            obj.create_schema()  # Create schema when tenant is saved
        super().save_model(request, obj, form, change)


admin.site.register(Tenant)
admin.site.register(Domain)
