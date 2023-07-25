from dotenv import load_dotenv

import json

from src.Setup import Setup
from src.Download import Download
from src.Process import Process
from src.Save import Save


def main():
    # TODO: Might to add inheritance to avoid setup.config appearance
    #       in every component initialization

    setup = Setup()

    downloader = Download(setup.config)

    processor = Process(downloader.get_all())

    saver = Save(setup.config["path_to_save"])
    for i, data_chunk in enumerate(processor.clean()):
        saver.save(data_chunk)


if __name__ == '__main__':
    load_dotenv()
    main()
