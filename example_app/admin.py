from django_descope.models import DescopeUser
from django.shortcuts import render
from django.contrib import admin
from django.urls import path


class MyAdminSite(admin.AdminSite):
    login_template = 'admin_login.html'


descope_admin_site = MyAdminSite()
descope_admin_site.register(DescopeUser)