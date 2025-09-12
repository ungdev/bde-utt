import os
from dotenv import load_dotenv

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
        allowed_hosts = self.get("ALLOWED_HOSTS", "").split(",")
        if not any(host.strip() for host in allowed_hosts):
            raise EnvVarNotSetError("ALLOWED_HOSTS")
        return allowed_hosts

    @property
    def ADMIN_URL(self) -> str:
        url = self.get("ADMIN_URL", "admin/")
        if not url.endswith("/"):
            url += "/"
        return url

    @property
    def SECRET_KEY(self) -> str:
        secret_key = self.get("SECRET_KEY", "")
        if not secret_key:
            raise EnvVarNotSetError("SECRET_KEY")
        return secret_key

    @property
    def SESSION_COOKIE_SECURE(self) -> bool:
        return self.get("SESSION_COOKIE_SECURE", "True") == "True"

    @property
    def CSRF_COOKIE_SECURE(self) -> bool:
        return self.get("CSRF_COOKIE_SECURE", "True") == "True"

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
        endpoint = self.get("OIDC_OP_AUTHORIZATION_ENDPOINT", "")
        if not endpoint:
            raise EnvVarNotSetError("OIDC_OP_AUTHORIZATION_ENDPOINT")
        return endpoint

    @property
    def OIDC_OP_TOKEN_ENDPOINT(self) -> str:
        endpoint = self.get("OIDC_OP_TOKEN_ENDPOINT", "")
        if not endpoint:
            raise EnvVarNotSetError("OIDC_OP_TOKEN_ENDPOINT")
        return endpoint

    @property
    def OIDC_OP_USER_ENDPOINT(self) -> str:
        endpoint = self.get("OIDC_OP_USER_ENDPOINT", "")
        if not endpoint:
            raise EnvVarNotSetError("OIDC_OP_USER_ENDPOINT")
        return endpoint

    @property
    def OIDC_OP_JWKS_ENDPOINT(self) -> str:
        endpoint = self.get("OIDC_OP_JWKS_ENDPOINT", "")
        if not endpoint:
            raise EnvVarNotSetError("OIDC_OP_JWKS_ENDPOINT")
        return endpoint

    @property
    def OIDC_RP_CLIENT_ID(self) -> str:
        id = self.get("OIDC_RP_CLIENT_ID", "")
        if not id:
            raise EnvVarNotSetError("OIDC_RP_CLIENT_ID")
        return id

    @property
    def OIDC_RP_CLIENT_SECRET(self) -> str:
        secret = self.get("OIDC_RP_CLIENT_SECRET", "")
        if not secret:
            raise EnvVarNotSetError("OIDC_RP_CLIENT_SECRET")
        return secret

    @property
    def OIDC_RP_SIGN_ALGO(self) -> str:
        algo = self.get("OIDC_RP_SIGN_ALGO", "")
        if not algo:
            raise EnvVarNotSetError("OIDC_RP_SIGN_ALGO")
        return algo

    @property
    def OIDC_RP_SCOPES(self) -> str:
        scopes = self.get("OIDC_RP_SCOPES", "")
        if not scopes:
            raise EnvVarNotSetError("OIDC_RP_SCOPES")
        return scopes
