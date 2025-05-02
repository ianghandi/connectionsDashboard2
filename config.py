import os

# OAuth Configuration
OAUTH_CONFIG = {
    "client_id": os.getenv("OAUTH_CLIENT_ID"),
    "authorization_endpoint": os.getenv("OAUTH_AUTHORIZATION_ENDPOINT"),
    "token_endpoint": os.getenv("OAUTH_TOKEN_ENDPOINT"),
    "redirect_uri": os.getenv("OAUTH_REDIRECT_URI"),
    "scopes": ["openid", "profile", "email"],
}

# Allowed AD Groups
ALLOWED_GROUPS = ["app_iam_admins", "app_iam_audit"]

# Environments Configuration
ENVIRONMENTS = {
    "Dev": {
        "url": os.getenv("PF_DEV_URL"),
        "username": os.getenv("PF_DEV_USERNAME"),
        "password": os.getenv("PF_DEV_PASSWORD")
    },
    "QA": {
        "url": os.getenv("PF_QA_URL"),
        "username": os.getenv("PF_QA_USERNAME"),
        "password": os.getenv("PF_QA_PASSWORD")
    },
    "Stage": {
        "url": os.getenv("PF_STAGE_URL"),
        "username": os.getenv("PF_STAGE_USERNAME"),
        "password": os.getenv("PF_STAGE_PASSWORD")
    },
    "Prod": {
        "url": os.getenv("PF_PROD_URL"),
        "username": os.getenv("PF_PROD_USERNAME"),
        "password": os.getenv("PF_PROD_PASSWORD")
    },
    "Sandbox": {
        "url": os.getenv("PF_SANDBOX_URL"),
        "username": os.getenv("PF_SANDBOX_USERNAME"),
        "password": os.getenv("PF_SANDBOX_PASSWORD")
    },

    # PingAccess Environments
    "PA-DEV": {
        "url": os.getenv("PA_DEV_URL"),
        "username": os.getenv("PA_DEV_USERNAME"),
        "password": os.getenv("PA_DEV_PASSWORD")
    },
    "PA-QA": {
        "url": os.getenv("PA_QA_URL"),
        "username": os.getenv("PA_QA_USERNAME"),
        "password": os.getenv("PA_QA_PASSWORD")
    },
    "PA-PROD": {
        "url": os.getenv("PA_PROD_URL"),
        "username": os.getenv("PA_PROD_USERNAME"),
        "password": os.getenv("PA_PROD_PASSWORD")
    }
}