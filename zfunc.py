import pypinyin
from datetime import datetime

def str2pinyin(hans, style=pypinyin.FIRST_LETTER):
    #字符串转拼音，默认只获取首字母
    pinyin_str = pypinyin.slug(hans, style=style, separator="")
    num = 2
    while pinyin_str in _pinyin_names:
        pinyin_str += str(num)
        num += 1
    return pinyin_str

def parse_time(timestamp, pattern="%Y-%m-%d %H:%M:%S"):
    #解析时间
    return datetime.fromtimestamp(timestamp).strftime(pattern)

def index_tags(tags, fid):
    # 为标签倒排索引添加标签
    for tag in tags:
        if tag in TAG_INVERTED_INDEX:
            TAG_INVERTED_INDEX[tag].append(fid)
        else:
            TAG_INVERTED_INDEX[tag] = [fid]
def dump_index():
    # """持久化索引信息
    dat = shelve.open(INDEX_DAT)
    dat["article_index"] = ARTICLE_INDEX
    dat["tag_inverted_index"] = TAG_INVERTED_INDEX
    dat["author_inverted_index"] = AUTHOR_INVERTED_INDEX
    dat.close()




def index_authors(authors, fid):
    # """为作者倒排索引添加作者
    for author in authors:
        if author in AUTHOR_INVERTED_INDEX:
            AUTHOR_INVERTED_INDEX[author].append(fid)
        else:
            AUTHOR_INVERTED_INDEX[author] = [fid]


def save_html(out_path, html):
    # """保存html至文件
    base_folder = os.path.dirname(out_path)
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    with codecs.open(out_path, "w+", "utf-8") as f:
        f.write(html)


def render_tags_html(tags):
    """渲染tags的html
    """
    tags_html = ""
    for tag in tags:
        tags_html += TAG_HTML_TEMPLATE.format(tag=tag)
    return tags_html


def render_authors_html(authors):
    """渲染作者html
    """
    authors_html = ""
    for author in authors:
        authors_html += AUTHOR_HTML_TEMPLATE.format(author=author)
    return authors_html


def render_title_html(title):
    """渲染标题html
    """
    title_html = ""
    if title.strip() != "":
        title_html = TITLE_HTML_TEMPLATE.format(title_str=title)
    return title_html


