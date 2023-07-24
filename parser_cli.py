import argparse
import os

parser = argparse.ArgumentParser(
    prog="VK Friends Getter",
    description="Get friends list from VK using VK API"
)

parser.add_argument("-i", "--id", dest="id",
                    type=str,
                    help="User's ID to get friends list from\n(Default: <your ID>)")
parser.add_argument("-d", "--directory", dest="directory",
                    default=os.getcwd(),
                    help="Path to save a report file\n(Default: app root)")
parser.add_argument("-n", "--filename", dest="filename",
                    default="report", type=str,
                    help="Name of report file\n(Default: 'report')")
parser.add_argument("-e", "-extension", dest="extension",
                    default=".csv", type=str,
                    help="Report file extension\n(Default: .csv)")
