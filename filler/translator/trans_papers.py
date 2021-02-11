import os
import sys

from google_translator import translate


PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../'))

lib_path = os.path.join(
    PROJECT_ROOT, 'libs'
)

sys.path.insert(0, lib_path)

from data_loader.csv_loader.nature_data_loader import iter_nature_data
from data_dumper.csv_writer import save_csv
from config.content_types import translateContentTypes


input_path = os.path.join(
    PROJECT_ROOT, 'paper-data/rawdata/nature')

output_dir = os.path.join(
    PROJECT_ROOT, 'paper-data/trans/nature')


record_key_name = 'doi'
field_to_trans = [
    'title',
    'abstract',
    # 'affiliations',
]

output_header = [
    record_key_name,
    'title',
    'title_cn',
    'abstract',
    'abstract_cn',
    # 'affiliations',
    # 'affiliations_cn',
]


def main():
    data_type = 'rawdata'
    for journal_pcode, issue, issue_data in iter_nature_data(data_type):
            output_file = os.path.join(
                output_dir, journal_pcode, issue
            )

            if os.path.exists(output_file):
                print('skip, output file exists: %s' % output_file)
                continue

            trans_data = trans_records(issue_data)
            save_csv(output_file, output_header, trans_data)
            print('saved: %s' % output_file)


def trans_records(issue_data):
    results = []
    for record in issue_data:

        contentType = record['contentType']

        if contentType not in translateContentTypes:
            continue

        trans_record = {
            key: record[key] for key in field_to_trans
        }
        trans_record[record_key_name] = record[record_key_name]

        for key in field_to_trans:
            value = record[key]
            trans_record['%s_cn' % key] = translate(value, sleep_interval=5)
        results.append(trans_record)

    return results


if __name__ == '__main__':
    main()
