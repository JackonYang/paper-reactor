# paper-reactor

科技论文的下载、数据清洗与信息提取，试着碰撞一下好玩的思路💥


## Paper-Pipeline Design

这是最完整的流程设计，不同的期刊和处理目的，可以跳过其中一些步骤。

1. downloader(including parsering)
2. cleaner
3. normalizer
4. filler
5. merger
6. sinker

#### nature.com pipeline

```bash
# download new papers
python3 downloader/nature_downloaders/download_nature.py
# translate using google API
proxychains4 -q python3 filler/translator/trans_papers.py
# merge issuely files into one
python3 merger/nature/merge_issuely_csv_files.py
```

analysis

```bash
python3 analyzer/topic_photonics/data_insights/list_paper_types.py > docs/nature/contentType-list.md
```

upload to 黑帕云

渣渣 API，大约需要等待 30 min 才能上传 5000 条数据。

```bash
python3 tools/upload_papers_to_hipacloud.py
```

下面的方法，效率更低，放弃。

```bash
rm -rf tmp-data && mkdir tmp-data && split -l 520 paper-data/merged/nature/nature_papers_merged_long_paper.csv tmp-data/long_paper_part
```

网站的导入能力极差，先苟一下。

```bash
# list article type
python3 analyzer/topic_photonics/data_insights/list_paper_types.py > docs/nature/contentType-list.md
```

翻译速度：

1. 调用 Google translate API，安全起见，间隔 5 秒。
2. 一篇文章翻译 2 个字段 ：title/abstract，需 10 秒。
3. 一小时可以翻译 360 篇文章。全量文章共 10k 篇，大约需要 30 小时。


## Setup

```bash
pip3 install -r requirements.txt
```
