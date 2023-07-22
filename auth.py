import os

import webbrowser
import requests


def get_user_auth_code():
    """
    Authorization function that opens VK authorization page where a client has to copy code from url bar
    :return: Authenticated user's code
    """
    vk_app_id = os.environ.get("VK_CLIENT_ID")
    webbrowser.open(
        f"https://oauth.vk.com/authorize"
        f"?client_id={vk_app_id}"
        f"&display=page"
        f"&redirect_uri=https://api.vk.com/blank.html"
        f"&scope=friends"
        f"&response_type=code"
        f"&v=5.131"
    )

    user_auth_code = input("[?] Enter authorization code: ")

    return user_auth_code


def get_access_token(user_auth_code):
    """
    Get expiring access token by generated user authentication code
    :param user_auth_code: User's authentication code
    :return: Access token of user
    """
    result = requests.get("https://oauth.vk.com/access_token",
                          params={
                              "client_id": os.environ.get("VK_CLIENT_ID"),
                              "client_secret": os.environ.get("VK_CLIENT_SECRET"),
                              "redirect_uri": "https://api.vk.com/blank.html",
                              "code": user_auth_code
                          })

    return result.json()["access_token"]


def auth():
    """
    Authorization function that gets authentication code via logging user in VK and
    gets access token via request to VK-API.
    :return: User's access token.
    """

    user_auth_code = get_user_auth_code()
    user_access_token = get_access_token(user_auth_code)

    return user_access_token
