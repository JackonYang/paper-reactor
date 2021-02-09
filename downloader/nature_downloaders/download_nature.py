import csv
import json
import re
import bleach
import os

from jkPyUtils.requests2.fetch import get_url_text

from lxml import etree


PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../'))
output_dir = os.path.join(
    PROJECT_ROOT, 'paper-data/rawdata/nature')

# inner configs, do NOT modify
DOI_DOMAIN = 'https://doi.org/'
domain = 'https://www.nature.com'

ptn = re.compile(r'\s*<a>.*?</a>\s*,?\s*')
to_add_space_ptn = re.compile(r'([,.])(\w\w)')
sections = [
    # 'NewsandViews',
    # 'Perspectives',
    'Letters',
    'Letter',
    'Articles',
    'Article',
    # 'AmendmentsandCorrections',
]


# @API
def download_issue_meta(journal_pcode, volume, issue):
    print('=== start downloading %s Vol.%s Iss.%s' % (journal_pcode, volume, issue))
    papers = get_issue_paper_list(journal_pcode, volume, issue)

    if papers is None or len(papers) == 0:
        print('error in %s.%s. papers: %s' % (volume, issue, papers and len(papers)))
        return

    paper_meta = []
    for idx, p in enumerate(papers):
        article_url = p['url']
        if 'articles/' not in article_url:
            # print('WARNING: ignoring %s' % article_url)
            continue

        try:
            print('downloading [Vol%s Iss%s] (%s/%s). %s, %s' % (volume, issue, idx+1, len(papers), p['title'], article_url))
            html = get_url_text(article_url)
            # print(len(html), html[:10])
            metainfo = parse_paper_metainfo(html)
            p.update(metainfo)
            paper_meta.append(p)
        except Exception as e:
            print('!!! error', e)

    save_csv(volume, issue, paper_meta)


