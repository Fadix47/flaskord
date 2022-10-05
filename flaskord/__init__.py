from .flaskord import client
from .exceptions import UndefinedToken
from .oauth2 import oauth
from flask_sqlalchemy import SQLAlchemy


base_keys = sorted(['FLASKORD_CLIENT_ID', 'FLASKORD_CLIENT_SECRET', 'FLASKORD_TOKEN'])
oauth_keys = sorted(['FLASKORD_OAUTH_REDIRECT_URI', 'FLASKORD_OAUTH_SCOPE', 'SQLALCHEMY_DATABASE_URI'])

class Flaskord(object):
    def __init__(self, flaskapp = None):
        if flaskapp is not None:
            self.flask_keys = flaskapp.config

            if sorted(list(set(list(base_keys)) & set(list(flaskapp.config.keys())))) != base_keys:
                raise KeyError(f"Some flask app keys not found in project. Make sure you have set up app['FLASKORD_CLIENT_ID'], app['FLASKORD_CLIENT_SECRET'] and app['FLASKORD_TOKEN']")

            self.client = client(flaskapp.config["FLASKORD_TOKEN"])

            if "FLASKORD_OAUTH" in list(flaskapp.config.keys()):
                if sorted(list(set(list(oauth_keys)) & set(list(flaskapp.config.keys())))) != oauth_keys:
                    raise KeyError(f"Some flask app keys not found in project. Make sure you have set up app['FLASKORD_OAUTH_REDIRECT_URI'], app['FLASKORD_OAUTH_SCOPE'] and app['SQLALCHEMY_DATABASE_URI']")

                db = SQLAlchemy(flaskapp)

                class DiscordOauth2(db.Model):
                    id = db.Column(db.Integer, primary_key=True)
                    discord_id = db.Column(db.Integer, nullable=False)
                    discord_name = db.Column(db.String, nullable=False)

                    def __repr__(self):
                        return '<DiscordOauth2 %r>' % self.id

                self.oauth = oauth(self, db, DiscordOauth2)

                db.create_all()

        else:
            raise UndefinedToken("app is not set")
