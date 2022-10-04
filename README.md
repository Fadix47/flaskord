# flaskord
Simple discord API-requester. Especially cool with flask, but you can use it anywhere

How to install 

```
pip install flaskord
```

# Parameters

|           Name             |                     Type                     |Default|                           Information                               |
|:-------------------------:|:-------------------------------------------:|:----------:|:-------------------------------------------------------------------:|
|           token             | `str` |   `None`     |    The token of your bot application          |

# Methods

### Do not forget to read https://discord.com/developers/docs/

|    Method      |             Arguments         | Return |   Information   |
|:--------------:|:-----------------------------:|:------:|:---------------:|
|   get_user    |  user_id: `Union[str, int]` |  `dict`  |  Return basic information about user (not include guild)   |
|   fetch_member  | guild_id: `Union[str, int]`, user_id: `Union[str, int]` | `dict` | Return full information about user (include guild) |
| get_guild | guild_id: `Union[str, int]` | `dict` | Return full information about guild |
| send | payload: `Union[dict, str]`, <channel_id>: `Union[str, int]`, <user_id>: `Union[str, int]` | `None` | Send message in channel or in user DM. |
| add_roles | guild_id: `Union[str, int]`, user_id: `Union[str, int]`, role_id: `Union[str, int]` | `None` | Add role to guild member |
| remove_roles | guild_id: `Union[str, int]`, user_id: `Union[str, int]`, role_id: `Union[str, int]` | `None` | Remove role from guild member |

| create_channel | guild_id: `Union[str, int]`, channel: `dict` | `None` | Creates channel by `channel` settings on guild|
| delete_channel | guild_id: `Union[str, int]`, channel_id: `Union[str, int]` | `None` | Remove channel from guild |
| edit_channel | guild_id: `Union[str, int]`, channel_id: `Union[str, int]`, payload: `dict` | `None` | Edits channel on guild by `payload` settings |
| create_role | guild_id: `Union[str, int]`, role: `dict` | `None` | Creates role by `role` settings on guild |
| delete_role | guild_id: `Union[str, int]`, role_id: `Union[str, int]` | `None` | Remove role from guild |
| edit_role | guild_id: `Union[str, int]`, role_id: `Union[str, int]`, payload: `dict` | `None` | Edits role on guild by `payload` settings |
| kick_member | guild_id: `Union[str, int]`, user_id: `Union[str, int]` | `None` | Kicks member from guild |
| ban_member | guild_id: `Union[str, int]`, user_id: `Union[str, int]` | `None` | Ban member from guild |
| unban_member | guild_id: `Union[str, int]`, user_id: `Union[str, int]` | `None` | Unban member from guild |
| unban_member | guild_id: `Union[str, int]`, user_id: `Union[str, int]` | `None` | Unban member from guild |
| edit_member | guild_id: `Union[str, int]`, user_id: `Union[str, int]`, payload: `dict` | `None` | Edits guild member information |

 

# Usage example

```py
from flaskord import Flaskord

discord_client = Flaskord(token='YOUR_TOKEN_HERE')

guild = discord_client.get_guild(585021318282346496)
print(guild["member_count"]) # returns member count on server (do not forget to turn on Intents on your bot and give him permissions on server)

```

