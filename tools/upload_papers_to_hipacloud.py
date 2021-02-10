import requests
import json
import os
import time

import sys

PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../'))
lib_path = os.path.join(
    PROJECT_ROOT, 'libs'
)

sys.path.insert(0, lib_path)

from data_loader.csv_loader.nature_data_loader import load_csv_file

APP_URL = 'https://api.hipacloud.com/v1/apps/6024022362434ae27203d4b1/tables/6024022362434ae27203d4b7/records'

token_config_file = os.path.join(os.path.expanduser('~'), '.hipacloud-token')
with open(token_config_file, 'r') as fr:
    token = ''.join(fr.readlines()).strip()


def main(datafile):
    for record in load_csv_file(datafile):
        send_request(transform_record(record))


def transform_record(record):
    to_int = [
        'count_accesses',
        'count_altmetric',
        'count_citations',
        'issue',
        'volume',
    ]
    for key in to_int:
        record[key] = int(record[key])

    return record


def send_request(data):
    try:
        response = requests.post(
            url=APP_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer %s" % token,
            },
            data=json.dumps({
                "values": data,
            })
        )
        if response.status_code != 200:
            print(response.text)
            print(data)
            print('==========')
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


if __name__ == '__main__':
    main('/home/jackon/vip-projects/paper-reactor/paper-data/merged/nature/nature_papers_merged_long_paper.csv')
