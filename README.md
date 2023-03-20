# Descope Django App

Descope is a user management and authentication platform.
This plugin integrates Descope with your Django app.

## Quick start

1. Sign up for Descope and set admin roles

- Get your project id
- Create two roles in Descope, that will be mapped to Django permissions
  - is_staff
  - is_superuser

Map these roles to any user you would like to make a staff or superuser in your Django app.
_The names of these roles can be customized in the settings below._

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
   path('auth/', include('django_descope.urls')),
```

1. In your site templates, insert the `descope_flow` tag where you want to place your flow

```html
{% load descope %}
<!-- load the descope registry -->

{% if user.is_authenticated %}
<h1>Welcome {{ user.email }} you are logged in!</h1>
<p><a href="{% url 'logout' %}">Log Out</a></p>
{% else %} {% descope_flow "sign-up-or-in" "/" %}
<!-- provide the descope flow id, and where to redirect after a successful login-->
{% endif %}
```

2. Start the development server and visit http://127.0.0.1:8000/auth/signup

3. Visit http://127.0.0.1:8000/auth/tokens to see the user tokens after login

## Settings

The following settings are available to configure in your project `settings.py`

```
DESCOPE_PROJECT_ID **Required**
DESCOPE_IS_STAFF_ROLE
DESCOPE_IS_SUPERUSER_ROLE
```
