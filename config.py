
# config.py

OAUTH_CONFIG = {
    "client_id": "dummy-client-id",
    "authorization_endpoint": "https://your-pingfederate-server.com/as/authorization.oauth2",
    "token_endpoint": "https://your-pingfederate-server.com/as/token.oauth2",
    "redirect_uri": "http://localhost:5000/callback",
    "scopes": ["openid", "profile", "email"],
}

ALLOWED_GROUPS = ["app_iam_admins", "app_iam_audit"]

ENVIRONMENTS = {
    "Dev": {
        "url": "https://pingfed-dev.example.com",
        "username": "admin-dev",
        "password": "password-dev"
    },
    "QA": {
        "url": "https://pingfed-qa.example.com",
        "username": "admin-qa",
        "password": "password-qa"
    },
    "Stage": {
        "url": "https://pingfed-stage.example.com",
        "username": "admin-stage",
        "password": "password-stage"
    },
    "Prod": {
        "url": "https://pingfed-prod.example.com",
        "username": "admin-prod",
        "password": "password-prod"
    },
    "Sandbox": {
        "url": "https://pingfed-sandbox.example.com",
        "username": "admin-sandbox",
        "password": "password-sandbox"
    },

    # New PingAccess Environments
    "PA-DEV": {
        "url": "https://pingaccess-dev.example.com",
        "username": "admin-pa-dev",
        "password": "password-pa-dev"
    },
    "PA-QA": {
        "url": "https://pingaccess-qa.example.com",
        "username": "admin-pa-qa",
        "password": "password-pa-qa"
    },
    "PA-PROD": {
        "url": "https://pingaccess-prod.example.com",
        "username": "admin-pa-prod",
        "password": "password-pa-prod"
    }
}

'''
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

.env file below

OAUTH_CLIENT_ID=your-client-id
OAUTH_AUTHORIZATION_ENDPOINT=https://yourserver/as/authorization.oauth2
OAUTH_TOKEN_ENDPOINT=https://yourserver/as/token.oauth2
OAUTH_REDIRECT_URI=http://localhost:5000/callback

PF_DEV_URL=https://pingfed-dev.example.com
PF_DEV_USERNAME=admin-dev
PF_DEV_PASSWORD=SuperSecretDevPassword

PA_DEV_URL=https://pingaccess-dev.example.com
PA_DEV_USERNAME=admin-pa-dev
PA_DEV_PASSWORD=SuperSecretPADPassword

