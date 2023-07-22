import os

from dotenv import load_dotenv

import savers
from auth import auth
import getters

load_dotenv()
supported_ext = [".csv", ".tsv", ".json"]


def main():
    user_access_token = auth()
    # 690861865 closed to me
    # 263421973
    # 138826891
    # 97846790 > 1000 friends
    chosen_profile_id = input("[?] Enter user ID (leave blank to get your friend list): ")
    dir_to_save = input("[?] Enter path to save a file (leave blank to save into app root): ")
    filename = input("[?] Enter file name (leave blank to set it to <report>: ")
    print(f"[+] Supported file extensions are: {supported_ext}.")
    data_ext = input(f"[?] Choose output file extension (leave blank to set it to .csv): ").lower()
    
    dir_to_save, filename, data_ext = validate_inputs(dir_to_save, filename, data_ext)
    path_to_save = os.path.join(dir_to_save, filename + data_ext)

    print(path_to_save)

    clear_reports(path_to_save)
    savers.create_file(path_to_save, data_ext)

    friends_left = 1
    offset = 0
    count = 250
    while friends_left > 0:
        print("scanning")
        friends, friends_left = getters.get_friends_list(user_access_token, chosen_profile_id, offset, count)
        print(friends_left)
        savers.save(friends, path_to_save)
        offset += count


def clear_reports(path=""):
    """
    Function to clear reports from standard paths, i.e., in project root and from given path to save
    :param path: Path to save a file
    :return:
    """
    # Clear reports from standard paths
    paths_std = ["report.tsv", "report.csv", "report.json"]
    for path in paths_std:
        if os.path.exists(path):
            os.remove(path)

    if path == "":
        return
    # Clearing an existing report from a save path
    if os.path.exists(path):
        os.remove(path)


def validate_inputs(dir_to_save, filename, data_ext):
    # TODO doc
    if dir_to_save == "":
        dir_to_save = os.getcwd()

    if filename == "":
        filename = "report"

    if data_ext != "" and data_ext not in supported_ext:
        raise ValueError(f"[!] Data extension {data_ext} is not supported.\n"
                         f"[!] Supported extensions: {supported_ext}")

    if data_ext == "":
        data_ext = ".csv"

    return dir_to_save, filename, data_ext


if __name__ == '__main__':
    main()
