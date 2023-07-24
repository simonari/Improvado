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
    print(args.id, args.directory, args.filename, args.extension)

    chosen_profile_id, dir_to_save, filename, data_ext = validate_inputs(args.id,
                                                                         args.directory,
                                                                         args.filename,
                                                                         args.extension)

    user_access_token = auth()
    # 690861865 closed to me
    # 263421973
    # 138826891
    # 97846790 > 1000 friends

    path_to_save = os.path.join(dir_to_save, filename + data_ext)

    clear_reports(path_to_save)
    savers.create_file(path_to_save, data_ext)

    friends_left = 1
    offset = 0
    count = 250
    while friends_left > 0:
        friends, friends_left = getters.get_friends_list(user_access_token, chosen_profile_id, offset, count)
        savers.save(friends, path_to_save)
        offset += count


def clear_reports(path):
    """
    Function to clear reports from standard paths, i.e., in project root and from given path to save
    :param path: Path to save a file
    """
    # Clear reports from standard paths
    paths_std = ["report.tsv", "report.csv", "report.json"]
    for path in paths_std:
        if os.path.exists(path):
            os.remove(path)

    # Clearing an existing report from a save path
    if os.path.exists(path):
        os.remove(path)


def validate_inputs(_id, dir_to_save, filename, data_ext):
    """
    Validate inputs to correctly save data.
    :param _id: User's ID to get friends list from.
    :param dir_to_save: Directory where a report will be saved.
                        Default - app root.
    :param filename: Name of report file.
    :param data_ext: Extension of a file, which contains report data.
                     Default: ".csv".
                     Raises ValueError if data_ext is not supported.
    :return: Validated inputs.
    """
    if _id is not None and not _id.isdigit():
        raise ValueError("ID must be a positive integer.")

    # TODO: Might add check for correct filename: not containing any special characters

    if not os.path.isabs(dir_to_save):
        # If a user enters a relative path with leading slash -> remove it
        if dir_to_save.startswith("/"):
            dir_to_save = dir_to_save[1:]
        # Making path absolute

        dir_to_save = os.path.join(os.getcwd(), dir_to_save)

        if not os.path.isdir(dir_to_save):
            raise ValueError(f"Directory {dir_to_save} is not valid!")

    if data_ext not in supported_ext:
        raise ValueError(f"Data extension {data_ext} is not supported.\n"
                         f"Supported extensions: {supported_ext}")

    return _id, dir_to_save, filename, data_ext


if __name__ == '__main__':
    main()
