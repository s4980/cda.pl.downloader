import argparse
import json
import os

from configparser import ConfigParser

from cdapldownloader.cdapl import download_videos_from_subfolders
from cdapldownloader.downloader import Downloader


def parse_parameters(cfg):
    parser = argparse.ArgumentParser(prog='cda.pl downloader',
                                     description='Downloads movies from cda.pl',
                                     usage="""
    python cdapldownloader \
      --domain https://www.cda.pl \
      --user testuser \
      --folder https://www.cda.pl/testuser/folder/1790719
    """)
    parser.add_argument('-u', '--user', dest='cda_user', help='Cda.pl user name', required=True)
    parser.add_argument('-d', '--domain', dest='cda_domain', help='Cda.pl main url', required=False,
                        default=cfg.get('cda.pl', 'domain'))
    parser.add_argument('-f', '--folder', dest='cda_folders', help='user folders urls', required=True, action='append')
    parser.add_argument('-o', '--output_folder', dest='output_folder', help='destination folder for downloaded videos',
                        required=False, default=os.getcwd())
    parser.add_argument('--dry-run', dest='dry_run', help='Collect video urls without downloading them',
                        action="store_true")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s version 0.1')

    args = parser.parse_args()
    return json.loads(json.dumps(args.__dict__))


def read_config():
    cfg = ConfigParser()
    cfg.read_file(open(os.path.os.path.join(os.path.dirname(__file__), 'config.cfg')))
    return cfg


def main():
    config = read_config()
    params = parse_parameters(config)
    downloader = Downloader(params['cda_domain'], params['cda_user'], params['output_folder'], params['dry_run'])
    download_videos_from_subfolders(params['cda_folders'], downloader)
