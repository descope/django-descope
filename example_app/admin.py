from django.contrib import admin

descope_admin_site = admin.site

# override the login template with our own
descope_admin_site.login_template = "admin_login.html"
