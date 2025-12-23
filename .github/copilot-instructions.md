# Django Descope Integration Plugin

Django-descope is a Django plugin that integrates Descope authentication and user management platform with Django applications. The plugin provides middleware, authentication backends, template tags, and views for seamless integration with Descope's authentication flows.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap and Setup
- **Install Python dependencies**:
  ```bash
  poetry install --with dev
  ```
  - Installation takes ~90 seconds. Uses Poetry for consistent dependency management.
  - Note: django-stubs is only installed on Python >=3.10 due to version constraints.
  
- **Set required environment variables**:
  ```bash
  export DESCOPE_PROJECT_ID=P2ZRsmAQw8MKG78knGZ9GXWRqxM5  # Test project ID
  # export DESCOPE_MANAGEMENT_KEY=your_secret_key  # Required for full test suite
  ```

- **Initialize Django application**:
  ```bash
  poetry run python manage.py migrate  # ~0.6 seconds
  poetry run python manage.py check    # Validates Django configuration
  ```

### Development Workflow
- **Run development server**:
  ```bash
  export DESCOPE_PROJECT_ID=P2ZRsmAQw8MKG78knGZ9GXWRqxM5
  poetry run python manage.py runserver 0.0.0.0:8000
  ```
  - Server starts instantly and runs on port 8000
  - Access demo app at http://localhost:8000/
  - Admin interface at http://localhost:8000/admin/

### Testing
- **Run linting** (ALWAYS run before committing):
  ```bash
  poetry run flake8 django_descope/              # ~0.16 seconds
  poetry run black --check django_descope/       # ~0.25 seconds  
  poetry run isort --check-only django_descope/  # ~0.12 seconds
  ```
  - All linting is very fast (<1 second total)
  - CI will fail if linting doesn't pass

- **Run basic tests**:
  ```bash
  poetry run python manage.py test --exclude-tag=requires-management-key
  ```
  - Most tests require DESCOPE_MANAGEMENT_KEY (secret from CI)
  - Basic validation tests work without the management key

- **Run tests via tox** (full test matrix):
  ```bash
  poetry run tox -v  # Tests across Python 3.9-3.13 and Django 3.2-5.1
  ```
  - **NEVER CANCEL**: Full tox run can take 5-10 minutes. Set timeout to 15+ minutes.
  - Requires both DESCOPE_PROJECT_ID and DESCOPE_MANAGEMENT_KEY environment variables
  - **Note**: May fail due to network connectivity limitations in some environments

## Validation Scenarios
After making changes, always verify:

1. **Basic Django functionality**:
   ```bash
   poetry run python manage.py check
   poetry run python manage.py migrate  # if you added migrations
   ```

2. **Linting compliance**:
   ```bash
   poetry run black django_descope/ example_app/
   poetry run isort django_descope/ example_app/
   poetry run flake8 django_descope/
   ```

3. **Authentication flow** (manual testing):
   - Start development server
   - Visit http://localhost:8000/
   - Verify Descope authentication widget loads
   - Test login/logout flow if you have test credentials

4. **Admin integration**:
   - Visit http://localhost:8000/admin/
   - Verify custom Descope admin login template loads

## Common Development Tasks

### Repository Structure
```
.
├── django_descope/          # Main plugin package
│   ├── authentication.py    # Authentication backend
│   ├── middleware.py       # Descope middleware
│   ├── views.py           # Auth views
│   ├── templatetags/      # Django template tags
│   └── templates/         # HTML templates for auth
├── example_app/            # Demo/test application
│   ├── templates/         # Example templates
│   └── test_admin.py      # Integration tests
├── manage.py              # Django management script
├── settings.py           # Django settings with Descope config
├── pyproject.toml        # Poetry configuration
├── tox.ini              # Test matrix configuration
└── .github/workflows/    # CI/CD configuration
```

### Key Configuration Files
- **pyproject.toml**: Python dependencies and project metadata
- **settings.py**: Django settings with DESCOPE_PROJECT_ID configuration
- **tox.ini**: Test matrix across Python/Django versions
- **.pre-commit-config.yaml**: Git hooks for linting
- **.github/workflows/ci.yaml**: GitHub Actions CI configuration

### Environment Variables
```bash
# Required for basic functionality
DESCOPE_PROJECT_ID=P2ZRsmAQw8MKG78knGZ9GXWRqxM5  # Test project

# Required for full test suite (CI secret)
DESCOPE_MANAGEMENT_KEY=your_secret_key

# Optional Django settings
DEBUG=True
SECRET_KEY=your_secret_key
```

### Dependency Management
- **Primary**: Use `poetry install --with dev` for dependencies (consistent environments)
- **Note**: django-stubs requires Python >=3.10, handled via conditional installation
- **Lock file**: Keep poetry.lock updated with `poetry lock` when changing dependencies

### Testing Approach
- Unit tests in `django_descope/test_store_jwt.py`
- Integration tests in `example_app/test_admin.py`  
- Most tests require Descope management API access
- Use test project ID: `P2ZRsmAQw8MKG78knGZ9GXWRqxM5`
- Full test suite needs management key from CI secrets

### CI/CD Integration
- **GitHub Actions**: `.github/workflows/ci.yaml`
- **Test matrix**: Python 3.9-3.13 × Django 3.2-5.1
- **Required secrets**: DESCOPE_MANAGEMENT_KEY
- **Pre-commit hooks**: Automatic linting and formatting
- **Publishing**: Automated PyPI publication on release

## Troubleshooting

### Common Issues
1. **"DESCOPE_PROJECT_ID is required"** - Set the environment variable
2. **Poetry dependency conflicts** - Use pip instead of poetry
3. **Management key errors in tests** - Tests requiring API access need DESCOPE_MANAGEMENT_KEY
4. **Django check failures** - Ensure all required dependencies are installed
5. **Pre-commit hooks fail to install** - Network connectivity issues; use linting tools directly instead
6. **Tox fails with pip timeout** - Network connectivity limitations may prevent full test matrix execution

### Performance Notes
- **Dependency installation**: ~90 seconds for poetry install --with dev
- **Django operations**: All under 1 second (migrations: ~0.6s, check: instant, runserver: instant startup)
- **Linting tools**: All under 1 second (flake8: ~0.16s, black: ~0.25s, isort: ~0.12s)
- **Basic tests**: Under 1 second but require DESCOPE_MANAGEMENT_KEY for full functionality
- **Tox full test matrix**: 5-10 minutes when network allows - **NEVER CANCEL**
- No complex build steps or compilation required
- Development server starts instantly

### File Locations to Check
- Always check `django_descope/conf.py` when modifying settings
- Template changes go in `django_descope/templates/admin/`
- Authentication logic is in `django_descope/authentication.py`
- Middleware modifications in `django_descope/middleware.py`