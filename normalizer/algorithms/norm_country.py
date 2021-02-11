import json
import os

PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../'))

country_data_file = os.path.join(
    PROJECT_ROOT, 'metadata/iso_3166_country_codes.json')
country_map = {}


# @API
def norm_country(addr):
    if len(country_map) == 0:
        build_country_map()

    for p in reversed(addr.split(',')):
        p = p.strip(' .').lower()
        if p in country_map:
            return country_map[p]

    return None


country_map_extra = {
    'UK': 'United Kingdom',
    'Northern Ireland': 'United Kingdom',  # part of the country
    'Russia': 'Russian Federation',
    'Korea': 'Korea (the Republic of)',
    'South Korea': 'Korea (the Republic of)',
    'S. Korea': 'Korea (the Republic of)',
    'Republic of Korea': 'Korea (the Republic of)',
    'Czech Republic': 'Czechia',
    'The Netherlands': 'Netherlands',
    'PR China': 'China',
    'P. R. China': 'China',
    "People's Republic of China": 'China',
    "People’s Republic of China": 'China',
    'Taiwan': 'Taiwan (Province of China)',
    'México': 'Mexico',
    'United States': 'United States of America',
    'Napoli': 'Italy',  # city of the country
    'Iran': 'Iran (Islamic Republic of)',
    'Kingdom of Saudi Arabia': 'Saudi Arabia',
    'bâtiment A. Kastler': 'France',  # city of the country
    'UAE': 'United Arab Emirates',
    'FI-40014': 'Finland',
    '3112 Etcheverry Hall': 'United States of America',  # location in the country
    'School of Electrical and Computer Engineering': 'Brazil',  # not sure
}


def build_country_map():
    with open(country_data_file, 'r') as fr:
        data = json.load(fr)

    for item in data:
        name = item['country_name']

        # name and alias keys
        keys = ['country_name', 'alpha_2', 'alpha_3']

        for k in keys:
            country_map[item[k].lower()] = name

    # manually adding
    for k, v in country_map_extra.items():
        country_map[k.lower()] = v


if __name__ == '__main__':
    print(norm_country('Shanghai, China'))
    print(norm_country('Shanghai China'))
