# Descope Django App

Descope is a user management and authentication platform.
This plugin integrates Descope with your Django app.

## Quick start

1. Sign up for Descope

- Get your project id and set in settings (see below)
- Create two roles in Descope, that will be mapped to Django permissions, create a user and add these roles to your user
  - is_staff
  - is_superuser

1. Add "django_descope" to your INSTALLED_APPS setting like this:

```
   INSTALLED_APPS = [
   ...
   'django_descope',
   ]
```

1. Add Descope Middleware **after** the SessionMiddleware

```
   MIDDLEWARE = [
   ...
   'django.contrib.sessions.middleware.SessionMiddleware',
   ...
   'django_descope.middleware.DescopeMiddleware',
   ]
```

1. Include descope URLconf in your project urls.py like this:

```
   path('descope/', include('django_descope.urls')),
```

1. Start the development server and visit http://127.0.0.1:8000/descope/signup

1. Visit http://127.0.0.1:8000/tokens to see the user tokens after login

## Settings

The following settings are available to configure in your project `settings.py`

```
DESCOPE_PROJECT_ID **Required**
DESCOPE_REQUIRE_SIGNUP - Set this to true to create user on first login
DESCOPE_LOGIN_SENT_REDIRECT
DESCOPE_LOGIN_SUCCESS_REDIRECT
DESCOPE_LOGIN_TEMPLATE_NAME
DESCOPE_LOGIN_SENT_TEMPLATE_NAME
DESCOPE_LOGIN_FAILED_TEMPLATE_NAME
DESCOPE_SIGNUP_TEMPLATE_NAME
```

### TODO:

- [ ] Add additional authentication methods
- [ ] Add flows support
