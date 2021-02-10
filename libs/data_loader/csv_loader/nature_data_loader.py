import os
import csv


PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../../'))

data_root = os.path.join(
    PROJECT_ROOT, 'paper-data')


# @API
def load_nature_data(data_type='rawdata'):

    data = []

    for journal_pcode, issue, issue_data in iter_nature_data(data_type):
        data.extend(issue_data)

    return data


# @API
def iter_nature_data(data_type='rawdata'):
    input_path = os.path.join(data_root, data_type, 'nature')

    for journal_pcode in sorted(os.listdir(input_path)):
        journal_path = os.path.join(input_path, journal_pcode)
        for issue in sorted(os.listdir(journal_path)):
            issue_csv_file = os.path.join(journal_path, issue)
            issue_data = load_journal_issue_data(issue_csv_file)
            yield (journal_pcode, issue, issue_data)


def load_journal_issue_data(issue_csv_file):
    with open(issue_csv_file, 'r') as fr:
        csv_reader = csv.DictReader(fr)
        data = [line for line in csv_reader]

    return data


if __name__ == '__main__':
    load_nature_data()
