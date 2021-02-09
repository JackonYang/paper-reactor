"""one time scripts
"""
import os
import csv


PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../../'))

input_path = os.path.join(
    PROJECT_ROOT, 'paper-data/merged/')


journals = [
    ('nature', 'lsa'),
    ('nature', 'nphoton'),
    ('nature', 'nnano'),
]


def main():
    contentTypes = []
    for journal_group, journal_pcode in journals:
        filename = '%s/%s_papers_merged.csv' % (journal_group, journal_pcode)

        csv_file = os.path.join(input_path, filename)
        with open(csv_file, 'r') as fr:
            csv_reader = csv.DictReader(fr)
            for row in csv_reader:
                contentTypes.append(row.get('contentType'))

    print(len(contentTypes))

    type_counts = {i: contentTypes.count(i) for i in set(contentTypes)}
    for k, v in sorted(type_counts.items(), key=lambda x: x[1]):
        print('%4d: %s' % (v, k))

if __name__ == '__main__':
    main()
