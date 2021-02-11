"""one time scripts
"""
import os
import csv


PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../../'))

input_path = os.path.join(
    PROJECT_ROOT, 'paper-data/merged/nature/nature_papers_merged_all.csv')


def main():
    contentTypes = []

    with open(input_path, 'r') as fr:
        csv_reader = csv.DictReader(fr)
        for row in csv_reader:
            contentTypes.append(row.get('contentType'))

    print(len(contentTypes))

    type_counts = {i: contentTypes.count(i) for i in set(contentTypes)}
    print('| contentType | paper count |')
    print('| ------------- | ------------- |')

    for k, v in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        print('| %s |%4d |' % (k, v))

if __name__ == '__main__':
    main()
