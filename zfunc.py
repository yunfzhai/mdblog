import pypinyin
from datetime import datetime
import os
import codecs
import shelve

TAG_HTML_TEMPLATE = u"<a href='/tag/{tag}/' class='tag-index'>{tag}</a>"
AUTHOR_HTML_TEMPLATE = u"<a href='' class='tag-index'>{author}</a>"
TITLE_HTML_TEMPLATE = u"<div class='sidebar-module-inset'><h5 class='sidebar-title'><i class='icon-circle-blank side-icon'></i>标题</h5><p>{title_str}</p></div>"
def decode_str(str_,info):
    return codecs.decode(str_, "gb2312") if info['pyversion'] == "2" else str_

def str2pinyin(hans, nameset,style=pypinyin.FIRST_LETTER):
    #字符串转拼音，默认只获取首字母
    pinyin_str = pypinyin.slug(hans, style=style, separator="")
    num = 2
    while pinyin_str in nameset:
        pinyin_str += str(num)
        num += 1
    return pinyin_str

def parse_time(timestamp, pattern="%Y-%m-%d %H:%M:%S"):
    #解析时间
    return datetime.fromtimestamp(timestamp).strftime(pattern)

def index_tags(tags, fid,info):
    # 为标签倒排索引添加标签,fid是拼音名字
    for tag in tags:
        if tag in info['tag_index']:
            info['tag_index'][tag].append(fid)
        else:
            info['tag_index'][tag] = [fid]

def dump_index(info):
    # """持久化索引信息
    dat = shelve.open(info['index_dat'])
    dat["article_index"] =  info['article_index']
    dat["tag_inverted_index"] =  info['tag_index']
    dat["author_inverted_index"] =  info['author_index']
    dat.close()

def index_authors(authors, fid,info):
    # """为作者倒排索引添加作者，fid是拼音name
    for author in authors:
        if author in info['author_index']:
             info['author_index'][author].append(fid)
        else:
             info['author_index'][author] = [fid]

def save_html(out_path, html):
    # """保存html至文件
    base_folder = os.path.dirname(out_path)
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
    with codecs.open(out_path, "w+", "utf-8") as f:
        f.write(html)

def create_index(md_file, meta,_current_file_index,info):
    #创建索引信息    # :param filename: 文件从INPUT_CONTENT开始的全路径
    # :param meta:     :type meta: dict ,_current_file_index 是拼音name
    filename = decode_str(md_file,info)
    index_tags(meta.get("tags", []), _current_file_index,info)
    index_authors(meta.get("authors", []), _current_file_index,info)
    title = meta.get("title", [""])[0]
    if title == "":
        title = os.path.splitext(os.path.basename(filename))[0]

    publish_dates = meta.get("publish_date", [])
    if len(publish_dates) == 0:
        publish_date = parse_time(os.path.getctime(filename), "%Y-%m-%d")
    else:
        publish_date = publish_dates[0]

    info['article_index'][_current_file_index] = {
        "filename": filename,
        "modify_time": parse_time(os.path.getmtime(filename)),
        "title": title,
        "summary": meta.get("summary", [u""])[0],
        "authors": meta.get("authors", [u"匿名"]),
        "publish_date": publish_date,
        "tags": meta.get("tags", [])
    }

def render_tags_html(tags):
    # """渲染tags的html
    tags_html = ""
    for tag in tags:
        tags_html += TAG_HTML_TEMPLATE.format(tag=tag)
    return tags_html

def render_authors_html(authors):
    # """渲染作者html
    authors_html = ""
    for author in authors:
        authors_html += AUTHOR_HTML_TEMPLATE.format(author=author)
    return authors_html


def render_title_html(title):
    # """渲染标题html
    title_html = ""
    if title.strip() != "":
        title_html = TITLE_HTML_TEMPLATE.format(title_str=title)
    return title_html