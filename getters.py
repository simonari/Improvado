import requests


def get_friends_list(user_access_token, profile_id="", offset=0, count=250):
    """
    Get the friend list of given profile ID
    :param user_access_token: User's access token
    :param profile_id: Profile ID to get a friend list from.
    Leave blank to get your friend list.
    :param offset: Offset of the friend list.
    :param count: Number of friends to get.
    :return: JSON object containing info about the friend list
    """
    if user_access_token is None:
        raise ValueError("[!] User access token is empty")

    if not profile_id.isdigit() and profile_id != "":
        raise ValueError("[!] User ID is not a number")

    result = requests.get("https://api.vk.com/method/friends.get",
                          params={
                              "access_token": user_access_token,
                              "user_id": profile_id,
                              "order": "name",
                              "fields": "city,country,bdate,sex",
                              "offset": offset,
                              "count": count,
                              "v": "5.131"
                          })

    result = result.json()
    # print(result)
    # Need to check is private chosen profile for user of app
    try:
        # If it's private, then notify user about it and exit
        if result["error"]["error_code"] == 30:
            print("[!] App can't reach friend list of this profile, because it's private for you!")
            exit()
    except KeyError:
        # Else, return a friend list
        print(f"[+] Friend list of profile {profile_id} received!")
        friends_left = int(result["response"]["count"]) - offset - count
        return result["response"], friends_left
