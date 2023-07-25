# VK Friends list getter

## Introduction

This app will help you to get a friend list of user's profiles 
from Vkontakte social network using VK.API.

## How it works?
- Application authenticates under your account using VK.API. 
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
.csv, .tsv, and other formats (read more in [Supported Extensions](#supported-extensions))

## Installation
- Clone repository by using command:
  ```
  $ git clone https://github.com/simonari/Improvado.git
  ```
- Install dependencies using `pip`
  ```
  $ pip install pip install -r requirements.txt
  ```
- Create `.env` file in app root directory containing your VK.Apps Client ID and Client Secret 
  ([How-to-get](#getting-client-id-client-secret)
  It should look like this:
  ```
  VK_CLIENT_ID=<your Client ID>
  VK_CLIENT_SECRET=<your Client Secret>
  ```
- After that, you can run an app using the following command:
  ```
  $ py main.py [-h] [-i ID] [-p PATH]
  ```
  Flags description:
  ```
  -h, --help            show this help message and exit
  -i ID, --id ID        User's ID to get friends list from (Default: <your ID>)
  -p PATH, --path PATH  Path to save a report file (Default: <root>/report.csv)
  ```



## Usage
- Run an app
- Enter profile ID by request. How to get ID explained in [Getting Profile ID of user](#getting-profile-id-of-user)
- Web-browser will be opened
- Sign-in and copy access token from address bar:
  ```
  https://api.vk.com/blank.html#code=<your-access-token>
  ```
- Feed it to an app.
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

## [Getting Client ID, Client Secret]()