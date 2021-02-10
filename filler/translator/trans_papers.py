import os
import csv

from google_translator import translate


PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../'))

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
    for journal_pcode in sorted(os.listdir(input_path)):
        journal_path = os.path.join(input_path, journal_pcode)
        for issue in sorted(os.listdir(journal_path)):
            output_file = os.path.join(
                output_dir, journal_pcode, issue
            )

            if os.path.exists(output_file):
                # print('skip, output file exists: %s' % output_file)
                continue

            issue_csv_file = os.path.join(journal_path, issue)
            issue_data = load_journal_issue_data(issue_csv_file)
            trans_data = trans_records(issue_data)
            save_csv(output_file, output_header, trans_data)
            print('saved: %s' % output_file)


def load_journal_issue_data(issue_csv_file):
    with open(issue_csv_file, 'r') as fr:
        csv_reader = csv.DictReader(fr)
        data = [line for line in csv_reader]

    return data


def save_csv(filename, header, data):
    file_dir = os.path.dirname(filename)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for p in data:
            writer.writerow(p)


def trans_records(issue_data):
    results = []
    for record in issue_data:

        contentType = record['contentType']

        if contentType not in ['letter', 'article']:
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
