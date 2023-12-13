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

2. Install "django-descope" and add to your INSTALLED_APPS setting like this:

```bash
poetry add django-descope
OR
pip install django-descope
```

```
   INSTALLED_APPS = [
   ...
   'django_descope',
   ]
```

3. Add Descope Middleware **after** the AuthenticationMiddleware and SessionMiddleware

```
   MIDDLEWARE = [
   ...
   'django.contrib.sessions.middleware.SessionMiddleware',
   'django.contrib.auth.middleware.AuthenticationMiddleware',
   ...
   'django_descope.middleware.DescopeMiddleware',
   ]
```

4. Include descope URLconf in your project urls.py like this:

```
   path('auth/', include('django_descope.urls')),
```

5. In your site templates, insert the `descope_flow` tag where you want to place your flow

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

6. Start the development server and visit the newly created view

## Testing

See [test_admin.py](example_app/test_admin.py) for a rudimentary example of
how to utilize [Descope Test Users](https://docs.descope.com/manage/testusers/)
when testing your application with authenticated users.
You can use the helper [`django_descope.authentication.add_tokens_to_request`](django_descope/authentication.py) to add the tokens to the django session

> [!IMPORTANT]
> Remember you must create the relevant roles in [Descope Console](https://app.descope.com)
> so you can utilize them in your testing.

## Settings

The following settings are available to configure in your project `settings.py`

#### Required

```
DESCOPE_PROJECT_ID
```

#### Optional

```
DESCOPE_MANAGEMENT_KEY
DESCOPE_IS_STAFF_ROLE
DESCOPE_IS_SUPERUSER_ROLE
```
