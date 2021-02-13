import os
import sys


PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../'))
sys.path.insert(0, PROJECT_ROOT)

from libs.data_loader.csv_loader.nature_data_loader import load_nature_data
from libs.data_dumper.csv_writer import save_result_csv

from normalizer.cleanse_address import norm_addr


output_dir = os.path.join(
    PROJECT_ROOT, 'paper-data/merged/nature')

DOI_KEY = 'doi'


filters = {
    'long_paper': lambda x: x['contentType'] in ['article', 'letter'],
}


def main():

    trans = load_nature_data('trans')
    trans_map = {p[DOI_KEY]: p for p in trans}
    print('trans map length: %s' % len(trans_map))

    data = load_nature_data('rawdata')

    for record in data:
        key = record[DOI_KEY]
        if key in trans_map:
            record.update(trans_map[key])

        record.update(norm_addr(record))

    output(data)


def output(data):
    base_name = os.path.join(output_dir, "nature_papers_merged_%s.csv")

    output_file = base_name % 'all'
    save_result_csv(output_file, data)
    print('%s records saved: %s' % (len(data), output_file))

    for f_name, f_func in filters.items():
        filename = base_name % f_name
        filterd_data = [r for r in data if f_func(r)]
        save_result_csv(filename, filterd_data)
        print('%s %s records saved: %s' % (f_name, len(filterd_data), filename))


if __name__ == '__main__':
    main()
