# flaskord
Simple discord API-requester with oauth2 support

How to install 

```
pip install flaskord
```

# Requirements

```
pip install flask
pip install flask_sqlalchemy


app.config should contain 
FLASKORD_CLIENT_ID, FLASKORD_CLIENT_SECRET, FLASKORD_TOKEN, FLASKORD_OAUTH, FLASKORD_OAUTH_REDIRECT_URI, FLASKORD_OAUTH_SCOPE, SQLALCHEMY_DATABASE_URI
to make it possible to use all functions of this module

```

# Parameters

|           Name             |                     Type                     |Default|                           Information                               |
|:-------------------------:|:-------------------------------------------:|:----------:|:-------------------------------------------------------------------:|
|           flaskapp             | `flask.Flask` |   `None`     |    The flask application          |

# Methods

### Do not forget to read https://discord.com/developers/docs/

### Methods for flaskord.client

|    Method      |             Arguments         | Return |   Information   |
|:--------------:|:-----------------------------:|:------:|:---------------:|
|   get_user    |  user_id: `Union[str, int]` |  `dict`  |  Return basic information about user (not include guild)   |
|   fetch_member  | guild_id: `Union[str, int]`, user_id: `Union[str, int]` | `dict` | Return full information about user (include guild) |
| get_guild | guild_id: `Union[str, int]` | `dict` | Return full information about guild (special support for `member_count`, `text_channels`, `voice_channels`, `categories`) |
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

### Methods for flaskord.oauth

|    Method      |             Arguments         | Return |   Information   |
|:--------------:|:-----------------------------:|:------:|:---------------:|
|   get_login_url    |  `None` |  `str`  |  Return the url to oauth discord   |
|   confirm_login  | `None` | `dict` | Write information about logined user into database if not exist, also return dict with detailed information |

# Usage example

```py
from flaskord import Flaskord
from flask import Flask, redirect
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["FLASKORD_CLIENT_ID"] = 1006320287815569448
app.config["FLASKORD_CLIENT_SECRET"] = 'CLIENT_SECRET' # YOUR CLIENT SECRET (https://discord.com/developers/applications/{client_id}/oauth2/general)
app.config["FLASKORD_TOKEN"] = 'YOUR_TOKEN'
app.config["FLASKORD_OAUTH"] = True # remove this line if you dont need oauth 
app.config["FLASKORD_OAUTH_REDIRECT_URI"] = f'http://127.0.0.1:5000/oauth_callback'
app.config["FLASKORD_OAUTH_SCOPE"] = ['identify', 'guilds']

flaskord = Flaskord(app)

@app.route('/testpage')
def testpage():
    return redirect(flaskord.oauth.get_login_url())

@app.rout('/oauth_callback')
def oauth_callback():
    user = flaskord.oauth.confirm_login() # adds user into users.db (username with discriminator and id of user), also return dict with more information about user
    flaskord.client.send(user_id=user["id"], payload='Test message') # payload also supports embed (read docs for more information)
    
    # example of embed payload
    # payload = {
    #     "content": "Test message",
    #     "embeds": [{
    #         "title": "Test",
    #         'color': 0x0099ff,
    #         'fields': [
    #            {"name": "Test", "value":"test","inline":True},
    #            {"name": "Test", "value":"test","inline":True},
    #            {"name": "Test", "value":"test","inline":True}
    #            ],
    #         "image": {
    #             "url": "https://theme.zdassets.com/theme_assets/678183/84b82d07b293907113d9d4dafd29bfa170bbf9b6.ico"
    #         }
    #     }]
    # }

```

