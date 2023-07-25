import os
import sys

import webbrowser
import requests

from dotenv import load_dotenv

from .parser_cli import parser

load_dotenv()


class Setup:
    supported_ext = [".csv", ".tsv", ".json"]

    _vk_app_id = os.environ.get("VK_CLIENT_ID")
    _vk_client_secret = os.environ.get("VK_CLIENT_SECRET")

    _auth_code = None
    _access_token = None

    _data_ext = None

    def __init__(self):
        args = parser.parse_args(sys.argv[1:])

        self._profile_id_to_retrieve_from, self._path_to_save = args.id, args.path
        self._validate_inputs()

        self._get_user_auth_code()
        self._get_access_token()

    @property
    def config(self) -> dict:
        conf = {
            "auth_code": self._auth_code,
            "access_token": self._access_token,
            "profile_id_to_retrieve_from": self._profile_id_to_retrieve_from,
            "path_to_save": self._path_to_save,
            "data_ext": self._data_ext
        }

        return conf

    def _validate_inputs(self) -> None:
        """
        Validate inputs to correctly save data.
        """
        _id = self._profile_id_to_retrieve_from
        _path = self._path_to_save

        if _id is not None and not _id.isdigit():
            raise ValueError("ID must be a positive integer.")

        if _id is None:
            _id = ""

        # TODO: Might add check for correct filename: not containing any special characters.

        # Check to an absolute path
        if not os.path.isabs(_path):
            _path = os.path.join(os.getcwd(), _path)
            print(f"asfdg {_path}")

        # Check to a valid path
        if not os.path.isdir(os.path.split(_path)[0]):
            raise ValueError(f"Directory {_path} is not valid!")

        data_ext = os.path.splitext(_path)[-1]

        if data_ext not in self.supported_ext:
            raise ValueError(f"Data extension {data_ext} is not supported.\n"
                             f"Supported extensions: {self.supported_ext}")

        self._data_ext = data_ext

        self._profile_id_to_retrieve_from = _id
        self._path_to_save = _path

    def _get_user_auth_code(self) -> None:
        """
        Authorization function that opens VK authorization page where a client has to copy code from url bar
        """
        webbrowser.open(
            f"https://oauth.vk.com/authorize"
            f"?client_id={self._vk_app_id}"
            f"&display=page"
            f"&redirect_uri=https://api.vk.com/blank.html"
            f"&scope=friends"
            f"&response_type=code"
            f"&v=5.131"
        )

        self._auth_code = input("[?] Enter authorization code: ")

    def _get_access_token(self) -> None:
        """
        Get access token by generated user authentication code
        """
        result = requests.get("https://oauth.vk.com/access_token",
                              params={
                                  "client_id": self._vk_app_id,
                                  "client_secret": self._vk_client_secret,
                                  "redirect_uri": "https://api.vk.com/blank.html",
                                  "code": self._auth_code
                              })

        self._access_token = result.json()["access_token"]
