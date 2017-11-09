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

info={}
# 相关目录
info['static_root'] = "/static/"
info['indir'],info['outdir'] = "./in/", "./static/out/"
# 索引文件
info['index_dat']= "./static/out/index.dat"
info['pyversion'] = "3" if sys.version >= "3" else "2"
info['tag_index'],info['author_index'],info['article_index']={},{},{}
info['pinyin_name'] = set()

env = Environment(loader=FileSystemLoader("templates"))
TAG_HTML_TEMPLATE = u"<a href='/tag/{tag}/' class='tag-index'>{tag}</a>"
AUTHOR_HTML_TEMPLATE = u"<a href='' class='tag-index'>{author}</a>"
TITLE_HTML_TEMPLATE = u"<div class='sidebar-module-inset'><h5 class='sidebar-title'><i class='icon-circle-blank side-icon'></i>标题</h5><p>{title_str}</p></div>"


########---------------function---------------------############

def render(md_file,pinyname):
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
        create_index(md_file, meta,pinyname,info)

        template = env.get_template("base_article.html")
        text = template.render(
            blog_content=html,
            static_root=info['static_root'],
            title=info['article_index'][pinyname].get("title"),
            title_html=render_title_html(info['article_index'][pinyname].get("title")),
            summary=info['article_index'][pinyname].get("summary", ""),
            authors=render_authors_html(info['article_index'][pinyname].get("authors")),
            tags=render_tags_html(info['article_index'][pinyname].get("tags")),
            toc=toc,
        )
    return text    
# 第一步,清理输出文件夹，扫描输入md文件
def clear_scan():
    if os.path.exists(info['outdir']):
        shutil.rmtree(info['outdir'])
    mdfiles = []
    pinyin_names=set()    
    for root, dirs, files in os.walk(info['indir']):   #遍历文件夹的所有文件
        for f in files:
            if os.path.splitext(f)[1].lower() == ".md":
                mdfiles.append(os.path.join(root, f))
    info['mdfiles'] = mdfiles            

def each_file(mdfile):
    file_base_name = os.path.splitext(os.path.basename(mdfile))[0]   #file_base_name是文件名，不带扩展名的
    _current_file_index = str2pinyin(decode_str(file_base_name,info),info['pinyin_name'])
    info['pinyin_name'].add(_current_file_index)
    out_path = os.path.join(info['outdir'], _current_file_index + ".html")
    html = render(mdfile,_current_file_index)
    save_html(out_path, html)


def convertall():
    for f in info['mdfiles']:
        each_file(f)
    dump_index(info)


if __name__ == "__main__":
    clear_scan()
    convertall()

