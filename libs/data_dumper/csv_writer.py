import csv
import os


# @API
def save_csv(filename, header, data):
    file_dir = os.path.dirname(filename)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for p in data:
            writer.writerow(p)


# @API
def save_result_csv(fname, paper_meta):
    if len(paper_meta) == 0:
        return

    required_f = ['contentType', 'title']
    extra_f = set(paper_meta[0].keys()) - set(required_f)
    fieldnames = required_f + sorted(extra_f)

    save_csv(fname, fieldnames, paper_meta)
