import os
import logging
import json

# Si no lo tienes aún en tus requirements, añade:
# google-auth, google-auth-oauthlib, google-auth-httplib2, google-cloud-storage, etc.
from google.oauth2 import service_account
import google.auth


# Retrieve the API key from environment variables
API_KEY = os.environ.get('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY environment variable is not set")

# Storage path setting
LOCAL_STORAGE_PATH = os.environ.get('LOCAL_STORAGE_PATH', '/tmp')

# GCP environment variables (ahora opcional el JSON)
GCP_SA_CREDENTIALS = os.environ.get('GCP_SA_CREDENTIALS')  # puede quedar vacío
GCP_BUCKET_NAME = os.environ.get('GCP_BUCKET_NAME', '')


def validate_env_vars(provider):
    """
    Validate the necessary environment variables for the selected storage provider.
    Ahora GCP sólo exige GCP_BUCKET_NAME, no la credencial JSON.
    """
    required_vars = {
        'GCP': ['GCP_BUCKET_NAME'],
        'S3': ['S3_ENDPOINT_URL', 'S3_ACCESS_KEY', 'S3_SECRET_KEY', 'S3_BUCKET_NAME', 'S3_REGION'],
        'S3_DO': ['S3_ENDPOINT_URL', 'S3_ACCESS_KEY', 'S3_SECRET_KEY']
    }

    missing_vars = [var for var in required_vars.get(provider, []) if not os.getenv(var)]
    if missing_vars:
        raise ValueError(
            f"Missing environment variables for {provider} storage: {', '.join(missing_vars)}"
        )


def get_gcp_credentials():
    """
    Devuelve un objeto Credentials de GCP:
      - Si GCP_SA_CREDENTIALS está definido, parsea el JSON y crea la credencial.
      - En otro caso, usa las ADC exposadas por Cloud Run (Metadata Server).
    """
    if GCP_SA_CREDENTIALS:
        info = json.loads(GCP_SA_CREDENTIALS)
        return service_account.Credentials.from_service_account_info(info)

    # Application Default Credentials (ADC)
    creds, _ = google.auth.default()
    return creds
