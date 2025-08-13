from __future__ import annotations

from flask import current_app, redirect, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token

from ..extensions import oauth, db
from ..models import User


class GoogleLoginResource(Resource):
    def get(self):
        if not oauth._clients.get("google"):
            return {"message": "Google OAuth not configured"}, 501
        redirect_uri = current_app.config.get("OAUTH_REDIRECT_URI") or request.host_url.rstrip("/") + "/oauth/callback/google"
        return oauth.google.authorize_redirect(redirect_uri)


class GoogleCallbackResource(Resource):
    endpoint = "googlecallbackresource"

    def get(self):
        if not oauth._clients.get("google"):
            return {"message": "Google OAuth not configured"}, 501
        token = oauth.google.authorize_access_token()
        # Try OIDC id_token first, fall back to userinfo endpoint
        user_info = oauth.google.parse_id_token(token)
        if not user_info:
            resp = oauth.google.get("userinfo")
            user_info = resp.json() if resp else None
        if not user_info:
            return {"message": "Failed to retrieve user info"}, 400

        email = (user_info.get("email") or "").lower()
        sub = user_info.get("sub") or user_info.get("id")
        name = user_info.get("name") or email.split("@")[0]
        if not email:
            return {"message": "Email not available from provider"}, 400

        user = None
        if sub:
            user = User.query.filter_by(auth_provider="google", auth_provider_sub=sub).first()
        if not user:
            user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email, name=name, auth_provider="google", auth_provider_sub=sub)
            db.session.add(user)
        else:
            user.auth_provider = user.auth_provider or "google"
            user.auth_provider_sub = user.auth_provider_sub or sub
        db.session.commit()

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {"id": user.id, "email": user.email, "name": user.name},
        }, 200