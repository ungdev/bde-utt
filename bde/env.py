import os
from dotenv import load_dotenv
import secrets

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))


class EnvVarNotSetError(Exception):
    """Raised when a required environment variable is not set."""

    def __init__(self, var_name: str):
        super().__init__(f"{var_name} is not set in environment variables")
        self.var_name = var_name


class EnvConfig:
    """
    Object-oriented access to environment variables loaded from .env.
    Example:
        env = EnvConfig()
        admin_url = env.ADMIN_URL
    """

    def __init__(self):
        # Optionally, you can cache values here
        pass

    def get(self, key: str, default: str) -> str:
        return os.environ.get(key, default)

    @property
    def DEBUG(self) -> bool:
        return self.get("DEBUG", "False") == "True"

    @property
    def ALLOWED_HOSTS(self) -> list:
        return self.get("ALLOWED_HOSTS", "").split(",")

    @property
    def CSRF_TRUSTED_ORIGINS(self) -> list:
        origins = self.get("CSRF_TRUSTED_ORIGINS", "").split(",")
        return origins if origins[0] != "" else []

    @property
    def CSRF_COOKIE_SECURE(self) -> bool:
        return self.get("CSRF_COOKIE_SECURE", "True") == "True"

    @property
    def DEV_MODE(self) -> bool:
        return self.get("DEV_MODE", "False") == "True"

    @property
    def SESSION_COOKIE_SECURE(self) -> bool:
        return self.get("SESSION_COOKIE_SECURE", "True") == "True"

    @property
    def ADMIN_URL(self) -> str:
        url = self.get("ADMIN_URL", "admin/")
        if not url.endswith("/"):
            url += "/"
        return url

    @property
    def SECRET_KEY(self) -> str:
        return self.get("SECRET_KEY", secrets.token_urlsafe(42))

    @property
    def DB_NAME(self) -> str:
        return self.get("DB_NAME", "bde")

    @property
    def DB_USER(self) -> str:
        return self.get("DB_USER", "bde")

    @property
    def DB_PASSWORD(self) -> str:
        return self.get("DB_PASSWORD", "bde")

    @property
    def DB_HOST(self) -> str:
        return self.get("DB_HOST", "localhost")

    @property
    def DB_PORT(self) -> str:
        return self.get("DB_PORT", "3006")

    @property
    def OIDC_OP_AUTHORIZATION_ENDPOINT(self) -> str:
        return self.get("OIDC_OP_AUTHORIZATION_ENDPOINT", "")

    @property
    def OIDC_OP_TOKEN_ENDPOINT(self) -> str:
        return self.get("OIDC_OP_TOKEN_ENDPOINT", "")

    @property
    def OIDC_OP_USER_ENDPOINT(self) -> str:
        return self.get("OIDC_OP_USER_ENDPOINT", "")

    @property
    def OIDC_OP_JWKS_ENDPOINT(self) -> str:
        return self.get("OIDC_OP_JWKS_ENDPOINT", "")

    @property
    def OIDC_RP_CLIENT_ID(self) -> str:
        return self.get("OIDC_RP_CLIENT_ID", "")

    @property
    def OIDC_RP_CLIENT_SECRET(self) -> str:
        return self.get("OIDC_RP_CLIENT_SECRET", "")

    @property
    def OIDC_RP_SIGN_ALGO(self) -> str:
        return self.get("OIDC_RP_SIGN_ALGO", "")

    @property
    def OIDC_RP_SCOPES(self) -> str:
        return self.get("OIDC_RP_SCOPES", "")

    @property
    def OIDC_SUPERUSER_GROUP(self) -> str:
        return self.get("OIDC_SUPERUSER_GROUP", "")

    @property
    def OIDC_EDITOR_GROUP(self) -> str:
        return self.get("OIDC_EDITOR_GROUP", "")

    @property
    def OIDC_EDITOR_DJANGO_GROUP(self) -> str:
        return self.get("OIDC_EDITOR_DJANGO_GROUP", "")
