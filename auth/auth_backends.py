import logging

from mozilla_django_oidc.auth import (  # type: ignore[import-untyped]
    OIDCAuthenticationBackend,
)


logger = logging.getLogger(__name__)


class CustomOIDCBackend(OIDCAuthenticationBackend):

    @staticmethod
    def _claims_context(claims):
        return {
            "sub": claims.get("sub"),
            "preferred_username": claims.get("preferred_username"),
            "email": claims.get("email"),
            "name": claims.get("name"),
        }

    def create_user(self, claims):
        logger.debug("OIDC create_user start: %s", self._claims_context(claims))
        try:
            user = super().create_user(claims)

            name = claims.get("name", user.username)

            user.username = claims.get("preferred_username", user.username)
            user.first_name = name.split(" ")[0] if " " in name else name
            user.last_name = " ".join(name.split(" ")[1:]) if " " in name else ""
            user.email = claims.get("email", "")
            user.save()

            logger.info("OIDC create_user success for username=%s", user.username)
            return user
        except Exception:
            logger.exception(
                "OIDC create_user failed: %s", self._claims_context(claims)
            )
            raise

    def update_user(self, user, claims):
        logger.debug(
            "OIDC update_user start for username=%s claims=%s",
            user.username,
            self._claims_context(claims),
        )
        try:
            name = claims.get("name", user.username)

            user.username = claims.get("preferred_username", user.username)
            user.first_name = name.split(" ")[0] if " " in name else name
            user.last_name = " ".join(name.split(" ")[1:]) if " " in name else ""
            user.email = claims.get("email", "")
            user.save()

            logger.info("OIDC update_user success for username=%s", user.username)
            return user
        except Exception:
            logger.exception(
                "OIDC update_user failed for username=%s claims=%s",
                user.username,
                self._claims_context(claims),
            )
            raise
