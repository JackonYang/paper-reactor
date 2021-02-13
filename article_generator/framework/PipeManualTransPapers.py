import os
import csv

from .article_pipeline_base import ArticlePipelineBase

article_tmpl = {
    # 'title': 'string',
    # 'digest': 'brief introduction',
    # 'content': content,
    # 'thumb_media_id': 'kydwHY6c4LpYQ6QJIoazsO8R5Ofmp_2IfRd1pSHDQjQ',
    # 'author': settings.author,
    'show_cover_pic': 0,
    'content_source_url': '',
    # 'need_open_comment': 1,
    # 'only_fans_can_comment': 0,
}


class PipeManualTransPapers(ArticlePipelineBase):

    def iter_tasks(self):
        input_data_dir = os.path.join(
            self.config_dir, 'manual-trans-files'
        )
        en_filename_ptn = os.path.join(
            self.project_data_dir,
            'rawdata/nature/%(journal_pcode)s/%(journal_pcode)s-volume%(volume)02d-issue%(issue)02d.csv'
        )
        for trans_filename in sorted(os.listdir(input_data_dir)):
            full_path = os.path.join(input_data_dir, trans_filename)

            cn_papers = self.read_txt(full_path)

            # find en_issue
            basename = os.path.basename(trans_filename)
            journal_pcode, volume_str, issue_str, author = basename.split('-')
            issue_int = int(issue_str[-2:])
            volume_int = int(volume_str[-2:])
            _kwargs = {'journal_pcode': journal_pcode, 'volume': volume_int, 'issue': issue_int}

            en_papers_map = {}

            # read en papers and meta info
            en_filename = en_filename_ptn % _kwargs
            with open(en_filename) as csvfile:
                reader = csv.DictReader(csvfile)
                for p in reader:
                    en_papers_map[p['url'].strip()] = p
                    en_papers_map[p['doi_url'].strip()] = p

            # match cn with en papers
            trans_papers = []
            for p_cn in cn_papers:
                p_en = en_papers_map[p_cn['url'].strip()]
                p_cn.update(p_en)
                trans_papers.append(p_cn)

            # get titles to build table of contents section
            paper_titles = {}
            for idx, p in enumerate(trans_papers):
                contentType = p['contentType'].title() + 's'
                if contentType not in paper_titles:
                    paper_titles[contentType] = []

                t_en = p['title']
                t_cn = p['title_atifical_translation']
                paper_titles[contentType].append({
                    'title': t_en,
                    'title_en': t_en,
                    'title_cn': t_cn,
                })
            paper_titles_sorted = []
            idx = 1
            for sec, pts in paper_titles.items():
                pts_sorted = []
                for p in pts:
                    p['seq'] = idx
                    pts_sorted.append(p)
                    idx += 1
                paper_titles_sorted.append([sec, pts_sorted])

            journal_title = trans_papers[0]['journal_title'].title()
            task_meta = {
                'journal_title': journal_title,
                'journal_pcode': journal_pcode,
                'year': 2020,
                'volume': volume_int,
                'issue': issue_int,
                'author': author,
                'papers': trans_papers,
                'paper_titles': paper_titles_sorted,
            }

            yield task_meta

    def render_task_article(self, task_meta):
        content = {}  # common_args.copy()
        content.update(task_meta)
        content.update({
            'year_issue': '%(year)s.%(issue)02d' % task_meta,
        })

        filename = 'trans-%(journal_pcode)s-%(year)s-%(issue)s.html' % task_meta
        tmpl_name = 'trans_%(journal_pcode)s_tmpl.html' % task_meta

        # thumb_media_id = settings.thumb_ids['trans_%s_logo' % task_meta['journal_pcode']]['media_id']
        title = '%(journal_title)s 论文导读 -- %(year)s.%(issue)02d Vol.%(volume)s Issue %(issue)s' % task_meta
        brief = '光学领域国际顶级学术期刊. %(year)s.%(issue)s 月刊论文导读' % task_meta

        content = self.render(template=tmpl_name, filename=filename, **content)

        article = article_tmpl.copy()
        article.update({
            'title': title,
            'author': task_meta['author'],
            'digest': task_meta.get('brief', brief),
            'content': content,
            # 'thumb_media_id': thumb_media_id,
        })

        return article

    def read_txt(self, filename):
        data = []
        record_fields = [
            'url',
            'title',
            'abstract',
            'title_atifical_translation',
            'abstract_atifical_translation',
        ]
        with open(filename) as fr:
            record_values = []
            for row in fr:
                if row.startswith('------'):
                    data.append({k: v for k, v in zip(record_fields, record_values)})
                    record_values = []
                elif len(row.strip()) > 0:
                    record_values.append(row.strip())
            if len(record_values) > 0:
                data.append({k: v for k, v in zip(record_fields, record_values)})

        print('%s papers found in %s' % (len(data), filename))
        return data
