import os
import glob
import pandas as pd


PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../'))

input_path = os.path.join(
    PROJECT_ROOT, 'paper-data/rawdata/nature')

output_dir = os.path.join(
    PROJECT_ROOT, 'paper-data/merged/nature')


def main():
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    all_journal_data = []
    for journal_pcode in sorted(os.listdir(input_path)):
        journal_path = os.path.join(input_path, journal_pcode)

        journal_data = merge_journal(journal_pcode, journal_path, output_dir)
        all_journal_data.append(journal_data)

    all_in_one_csv = pd.concat(all_journal_data)

    output_file = "%s/_all_papers_merged.csv" % output_dir
    all_in_one_csv.to_csv(output_file, index=False, encoding='utf-8')


def merge_journal(journal_pcode, journal_path, output_dir, extension='csv'):

    all_filenames = [i for i in sorted(glob.glob('%s/*.%s' % (journal_path, extension)))]

    # combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])

    # filter
    data = combined_csv[combined_csv['contentType'].isin(['letter', 'article'])]
    # export to csv
    output_file = "%s/%s_papers_merged.csv" % (output_dir, journal_pcode)
    data.to_csv(output_file, index=False, encoding='utf-8')

    return data


if __name__ == '__main__':
    main()