# @API
def save_csv(year, issue, paper_meta):
    if len(paper_meta) == 0:
        return

    journal_pcode = paper_meta[0]['journal_pcode']
    journal_dirname = os.path.join(output_dir, journal_pcode)
    if not os.path.exists(journal_dirname):
        os.makedirs(journal_dirname)

    fname = os.path.join(journal_dirname, '%s-volume%02d-issue%02d.csv' % (journal_pcode, year, issue))
    required_f = ['contentType', 'title']
    extra_f = set(paper_meta[0].keys()) - set(required_f)
    fieldnames = required_f + sorted(extra_f)

    with open(fname, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for p in paper_meta:
            writer.writerow(p)

    print('---> %s papers in %s' % (len(paper_meta), fname))


def translate(src):
    return ''
    # output = translator.translate(src, dest='zh-cn').text
    # return output


def get_nodes_from_html(html, xpath_ptn):
    if isinstance(html, str):
        dom = etree.HTML(html)
    else:
        dom = html
    nodes = dom.xpath(xpath_ptn)
    return nodes


def clean_abstract(text):
    allowed_tags = ['p', 'sup', 'sub', 'a']
    text = bleach.clean(text, tags=allowed_tags, attributes=[], strip=True, strip_comments=True)
    text = ptn.sub('', text).replace('<sup></sup>', '')
    return text


def clean_text(text):
    text = text.replace('’', "'").replace('‘', "'")
    return text


def get_issue_paper_list(journal_pcode, volume, issue):
    url = 'https://www.nature.com/%s/volumes/%s/issues/%s' % (journal_pcode, volume, issue)
    title_ptn = '//*[@class="mb10 extra-tight-line-height"]/a'
    # title_ptn = '//*[@id="Letter-content"]/ul/li[2]/article/div/h3/a'

    content = get_url_text(url)
    if content is None:
        return

    papers = []
    title_nodes = get_nodes_from_html(content, title_ptn)

    titles = [''.join(i.itertext()).strip() for i in title_nodes]
    urls = [i.attrib['href'] for i in title_nodes]

    for t, url in zip(titles, urls):
        paper_url = domain + url
        # title_cn = translate(t)
        papers.append({
            'title': t,
            'url': paper_url,
        })
    return papers


def should_parse_abstract(contentType):
    contentType_lower = contentType.lower()
    keywords = [
        'news',
        'highlights',
        'perspective',
        'editorial',
        'out of the lab',
        'in this issue',
        'interview',
        'profile',
        'photonics at npg',
        'commentary',
        'correction',
        'correspondence',
        'arts',
        'product',
        'erratum',
    ]

    for k in keywords:
        if k.lower() in contentType_lower:
            return False
    return True


def parse_paper_metainfo(content):
    detail_info = {}

    metadata_ptn = '//*[@data-test="dataLayer"]'
    metadata_str = get_nodes_from_html(content, metadata_ptn)[0].text.strip()

    start_idx = metadata_str.index('[')
    end_idx = metadata_str.rindex(']')
    metadata_obj = json.loads(metadata_str[start_idx: end_idx + 1])[0]['content']
    # print(json.dumps(metadata_obj, indent=4))

    contentType = metadata_obj['category']['contentType']
    detail_info['contentType'] = contentType
    detail_info['doi'] = metadata_obj['article']['doi']
    detail_info['doi_url'] = DOI_DOMAIN + metadata_obj['article']['doi'].lstrip('/')

    detail_info['authors'] = json.dumps(metadata_obj['contentInfo']['authors'], ensure_ascii=True)
    detail_info['publishedAt'] = metadata_obj['contentInfo']['publishedAt']
    detail_info['publishedAtString'] = metadata_obj['contentInfo']['publishedAtString']
    detail_info['title'] = clean_text(metadata_obj['contentInfo']['title'])
    detail_info['documentType'] = metadata_obj['contentInfo']['documentType']

    detail_info['journal_pcode'] = metadata_obj['journal']['pcode']
    detail_info['journal_title'] = metadata_obj['journal']['title']
    detail_info['volume'] = metadata_obj['journal']['volume']
    detail_info['issue'] = metadata_obj['journal']['issue']

    detail_info['authorization'] = metadata_obj['authorization']['status']
    detail_info['issue'] = metadata_obj['journal']['issue']
    detail_info['issue'] = metadata_obj['journal']['issue']

    # focus & subjects
    detail_info['focus'] = metadata_obj['category']['legacy']['webtrendsContentCollection']
    detail_info['subjects'] = metadata_obj['category']['legacy']['webtrendsSubjectTerms']

    # print(contentType)
    # parse abstract
    # abs_text_cn = ''
    abs_text = ''
    if should_parse_abstract(contentType):
        abs_nodes = get_nodes_from_html(content, '//*[@id="Abs1-content"]/p')
        if len(abs_nodes) == 0:
            abs_text = ''
        else:
            assert len(abs_nodes) == 1
            abs_node = abs_nodes[0]
            abs_html = etree.tostring(abs_node).decode('utf8')
            abs_text = clean_text(clean_abstract(abs_html))

        # abs_text_cn = translate(abs_text)

    detail_info['abstract'] = abs_text
    # detail_info['abstract_google_cn'] = abs_text_cn

    # citation_str
    citation_ptn = '//*[@class="c-bibliographic-information__citation"]'
    citation_node = get_nodes_from_html(content, citation_ptn)[0]
    citation_str = ''.join([i.strip() for i in citation_node.itertext()])

    url_start = citation_str.rfind('https://')
    citation_str = citation_str[:url_start].strip()
    citation_str = to_add_space_ptn.sub(r'\1 \2', citation_str)
    detail_info['citation_text'] = citation_str

    metrics_ptn = '//*[@class="c-article-metrics-bar__count"]'
    metrics_nodes = get_nodes_from_html(content, metrics_ptn)
    for n in metrics_nodes:
        cnt, cnt_name = list(n.itertext())
        key = 'count_%s' % cnt_name.lower().strip()
        detail_info[key] = int(cnt.strip().replace('k', '000'))
    if 'count_citations' not in detail_info:
        detail_info['count_citations'] = 0
    if 'count_altmetric' not in detail_info:
        detail_info['count_altmetric'] = 0

    # parse affiliation
    aff_addr_ptn = '//*[@class="c-article-author-affiliation__address u-h3"]'
    aff_author_ptn = '//*[@class="c-article-author-affiliation__authors-list"]'
    aff_addrs = get_nodes_from_html(content, aff_addr_ptn)
    aff_authors = get_nodes_from_html(content, aff_author_ptn)
    affs = []
    for aff_addr, aff_author in zip(aff_addrs, aff_authors):
        affs.append({
            'address': ' '.join(aff_addr.itertext()),
            'authors': list(aff_author.itertext()),
        })
    # print(json.dumps(affs, indent=4))
    detail_info['affiliations'] = json.dumps(affs, ensure_ascii=True)

    return detail_info


def download_nphoton():
    journal_pcode = 'nphoton'
    # Vol.1 released in 2007
    # for year in range(2007, 2020):
    for volume in range(15, 14):
        for i in range(12):
            issue = i + 1
            download_issue_meta(journal_pcode, volume, issue)

    volume = 15
    for issue in range(1, 3):
        download_issue_meta(journal_pcode, volume, issue)


def download_light():
    journal_pcode = 'lsa'
    # Vol.1 released in 2012, starting from issue 3
    for volume in range(2, 7):
        for i in range(12):
            issue = i + 1
            download_issue_meta(journal_pcode, volume, issue)

    volume = 7
    for i in range(5):
        issue = i + 1
        download_issue_meta(journal_pcode, volume, issue)

    volume = 1
    for i in range(2, 12):
        issue = i + 1
        download_issue_meta(journal_pcode, volume, issue)


def download_nanotechnology():
    journal_pcode = 'nnano'
    for volume in range(2, 15):
        for i in range(12):
            issue = i + 1
            download_issue_meta(journal_pcode, volume, issue)

    volume = 15
    for i in range(5):
        issue = i + 1
        download_issue_meta(journal_pcode, volume, issue)

    # Vol.1 released in 2006, issue 1 - 3
    volume = 1
    for i in range(3):
        issue = i + 1
        download_issue_meta(journal_pcode, volume, issue)


def download_physics():
    # Vol.1 released in 2005, issue 1 - 3
    vol_cnt = 16
    journal_pcode = 'nphys'
    vol1_issues = range(3)

    for volume in range(2, vol_cnt):
        for i in range(12):
            issue = i + 1
            download_issue_meta(journal_pcode, volume, issue)

    volume = vol_cnt
    for i in range(5):
        issue = i + 1
        download_issue_meta(journal_pcode, volume, issue)

    volume = 1
    for i in vol1_issues:
        issue = i + 1
        download_issue_meta(journal_pcode, volume, issue)


if __name__ == '__main__':
    download_nphoton()
    # download_light()
    # download_physics()
    # download_nanotechnology()
