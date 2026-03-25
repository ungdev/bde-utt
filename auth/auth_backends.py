# You're lucky, I added some comments to this file to explain the custom logic.
# Maybe because it's not trivial (that's the least we can say...)
# So, have a good read !
# Arthur

# Some imports (trivial for now)
import logging

from django.conf import settings
from django.contrib.auth.models import Group
from mozilla_django_oidc.auth import (  # type: ignore[import-untyped]
    OIDCAuthenticationBackend,
)


logger = logging.getLogger(__name__)


class CustomOIDCBackend(OIDCAuthenticationBackend):

    # Normalize the groups claim so downstream checks always work on a list[str].
    @staticmethod
    def _extract_groups(claims):
        groups = claims.get("groups", [])
        if isinstance(groups, str):
            return [groups]
        if isinstance(groups, list):
            return [str(group) for group in groups]
        logger.warning("OIDC claims 'groups' has unsupported type: %s", type(groups))
        return []

    # Synchronize Django access flags and group membership from OIDC claims.
    # Rules:
    # - superuser comes only from OIDC_SUPERUSER_GROUP
    # - staff comes from superuser OR editor OIDC group
    # - editor Django group membership mirrors editor OIDC group presence
    def _sync_oidc_access(self, user, claims):
        oidc_groups = self._extract_groups(claims)

        # Names are configured through environment-backed Django settings.
        superuser_group = getattr(settings, "OIDC_SUPERUSER_GROUP", "")
        editor_group = getattr(settings, "OIDC_EDITOR_GROUP", "")
        editor_django_group_name = getattr(settings, "OIDC_EDITOR_DJANGO_GROUP", "")

        is_superuser_from_oidc = (
            bool(superuser_group) and superuser_group in oidc_groups
        )
        has_editor_from_oidc = bool(editor_group) and editor_group in oidc_groups

        if not superuser_group:
            logger.warning(
                "OIDC_SUPERUSER_GROUP is not configured; superuser flag will be removed"
            )

        # Keep Django privilege flags aligned with OIDC source of truth.
        user.is_superuser = is_superuser_from_oidc
        user.is_staff = is_superuser_from_oidc or has_editor_from_oidc

        if not editor_django_group_name:
            logger.warning(
                "OIDC_EDITOR_DJANGO_GROUP is not configured; cannot grant editor group"
            )
            return

        try:
            django_editor_group = Group.objects.get(name=editor_django_group_name)
        except Group.DoesNotExist:
            logger.warning(
                "Configured Django editor group '%s' does not exist",
                editor_django_group_name,
            )
            return

        if not editor_group:
            logger.warning(
                "OIDC_EDITOR_GROUP is not configured; removing editor Django group"
            )

        # Add or remove the editor Django group on every login to avoid drift.
        if has_editor_from_oidc:
            user.groups.add(django_editor_group)
        else:
            user.groups.remove(django_editor_group)

    # First login path: create local user, then apply profile and access sync.
    def create_user(self, claims):
        logger.debug("OIDC create_user start: %s", self._claims_context(claims))
        try:
            user = super().create_user(claims)

            name = claims.get("name", user.username)

        # Sync identity fields from OIDC claims.
        user.username = claims.get("preferred_username", user.username)
        user.first_name = name.split(" ")[0] if " " in name else name
        user.last_name = " ".join(name.split(" ")[1:]) if " " in name else ""
        user.email = claims.get("email", "")
        self._sync_oidc_access(user, claims)
        user.save()

            logger.info("OIDC create_user success for username=%s", user.username)
            return user
        except Exception:
            logger.exception(
                "OIDC create_user failed: %s", self._claims_context(claims)
            )
            raise

    # Subsequent logins: refresh profile and access rules from OIDC.
    def update_user(self, user, claims):
        logger.debug(
            "OIDC update_user start for username=%s claims=%s",
            user.username,
            self._claims_context(claims),
        )
        try:
            name = claims.get("name", user.username)

        # Sync identity fields from OIDC claims.
        user.username = claims.get("preferred_username", user.username)
        user.first_name = name.split(" ")[0] if " " in name else name
        user.last_name = " ".join(name.split(" ")[1:]) if " " in name else ""
        user.email = claims.get("email", "")
        self._sync_oidc_access(user, claims)
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
