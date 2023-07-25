import os
import sys

from dotenv import load_dotenv

import savers
from auth import auth
import getters
import parser_cli

load_dotenv()
supported_ext = [".csv", ".tsv", ".json"]


def main():
    args = parser_cli.parser.parse_args(sys.argv[1:])

    profile_id, path_to_save = args.id, args.path
    profile_id, path_to_save = validate_inputs(profile_id, path_to_save)

    # 690861865 closed to me
    # 263421973
    # 138826891
    # 97846790 > 1000 friends
    user_access_token = auth()

    clear_reports(path_to_save)
    savers.create_file(path_to_save)

    friends_left = 1
    offset = 0
    count = 250
    while friends_left > 0:
        friends, friends_left = getters.get_friends_list(user_access_token, profile_id, offset, count)
        savers.save(friends, path_to_save)
        offset += count
    print(f"[+] Report saved to {path_to_save}!")


def clear_reports(path: str):
    """
    Function to clear reports from standard paths, i.e., in project root and from given path to save
    :param path: Path to save a file
    """
    # Clear reports from standard paths
    cwd = os.getcwd()
    paths_std = ["report.tsv", "report.csv", "report.json"]
    paths_std = [os.path.join(cwd, path) for path in paths_std]

    for path in paths_std:
        if os.path.exists(path):
            os.remove(path)

    # Clearing an existing report from a save path
    if os.path.exists(path):
        os.remove(path)


def validate_inputs(_id: str, path: str) -> tuple[str, str]:
    """
    Validate inputs to correctly save data.
    :param _id: User's ID to get friends list from.
    :param path: Path to save a report file.
    :return: Validated inputs.
    """
    if _id is not None and not _id.isdigit():
        raise ValueError("ID must be a positive integer.")

    # TODO: Might add check for correct filename: not containing any special characters.

    # Check to an absolute path
    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)

    # Check to a valid path
    if not os.path.isdir(os.path.split(path)[0]):
        raise ValueError(f"Directory {path} is not valid!")

    data_ext = os.path.splitext(path)[-1]

    if data_ext not in supported_ext:
        raise ValueError(f"Data extension {data_ext} is not supported.\n"
                         f"Supported extensions: {supported_ext}")

    return _id, path


if __name__ == '__main__':
    main()
