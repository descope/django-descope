from django_descope.models import DescopeUser
from django.shortcuts import render
from django.contrib import admin
from django.urls import path


class MyAdminSite(admin.AdminSite):
    login_template = 'admin_login.html'

    def custom_page(self, request):
        context = {}
        return render(request, "admin_staff.html", context)

    def get_urls(self):
        return [ 
            path( "staff/", self.admin_view(self.custom_page), name="staff"),
        ] + super().get_urls()


descope_admin_site = MyAdminSite()
descope_admin_site.register(DescopeUser)