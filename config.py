
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

