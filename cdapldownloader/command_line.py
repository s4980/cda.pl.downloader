import argparse
import json
import os

from configparser import ConfigParser

from cdapldownloader.cdapl import download_videos


def parse_parameters(cfg):
    parser = argparse.ArgumentParser(prog='cda.pl downloader',
                                     description='Downloads movies from cda.pl',
                                     usage="""
    python cdapldownloader \
      --domain https://www.cda.pl \
      --user testuser \
      --folders 12345 235356 148745
    """)
    parser.add_argument('-u', '--user', dest='cda_user', help='Cda.pl user name', required=True)
    parser.add_argument('-d', '--domain', dest='cda_domain', help='Cda.pl main url', required=False,
                        default=cfg.get('cda.pl', 'domain'))
    parser.add_argument('-f', '--folder', dest='cda_folders', help='user folders', required=True, action='append')
    parser.add_argument('--dry-run', dest='dry_run', help='Collect video urls without downloading them',
                        action="store_true")
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s version 0.1')

    args = parser.parse_args()
    return json.loads(json.dumps(args.__dict__))


def read_config():
    cfg = ConfigParser()
    cfg.read_file(open(os.path.os.path.join(os.path.dirname(__file__), 'config.cfg')))
    return cfg


def main():
    config = read_config()
    download_videos(parse_parameters(config))
