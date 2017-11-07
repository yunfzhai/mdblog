# -*- coding:utf-8 -*-

"""Documentation"""
import shutil
import os
import codecs
import shelve
import sys
from jinja2 import Environment, FileSystemLoader
from markdown import Markdown
from zfunc import *

STATIC_ROOT = "/static/"
INPUT_CONTENT,OUTPUT_CONTENT = "./in/", "./static/out/"
# 索引文件
INDEX_DAT = "./static/out/index.dat"
env = Environment(loader=FileSystemLoader("templates"))

PY_VERSION = "3" if sys.version >= "3" else "2"
# 标签倒排索引
TAG_INVERTED_INDEX = {}
# 作者倒排索引
AUTHOR_INVERTED_INDEX = {}
# 文章索引
ARTICLE_INDEX = {}

_pinyin_names = set()

TAG_HTML_TEMPLATE = u"<a href='/tag/{tag}/' class='tag-index'>{tag}</a>"
AUTHOR_HTML_TEMPLATE = u"<a href='' class='tag-index'>{author}</a>"
TITLE_HTML_TEMPLATE = u"<div class='sidebar-module-inset'><h5 class='sidebar-title'><i class='icon-circle-blank side-icon'></i>标题</h5><p>{title_str}</p></div>"


########---------------function---------------------############

def create_index(filename, meta):
    #创建索引信息
    # :param filename: 文件从INPUT_CONTENT开始的全路径
    # :param meta:     :type meta: dict
    filename = decode_str(filename)
    index_tags(meta.get("tags", []), _current_file_index)
    index_authors(meta.get("authors", []), _current_file_index)
    title = meta.get("title", [""])[0]
    if title == "":
        title = os.path.splitext(os.path.basename(filename))[0]

    publish_dates = meta.get("publish_date", [])
    if len(publish_dates) == 0:
        publish_date = parse_time(os.path.getctime(filename), "%Y-%m-%d")
    else:
        publish_date = publish_dates[0]

    ARTICLE_INDEX[_current_file_index] = {
        "filename": filename,
        "modify_time": parse_time(os.path.getmtime(filename)),
        "title": title,
        "summary": meta.get("summary", [u""])[0],
        "authors": meta.get("authors", [u"匿名"]),
        "publish_date": publish_date,
        "tags": meta.get("tags", [])
    }

def render(md_file):
    #渲染html页面 :param md_file::return:
    with codecs.open(md_file, "r", "utf-8") as f:
        text = f.read()
        md = Markdown(
            extensions=[
                "fenced_code",
                "codehilite(css_class=highlight,linenums=None)",
                "meta",
                "admonition",
                "tables",
                "toc",
                "wikilinks",
            ],
        )
        html = md.convert(text)
        meta = md.Meta if hasattr(md, "Meta") else {}
        toc = md.toc if hasattr(md, "toc") else ""
        create_index(md_file, meta)

        template = env.get_template("base_article.html")
        text = template.render(
            blog_content=html,
            static_root=STATIC_ROOT,
            title=ARTICLE_INDEX[_current_file_index].get("title"),
            title_html=render_title_html(ARTICLE_INDEX[_current_file_index].get("title")),
            summary=ARTICLE_INDEX[_current_file_index].get("summary", ""),
            authors=render_authors_html(ARTICLE_INDEX[_current_file_index].get("authors")),
            tags=render_tags_html(ARTICLE_INDEX[_current_file_index].get("tags")),
            toc=toc,
        )
    return text    
# 第一步,清理输出文件夹，扫描输入md文件
def step1(outdir,indir):
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    mdfiels = []
    pinyin_names=[]    
    for root, dirs, files in os.walk(indir):   #遍历文件夹的所有文件
        for f in files:
            if os.path.splitext(f)[1].lower() == ".md":
                mdfiels.append(os.path.join(root, f))
    for f in mdfiels:
        file_base_name = os.path.splitext(os.path.basename(f))[0]   #file_base_name是文件名，不带扩展名的
        _current_file_index = str2pinyin(codecs.decode(file_base_name, "gb2312") if PY_VERSION == "2" else file_base_name)
        
        pinyin_names.add(_current_file_index)
        print('now check: '+f)
        out_path = os.path.join(outdir, _current_file_index + ".html")
        html = render(f)
        save_html(out_path, html)
    dump_index()


def generate():
    _reload_global()
    clean()
    load_md_files(INPUT_CONTENT) #全局变量，指定为 ./in/
    scan_md()
    dump_index()
    pass


if __name__ == "__main__":
    generate()
    pass
