

university_keywords = [i.lower().strip() for i in [
    'Samsung',
    'Toshiba',
    'RIKEN',
    'EPFL',
    'ETH Zurich',
    'Philips Lumileds Lighting',
    'Technion',  # Israel
    'Hamamatsu Photonics',
    'university',
    'Universidad',
    'Academia Sinica',  # taiwan
    'Chinese Academy of Sciences',
    'College',
    'Scuola Normale',
    'Universit',  # 'Universit?t',
    'Institut',  # 'Institute',
    'Istituto',  # Spanish
    'Instituci',
    'Instituut',
    'Campus',
    'school',
    'Laborator',  # 'Laboratories', 'Laboratory',
    'agency',
    'Corporation',
    'Ltd',
    'Company',
    'Center',
    'Centro',
    'Centre',
    'Research',
    'Technolog',
    'Technische',
    'Technion',
    'Polytechnique',
    'Foundation',
]]

university_keywords_negitive = [i.lower().strip() for i in [
    'Road',
    'Box',
    'Universitätsstr',
    'Boulevard',
    'Blvd',
    'University Park',
    '00',
]]

munually_university_cases = [
    ('EPFL', 'EPFL'),
    ('Born', 'Max Born Institute'),
    ('IBM', 'IBM Thomas J. Watson Research Center'),
    ('NTT', 'NTT Corporation'),
    ('Toshiba', 'Toshiba Research Europe Ltd'),
    ('CentraleSupélec', 'CentraleSupélec'),
    ('University of Ottawa', 'University of Ottawa'),
    ('Leibniz Universität Hannover and Max-Planck-Institut für Gravitationsphysik (Albert-Einstein-Institut)',
        'Leibniz Universität Hannover and Max-Planck-Institut für Gravitationsphysik'),
    ('Max Planck Advanced Study Group at Center for Free-Electron Laser Science (CFEL)',
        'Max Planck Advanced Study Group at Center for Free-Electron Laser Science'),
    ('Max-Planck-Zentrum für Physik und Medizin', 'Max-Planck-Zentrum für Physik und Medizin'),
    ('Planck', 'Max Planck Society'),
    ('Swiss Cent', 'Swiss Centre for Electronics and Microtechnology'),
    ('Russian Quantum Center', 'Russian Quantum Center'),
    ('University of Colorado and NIST', 'University of Colorado and NIST'),
    ('NIST and the University of Colorado', 'University of Colorado and NIST'),
    ('NIST 325 Broadway', 'National Institute of Standards and Technology'),
    ('DESY and University of Hamburg', 'DESY and University of Hamburg'),
    ('University of Hamburg', 'University of Hamburg'),
    ('Ludwig Maximilians University', 'Ludwig Maximilians University Munich'),
    ('Friedrich Schiller University', 'Friedrich Schiller University of Jena'),
    ('Friedrich Alexander University', 'Friedrich Alexander University of Erlangen Nürnberg'),
    ('Osaka University', 'Osaka University'),
    ('University of Tokyo', 'University of Tokyo'),
    ('RIKEN', 'RIKEN'),
    ('World Lab', 'World-Lab. Co. Ltd'),
    ('Technion', 'Technion'),
    ('Seoul National University', 'Seoul National University'),
    ('Intel', 'Intel Corporation'),
    ('Harvard Medical School', 'Harvard Medical School'),
    ('University of Nebraska', 'University of Nebraska Lincoln'),
    ('University of Colorado', 'University of Colorado'),
    ('Hewlett Packard', 'Hewlett Packard Labs'),
    ('Johns Hopkins University', 'Johns Hopkins University'),
    ('Iowa State University', 'Iowa State University'),
    ('California Institute of Technology', 'California Institute of Technology'),
    ('City University of New York', 'City University of New York'),
    ('University of Alberta', 'University of Alberta'),
    ('Institut national de la recherche scientifique', 'Institut National de la Recherche Scientifique'),
    ('Institut National de la Recherche Scientifique', 'Institut National de la Recherche Scientifique'),
    ('CIC nanoGUNE', 'CIC NanoGUNE'),
    ('CIC NanoGUNE', 'CIC NanoGUNE'),
    ('cole Polytechnique F', 'Federal Institute of Technology in Lausanne'),
    ('Ecole Polytechnique ParisTech', 'ParisTech Polytechnic Schoo'),
    ('Elettra Sincrotrone Trieste', 'Elettra Sincrotrone Trieste'),
    ('FOM Institute', 'FOM Institute AMOLF'),
    ('Ghent University', 'Ghent University'),
    ('ICFO', 'ICFO Institut de Ciencies Fotoniques'),
    ('Imperial College', 'Imperial College'),
    ('Nanophotonic', 'NanoPhotonics'),
    ('Paul Scherrer Institut', 'Paul Scherrer Institute'),
    ('Université Paris 7', 'Université Paris 7'),
    ('CNRS', 'CNRS'),
    ('Ruprecht', 'Heidelberg University'),
    ('Laboratory of Photonics and Quantum Measurements', 'EPFL'),
    ('Cambridge University', 'University of Cambridge'),
    ('University of Karlsruhe', 'Karlsruhe Institute of Technology'),
    ('Physikalisch Technical Bundesanstalt', 'Physikalisch-Technische Bundesanstalt'),
]

translates = [
    ('-', ' '),
    ('The ', ''),
    ('Universitá', 'University'),
    ('Università', 'University'),
    ('University of California at ', 'University of California '),
    ('Universität', 'University of'),
    ('Technische', 'Technical'),
    ('München', 'Munich'),
]

university_endings = [
    '(',
    ' in ',
]


# @API
def norm_university(addr):
    parts = [i.strip() for i in addr.split(',')]

    for k in university_keywords:

        for p in reversed(parts):
            p_lower = p.lower()

            if k in p_lower:
                negtive_triggered = False
                for n in university_keywords_negitive:
                    if n in p_lower:
                        negtive_triggered = True
                if not negtive_triggered:
                    return clean_university_name(p, addr)

    return clean_university_name(parts[0], addr)


def clean_university_name(name, addr):
    # hard coded rules for very special cases
    if 'National Institute of Standards and Technology' in name and 'University' in name:
        name = name.replace('National Institute of Standards and Technology', 'NIST')
    if 'Maryland' in name and 'NIST' in name:
        return 'NIST and the University of Maryland'

    # translate to English to deduplicate
    for old, new in translates:
        name = name.replace(old, new)

    # manually mappings
    for k, v in munually_university_cases:
        if k in name:
            # print('%s | %s' % (v, name))
            return v.strip()

    for end_token in university_endings:
        if name.count(end_token):
            brief_index = name.find(end_token)
            name = name[:brief_index].strip()

    return name


if __name__ == '__main__':
    print(norm_university('Michael Hayden is in the Department of Physics, University of Maryland Baltimore County, Baltimore, Maryland 21250, USA. hayden@umbc.edu'))
    print(norm_university('Ovum, 2033 Gateway Place, San Jose, 95110, California, USA'))
