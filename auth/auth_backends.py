from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class CustomOIDCBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super().create_user(claims)

        name = claims.get("name", user.username)

        user.username = claims.get("preferred_username", user.username)
        user.first_name = name.split(" ")[0] if " " in name else name
        user.last_name = " ".join(name.split(" ")[1:]) if " " in name else ""
        user.email = claims.get("email", "")
        user.save()

        return user

    def update_user(self, user, claims):
        name = claims.get("name", user.username)

        user.username = claims.get("preferred_username", user.username)
        user.first_name = name.split(" ")[0] if " " in name else name
        user.last_name = " ".join(name.split(" ")[1:]) if " " in name else ""
        user.email = claims.get("email", "")
        user.save()

        return user
