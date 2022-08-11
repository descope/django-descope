=====
Descope Django App
=====

Descope is a user management and authentication platform.
This plugin integrates Descope with your Django app.

## Quick start

1. Add "django_descope" to your INSTALLED_APPS setting like this::

   INSTALLED_APPS = [
   ...
   'django_descope',
   ]

1. Add Descope Middleware **after** the SessionMiddleware

   MIDDLEWARE = [
   ...
   'django.contrib.sessions.middleware.SessionMiddleware',
   ...
   'django_descope.middleware.DescopeMiddleware',
   ]

1. Include the polls URLconf in your project urls.py like this::

   path('descope/', include('django_descope.urls')),

1. Start the development server and visit http://127.0.0.1:8000/descope/signup

1. Visit http://127.0.0.1:8000/tokens to see the user tokens after login

### TODO:

- [ ] Get user details (name?) from jwt
- [ ] Get user permissions from claims
