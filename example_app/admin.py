from django_descope.models import DescopeUser
from django.contrib import admin


class MyAdminSite(admin.AdminSite):
    login_template = 'admin_login.html'


descope_admin_site = MyAdminSite()
descope_admin_site.register(DescopeUser)