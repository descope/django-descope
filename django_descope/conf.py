import os
from dataclasses import dataclass

from django.conf import settings as site_settings
from django.core.exceptions import ImproperlyConfigured


@dataclass(frozen=True)
class Settings:
    """
    Settings class for configuring Descope integration in a Django project.

    Methods:
        __getattribute__(name):
    """

    _PREFIX = "DESCOPE_"

    # renovate: datasource=npm packageName=@descope/web-component
    DESCOPE_WEB_COMPONENT_VERSION = "3.45.0"
    """ Version of the Descope web component. """

    DESCOPE_WEB_COMPONENT_SRC = (
        f"https://unpkg.com/@descope/web-component@{DESCOPE_WEB_COMPONENT_VERSION}/dist/index.js"  # noqa: E231
    )
    """ Source URL for the Descope web component. """

    DESCOPE_PROJECT_ID = os.environ.get("DESCOPE_PROJECT_ID")
    """ Project ID for Descope. Defaults to env, raises ImproperlyConfigured if not set."""

    DESCOPE_MANAGEMENT_KEY = os.environ.get("DESCOPE_MANAGEMENT_KEY")
    """ Management key for Descope. Defaults to env."""

    DESCOPE_IS_STAFF_ROLE = "is_staff"
    """ Role name for staff users in Descope. """
    DESCOPE_IS_SUPERUSER_ROLE = "is_superuser"
    """ Role name for superuser users in Descope. """

    DESCOPE_USERNAME_CLAIM = "sub"
    """
        JWT claim used for the username. Must be unique to avoid user merges
        or account takeovers.
        Ensure the claim used here is present in the JWT.
        Note: It is crucial to use a claim with a unique value for the username.
        Failure to do so may result in unintended user merges or account takeovers.
        For more information, refer to Descope's [NoAuth](https://www.descope.com/blog/post/noauth) blog post.
    """

    def __getattribute__(self, name):
        """
        Overrides the default __getattribute__ method to first check if the
        attribute exists in the site_settings module. If the attribute is found
        in site_settings, it returns the value of that attribute. Otherwise,
        it falls back to the default behavior of retrieving the attribute
        from the instance.

        Args:
            name (str): The name of the attribute to retrieve.

        Returns:
            Any: The value of the attribute from site_settings if it exists,
            otherwise the value from the instance.
        """

        if hasattr(site_settings, name):
            return getattr(site_settings, name)
        return super().__getattribute__(name)

    def validate(self):
        """
        Validates the settings for Descope integration in a Django project.

        Raises:
            ImproperlyConfigured: If the project ID is not set.
        """

        if not self.DESCOPE_PROJECT_ID:
            raise ImproperlyConfigured('"DESCOPE_PROJECT_ID" is required!')


settings = Settings()
settings.validate()
