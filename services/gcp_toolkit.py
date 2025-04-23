diff --git a/services/gcp_toolkit.py b/services/gcp_toolkit.py
index abc1234..def5678 100644
--- a/services/gcp_toolkit.py
+++ b/services/gcp_toolkit.py
@@ -1,7 +1,9 @@
 import os
-import json
+import json
 import logging
 from google.oauth2 import service_account
+import google.auth
 from google.cloud import storage
 
 # Configure logging
@@ -12,20 +14,42 @@ logger = logging.getLogger(__name__)
 
 # GCS environment variables
 GCP_BUCKET_NAME = os.getenv('GCP_BUCKET_NAME')
-STORAGE_PATH = "/tmp/"
+STORAGE_PATH = "/tmp/"
 
 gcs_client = None
 
-def initialize_gcp_client():
-
-    GCP_SA_CREDENTIALS = os.getenv('GCP_SA_CREDENTIALS')
-
-    if not GCP_SA_CREDENTIALS:
-        #logger.warning("GCP credentials not found. Skipping GCS client initialization.")
-        return None  # Skip client initialization if credentials are missing
-
-    # Define the required scopes for Google Cloud Storage
-    GCS_SCOPES = ['https://www.googleapis.com/auth/devstorage.full_control']
-
-    try:
-        credentials_info = json.loads(GCP_SA_CREDENTIALS)
-        gcs_credentials = service_account.Credentials.from_service_account_info(
-            credentials_info,
-            scopes=GCS_SCOPES
-        )
-        return storage.Client(credentials=gcs_credentials)
-    except Exception as e:
-        logger.error(f"Failed to initialize GCS client: {e}")
-        return None
+def initialize_gcp_client():
+    """
+    Inicializa el cliente GCS:
+      - Si existe GCP_SA_CREDENTIALS con JSON, lo parsea y crea la credencial.
+      - En otro caso, usa Application Default Credentials (ADC).
+    """
+    # Scopes necesarios para GCS
+    GCS_SCOPES = ['https://www.googleapis.com/auth/devstorage.full_control']
+
+    creds = None
+    sa_json = os.getenv('GCP_SA_CREDENTIALS')
+
+    if sa_json:
+        try:
+            info = json.loads(sa_json)
+            creds = service_account.Credentials.from_service_account_info(info, scopes=GCS_SCOPES)
+        except Exception as e:
+            logger.error(f"Error cargando credenciales de Service Account JSON: {e}")
+    else:
+        # Si no hay JSON, usar ADC (ej. Metadata Server de Cloud Run)
+        try:
+            creds, _ = google.auth.default(scopes=GCS_SCOPES)
+        except Exception as e:
+            logger.error(f"Error obteniendo ADC de GCP: {e}")
+
+    if not creds:
+        logger.error("No se obtuvieron credenciales GCP; el cliente GCS no será inicializado.")
+        return None
+
+    return storage.Client(credentials=creds)
 
 # Initialize the GCS client
 gcs_client = initialize_gcp_client()
