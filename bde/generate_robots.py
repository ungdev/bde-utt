from pathlib import Path
from bde.env import EnvConfig

env = EnvConfig()


def get_robots_content() -> str:

    if env.DEV_MODE:
        return "User-Agent: *\nDisallow: /"

    return f"""User-agent: *
    Disallow: /{env.ADMIN_URL}
    Disallow: /logout/
    Disallow: /redirect/
    Disallow: /sso/
    Disallow: /uploads/
    """


BASE_DIR = Path(__file__).resolve().parent.parent
STATICFILES_DIR = BASE_DIR / ("staticfiles" if not env.DEBUG else "static")
STATICFILES_DIR.mkdir(exist_ok=True)

robots_path = STATICFILES_DIR / "robots.txt"
with open(robots_path, "w") as f:
    f.write(get_robots_content())

print(f"robots.txt généré dans {robots_path}")
