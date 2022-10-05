from requests_oauthlib import OAuth2Session
from flask import request
from .exceptions import *
import requests

discord_api_base = "https://discordapp.com/api/v9"
discord_api_authorize = discord_api_base + "/oauth2/authorize"
discord_api_token = discord_api_base + "/oauth2/token"
discord_api_users = discord_api_base + "/users/@me"

class oauth:
    def __init__(self, flaskapp, db, DiscordOauth2):
        self.client_id = flaskapp.flask_keys["FLASKORD_CLIENT_ID"]
        self.client_secret = flaskapp.flask_keys["FLASKORD_CLIENT_SECRET"]
        self.redirect_uri = flaskapp.flask_keys["FLASKORD_OAUTH_REDIRECT_URI"]
        self.scope = flaskapp.flask_keys["FLASKORD_OAUTH_SCOPE"]
        self.db = db
        self.DiscordOauth2 = DiscordOauth2

    def get_login_url(self) -> str:
        oauth = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri, scope=self.scope)
        login_url, state = oauth.authorization_url(discord_api_authorize)
        return login_url

    def confirm_login(self) -> dict:
        payload = {
           "client_id": self.client_id,
           "client_secret": self.client_secret,
           "grant_type": "authorization_code",
           "code": request.args.get("code"),
           "redirect_uri": self.redirect_uri,
           "scope": self.scope
        }

        try:
            access_token = requests.post(url = discord_api_token, data = payload).json()["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}

            user = requests.get(url = discord_api_users, headers = headers).json()

            if not self.DiscordOauth2.query.filter_by(discord_id=user["id"]).first(): # check if user already registered
                self.db.session.add(self.DiscordOauth2(discord_id=user["id"], discord_name=f'{user["username"]}#{user["discriminator"]}'))
                self.db.session.commit()

            return user
        except KeyError:
            return None
