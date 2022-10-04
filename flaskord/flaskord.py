import requests
import json
from .exceptions import *
from typing import Union

# Read https://discord.com/developers/docs/resources/guild

discord_api_base = "https://discordapp.com/api/v9"
discord_api_authorize = discord_api_base + "/oauth2/authorize"
discord_api_token = discord_api_base + "/oauth2/token"

class Flaskcord:
    def __init__(self, token: str = None):
        if token:
            self.headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                "authorization": f"Bot {token}",
                "intents": "GUILD_MEMBERS"
            }
        else:
            raise UndefinedToken("Token is not set")

    def __run__(self, route, method, payload=None):
        route = discord_api_base + route
        resp = requests.request(method, route, headers=self.headers) if payload is None else requests.request(method, route, data=json.dumps(payload), headers=self.headers)

        if resp.status_code == 401:
            raise Unauthorized("Token incorrect")

        elif resp.status_code == 429:
            raise RateLimited(resp.json(), resp.headers)

        else:
            return resp.json()


    # base methods

    def get_user(self, # get basic user information
                 user_id: Union[str, int]) -> dict:

        resp =  self.__run__(route=f"/users/{user_id}", method="GET")
        avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{resp['avatar']}.png?size=512"
        resp["avatar_url"] = avatar
        return resp


    def fetch_member(self, # fetching user on guild
                     guild_id: Union[str, int],
                     user_id: Union[str, int]) -> dict:

        resp = self.__run__(route=f"/guilds/{guild_id}/members/{user_id}", method="GET")
        avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{resp['avatar']}.png?size=512"
        resp["avatar_url"] = avatar
        return resp


    def get_guild(self, # get basic information about guild
                  guild_id: Union[str, int]) -> dict:

        resp = self.__run__(route=f"/guilds/{guild_id}?with_counts=true", method='GET')
        resp["member_count"] = resp["approximate_member_count"]
        return resp

    # advanced methods

    def send(self, payload: Union[dict, str], # sends message in user DM or in channel
             channel_id: Union[str, int] = None,
             user_id: Union[str, int] = None):

        if channel_id or user_id:
            channel_id = self.__run__(route="/users/@me/channels", method="POST", payload={"recipients": [int(user_id)]})["id"] if user_id else channel_id

            payload = {"content": payload} if not isinstance(payload, dict) else payload
            return self.__run__(route=f"/channels/{channel_id}/messages", method="POST", payload=payload)
        else:
            return HttpException("user_id or channel_id must be set")


    def add_roles(self, # add roles for user on guild (easier method than edit_member)
                  guild_id: Union[str, int],
                  user_id: Union[str, int],
                  role_id: Union[str, int]):

        role_id = str(role_id)
        try:
            roles = self.fetch_member(guild_id, user_id)["roles"]

            if role_id not in roles: roles.append(role_id)

            payload = {"roles": roles}

            return self.__run__(route=f"/guilds/{guild_id}/members/{user_id}", method="PATCH", payload=payload)
        except KeyError:
            return HttpException("Member not found")


    def remove_roles(self, # remove roles for user on guild (easier method than edit_member)
                     guild_id: Union[str, int],
                     user_id: Union[str, int],
                     role_id: Union[str, int]):

        role_id = str(role_id)
        try:
            roles = self.fetch_member(guild_id, user_id)["roles"]
            if role_id in roles: roles.remove(role_id)
            payload = {"roles": roles}

            return self.__run__(route=f"/guilds/{guild_id}/members/{user_id}", method="PATCH", payload=payload)

        except KeyError:
            return HttpException("Member not found")


    def create_channel(self,
                       guild_id: Union[str, int],
                       channel: dict):

        return self.__run__(route=f"/guilds/{guild_id}/channels", method="POST", payload=channel)


    def delete_channel(self,
                    guild_id: Union[str, int],
                    channel_id: Union[str, int]):

        return self.__run__(route=f'/guilds/{guild_id}/channels/{channel_id}', method='DELETE')


    def edit_channel(self,
                     guild_id: Union[str, int],
                     channel_id: Union[str, int],
                     payload: dict):

        return self.__run__(route = f"/channels/{channel_id}", method="PATCH", payload=payload)


    def create_role(self,
                    guild_id: Union[str, int],
                    role: dict):

        return self.__run__(route=f'/guilds/{guild_id}/roles', method="POST", payload=role)


    def delete_role(self,
                    guild_id: Union[str, int],
                    role_id: Union[str, int]):

        return self.__run__(route=f'/guilds/{guild_id}/roles/{role_id}', method='DELETE')


    def edit_role(self,
                  guild_id: Union[str, int],
                  role_id: Union[str, int],
                  payload: dict):

        return self.__run__(route=f'/guilds/{guild_id}/roles/{role_id}', method="PATCH", payload=payload)


    def kick_member(self,
                    guild_id: Union[str, int],
                    user_id: Union[str, int]):

        return self.__run__(route=f'/guilds{guild_id}/members/{user_id}', method="DELETE")


    def ban_member(self,
                   guild_id: Union[str, int],
                   user_id: Union[str, int]):

        return self.__run__(route=f'/guilds/{guild_id}/bans/{user_id}', method='PUT')


    def unban_member(self,
                   guild_id: Union[str, int],
                   user_id: Union[str, int]):

        return self.__run__(route=f'/guilds/{guild_id}/bans/{user_id}', method='DELETE')


    def edit_member(self,
                    guild_id: Union[str, int],
                    user_id: Union[str, int],
                    payload: dict):

        return self.__run__(route=f"/guilds/{guild_id}/members/{user_id}", method="PATCH", payload=payload)
