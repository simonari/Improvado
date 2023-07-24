# *VK Friends list getter*

## Introduction

This app will help you to get a friend list of user's profiles 
from Vkontakte social network using VK.API.

## How it works?
- Application authentificates under your account using VK.API. 
It gets permission to receive a friend list of user's profiles, 
which is not closed to your own profile due to their privacy settings;

- After authenticating, an app will wait for your input containing
profile id to get a friend list from.

- An Application will create a report file, 
containing the following fields, sorted in alphabetic order by first name of users:
  - First name
  - Second name
  - Country 
  - City 
  - Birthdate
  - Sex\
File will be located in an app directory by default in 
.csv, .tsv, etc formats (read more in [Supported Extensions](#supported-extensions))

## Usage
- Run an app
- Enter profile ID by request. How to get ID explained in [Getting Profile ID of user](#getting-profile-id-of-user)
- Web-browser will be opened
- Sign-in and copy access token from address bar:
```
https://api.vk.com/blank.html#code=<your-access-token>
```
- Feed it to an app.
- Give to an app the following things:
  - Directory to save a report file
  - Name of report file
  - One of the [supported](#supported-extensions) extensions of report file
- Data collection must begin. It can take a while, so be patient :)
- A report will be saved to chosen directory

## Used API Endpoints
- path: oauth.vk.com
  - GET: /access_token\
    Request to get access token of user\
    Parameters:

    | parameter     | info                      |
    |---------------|---------------------------|
    | client_id     | ID of an app              |
    | client_secret | Secret key of an app      |
    | redirect_uri  | Redirection URI           |
    | code          | Authenticated user's code |

    Returns: access_token of user


- path: api.vk.com
  - GET: method/friends.get\
    Request to get friends' list\
    Parameters:

    | parameter    | info                                        |
    |--------------|---------------------------------------------|
    | access_token | User's access token                         |
    | user_id      | Profile ID of user to get it's friends list |
    | order        | Order of data in response                   |
    | fields       | A list of fields to get                     |
    | offset       | Offset from the beginning of friends list   |
    | count        | How much friends to get per request         |
    | v            | Version of an API                           |

    Returns: JSON response, containing a part or whole friends list
## [Supported Extensions]()
This app can save report files in the following extensions:
- .csv
- .tsv
- .json

## [Getting Profile ID of user]()
Do the following steps to get profile ID of Vkontakte user:
- Open any photo on user's page. If it's closed to you due to chosen user's privacy settings, 
an app can't get a friend list
- The current link in the search bar will look like this: 
```
https://vk.com/<profile-tag>?z=photo<profile-ID>_<some-numbers>%<info-album>
```
- You need to copy a set of numbers that is located between "photo" and underscore.
I've marked them as <profile-ID>