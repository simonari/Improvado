import argparse
import os

parser = argparse.ArgumentParser(
    prog="VK Friends Getter",
    description="Get friends list from VK using VK API"
)

parser.add_argument("-i", "--id", dest="id",
                    type=str,
                    help="User's ID to get friends list from\n(Default: <your ID>)")
parser.add_argument("-p", "--path", dest="path",
                    default=os.path.join(os.getcwd(), "report.csv"),
                    help="Path to save a report file (Default: <root/report.csv>)")
