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
python downloader/nature_downloaders/download_nature.py
# translate using google API
proxychains4 -q python filler/translator/trans_papers.py
# merge issuely files into one
python merger/nature/merge_issuely_csv_files.py
```


## Setup

```bash
pip3 install -r requirements.txt
```
