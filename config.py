
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
        "url": "https://ping-dev.example.com",
        "username": "dev-admin",
        "password": "dev-password"
    },
    "QA": {
        "url": "https://ping-qa.example.com",
        "username": "qa-admin",
        "password": "qa-password"
    },
    "Stage": {
        "url": "https://ping-stage.example.com",
        "username": "stage-admin",
        "password": "stage-password"
    },
    "Prod": {
        "url": "https://ping-prod.example.com",
        "username": "prod-admin",
        "password": "prod-password"
    },
    "Sandbox": {
        "url": "https://ping-sandbox.example.com",
        "username": "sandbox-admin",
        "password": "sandbox-password"
    }
}
