from pathlib import Path
from bde.env import EnvConfig

env = EnvConfig()


def get_robots_content() -> str:

    if env.DEV_MODE:
        return "User-Agent: *\nDisallow: /\nSitemap: /sitemap.xml\n"

    return (
        f"User-agent: *\n"
        f"Disallow: /{env.ADMIN_URL}\n"
        "Disallow: /logout/\n"
        "Disallow: /redirect/\n"
        "Disallow: /sso/\n"
        "Disallow: /uploads/\n"
        "Sitemap: /sitemap.xml\n"
    )


BASE_DIR = Path(__file__).resolve().parent.parent
STATICFILES_DIR = BASE_DIR / "staticfiles"
STATICFILES_DIR.mkdir(exist_ok=True)

robots_path = STATICFILES_DIR / "robots.txt"
with open(robots_path, "w") as f:
    f.write(get_robots_content())

print(f"robots.txt généré dans {robots_path}")
