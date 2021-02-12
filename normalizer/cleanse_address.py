import json

from .algorithms.norm_country import norm_country
from .algorithms.norm_university import norm_university


def norm_addr(record):
    cleansed_str = record['affiliations']
    addr_obj = json.loads(cleansed_str, encoding='utf8')

    countrys = set()
    universitys = set()
    unique_universitys = []

    for aff in addr_obj:
        raw_addr = aff['address']

        country = norm_country(raw_addr) or 'unknown'
        university = norm_university(raw_addr) or 'unknown'
        unique_university = '%s-%s' % (university, university)

        countrys.add(country)
        universitys.add(university)
        unique_universitys.append(unique_university)

    data = {
        'normed_countrys': json.dumps(list(countrys)),
        'normed_universitys': json.dumps(list(universitys)),
        'normed_unique_universitys': json.dumps(list(unique_universitys)),
    }
    return data
