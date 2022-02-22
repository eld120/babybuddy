import os
import sys
from pathlib import Path


from django.core.wsgi import get_wsgi_application

from dotenv import load_dotenv, find_dotenv

# Environment variables
# Check for and load environment variables from a .env file.
load_dotenv(find_dotenv())


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
sys.path.append(str(BASE_DIR / "babybuddy"))
# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.production"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")

application = get_wsgi_application()
