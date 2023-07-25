import requests


class Download:
    """
    Class to download friend list using VK.API.\n
    Can download by calling\n
    get_chunk() multiple times in a row or by calling\n
    get_all() once with usage of generator.
    """
    friends_left = 1

    def __init__(self,
                 _config: dict,
                 _offset: int = 0,
                 _count: int = 250):
        """
        :param _config: Config from Setup class.
        :param _offset: Offset of the friend list.
        :param _count: Number of friends to get.
        """
        self._config_from_setup(_config)
        self.offset = _offset
        self.count = _count

        self.validate()

    def _config_from_setup(self, config: dict):
        """
        :param config: Config from Setup.config.
        :param config: Setup.config property.
        """
        self.access_token = config["_access_token"]
        self.user_id = config["_user_id"]

    def validate(self) -> None:
        """
        Validates set configuration after initialization.
        :return:
        """
        if self.access_token in ["", None]:
            raise ValueError("[!] User access token is empty.")

        if self.user_id is None:
            raise ValueError("[!] User ID is empty.")

        if self.offset < 0:
            raise ValueError("[!] Offset must be positive.")

        if self.count < 0:
            raise ValueError("[!] Count must be positive.")

    def get_chunk(self) -> list[dict]:
        """
        Get a chunk of friends list.
        :return: JSON-formatted data chunk.
        """
        response = requests.get("https://api.vk.com/method/friends.get",
                                params={
                                    "access_token": self.access_token,
                                    "user_id": self.user_id,
                                    "order": "name",
                                    "fields": "city,country,bdate,sex",
                                    "offset": self.offset,
                                    "count": self.count,
                                    "v": "5.131"
                                })
        self.offset += self.count

        result = response.json()
        try:
            # If it's private, then notify user about it and exit
            if result["error"]["error_code"] == 30:
                print("[!] App can't reach friend list of this profile, because it's private for you!")
                exit()
        except KeyError:
            self.friends_left = int(result["response"]["count"]) - self.offset - self.count

            return result["response"]["items"]

    def get_all(self) -> list[dict]:
        """
        Generator to get all friends from a list by chunks of specified size
        :return: JSON-formatted data chunk.
        """
        while self.friends_left > 0:
            yield self.get_chunk()
