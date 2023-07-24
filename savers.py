import os

import csv
import json

from collections import OrderedDict


sv_delimiters = {
    ".csv": ",",
    ".tsv": "\t",
}


def fill_gaps(data):
    """
    Function to reformat data in a way that is easier to work with.
    Filling empty values with None.
    If values are not empty, then reformat them.
    Replaces sex code with string "Female" or "Male".
    :param data: JSON data.
    :return: JSON formatted data.
    """
    friends = data["items"]
    for friend in friends:
        if "city" not in friend:
            friend["city"] = None
        else:
            friend["city"] = friend["city"]["title"]

        if "country" not in friend:
            friend["country"] = None
        else:
            friend["country"] = friend["country"]["title"]

        if "bdate" not in friend:
            friend["bdate"] = None
        else:
            friend["bdate"] = bdate_to_iso(friend["bdate"])

        if "sex" not in friend:
            friend["sex"] = None
        else:
            friend["sex"] = "Female" if friend["sex"] == 1 else "Male"


def clean_json(data):
    """
    Function to clean JSON data.
    Uses fill_gaps function,
    then order fields and drop unwanted data.
    :param data: JSON data.
    :return: Reformatted JSON data.
    """
    fill_gaps(data)

    for i, friend in enumerate(data["items"]):
        data["items"][i] = OrderedDict([
            ("first_name", friend["first_name"]),
            ("last_name", friend["last_name"]),
            ("country", friend["country"]),
            ("city", friend["city"]),
            ("bdate", friend["bdate"]),
            ("sex", friend["sex"])
        ])

    return data


def bdate_to_iso(bdate):
    """
    Function to convert date to ISO format.
    :param bdate: Date of format <dd.mm.yyyy>.
    :return: Date is ISO format: YYYY-MM-DD.
             If year is not presented, year part is replaced with "XXXX"
    """
    if bdate is None:
        return None

    bdate_s = list(map(int, bdate.split(".")))

    if len(bdate_s) == 3:
        bdate = f"{bdate_s[2]}-{bdate_s[1]:02d}-{bdate_s[0]:02d}"
    else:
        bdate = f"XXXX-{bdate_s[1]:02d}-{bdate_s[0]:02d}"

    return bdate


def save_as_sv(data, path, data_ext=".csv"):
    """
    Function to save data in separated-values formatted files (example: .csv, .tsv, etc).
    :param data: JSON data.
    :param path: Path to save a file.
    :param data_ext: Output file extension.
    """

    with open(path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=sv_delimiters[data_ext])
        fill_gaps(data)
        friends = data["items"]

        for friend in friends:
            writer.writerow([
                friend["first_name"],
                friend["last_name"],
                friend["country"],
                friend["city"],
                friend["bdate"],
                friend["sex"]
            ])

    print(f"[+] Report saved to {path}!")


def save_as_json(data, path):
    """
    Function to save data in .json format.
    :param data: JSON data.
    :param path: Path to save a file.
    """
    data = clean_json(data)

    # after a messy code below, we will get JSON formatted like this:
    # [[{}, {}, {}], [{}, ...], [{}, ...], ..., [{}, ...]]
    # |           |  |       |  |       |       |       |
    #   1st part      2nd        3d              last
    with open(path, "ab") as file:
        # set caveat to eof
        file.seek(0, 2)
        # if a file is empty, dump data
        if file.tell() == 0:
            file.write(json.dumps([data["items"]], indent=2).encode())
        # else: put caveat one symbol back, delete "]" and write extra data
        else:
            file.seek(-1, 2)
            file.truncate()
            file.write(' , '.encode())
            file.write(json.dumps(data["items"], indent=2).encode())
            file.write("]".encode())

    print(f"[+] Report saved to {path}!")


def save(data, path):
    """
    Handler function to specify how to save data.
    :param data: JSON data.
    :param path: Path to save a report.
    """
    directory, file = os.path.split(path)
    filename, data_ext = os.path.splitext(file)

    # saving as JSON
    if data_ext == ".json":
        save_as_json(data, path)
        return

    # saving as .*sv
    save_as_sv(data, path, data_ext)


def create_file(path, data_ext):
    """
    Function to create directory and a report file if they are not existing.
    :param path: Full path to report file.
    :param data_ext: File extension of report file.
    """
    if not os.path.isdir(os.path.split(path)[0]):
        os.makedirs(os.path.split(path)[0])

    if data_ext in [".csv", ".tsv"]:
        with open(path, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file, delimiter=sv_delimiters[data_ext])
            writer.writerow(["First Name", "Last Name", "Country", "City", "Birthdate", "Sex"])

    if data_ext == ".json":
        open(path, "w", encoding="utf-8").close()
