# -*- coding:utf-8 -*-
import shutil
import os
import codecs
import shelve
import sys
from jinja2 import Environment, FileSystemLoader
from markdown import Markdown
import pypinyin
from datetime import datetime



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
def decode_str(str_,info):
    return codecs.decode(str_, "gb2312") if info['pyversion'] == "2" else str_

def str2pinyin(hans, nameset,style=pypinyin.FIRST_LETTER):    #字符串转拼音，默认只获取首字母
    pinyin_str = pypinyin.slug(hans, style=style, separator="")
    num = 2
    while pinyin_str in nameset:
        pinyin_str += str(num)
        num += 1
    return pinyin_str

def parse_time(timestamp, pattern="%Y-%m-%d %H:%M:%S"):     #解析时间
    return datetime.fromtimestamp(timestamp).strftime(pattern)
    
def index_tags_authors(tags,authors,fid,info):     # 为标签倒排索引添加标签,fid是拼音名字,为作者倒排索引添加作者，fid是拼音name
    for tag in tags:
        if tag in info['tag_index']:
            info['tag_index'][tag].append(fid)
        else:
            info['tag_index'][tag] = [fid]
    for author in authors:
        if author in info['author_index']:
             info['author_index'][author].append(fid)
        else:
             info['author_index'][author] = [fid]

def dump_index(info):     # """持久化索引信息
    dat = shelve.open(info['index_dat'])
    dat["article_index"] =  info['article_index']
    dat["tag_inverted_index"] =  info['tag_index']
    dat["author_inverted_index"] =  info['author_index']
    dat.close()


def save_html(out_path, html):     # """保存html至文件
    base_folder = os.path.dirname(out_path)
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
    with codecs.open(out_path, "w+", "utf-8") as f:
        f.write(html)

def render(md_file,pinyname):     #渲染html页面 :param md_file::return:
    with codecs.open(md_file, "r", "utf-8") as f:
        text = f.read()
        md = Markdown(extensions=[ "fenced_code", "codehilite(css_class=highlight,linenums=None)","meta","admonition","tables","toc","wikilinks",])
        html = md.convert(text)
        meta = md.Meta if hasattr(md, "Meta") else {}
        toc = md.toc if hasattr(md, "toc") else ""

    filename = decode_str(md_file,info)
    index_tags_authors(meta.get("tags", []),meta.get("authors", []),pinyname,info)
    title = meta.get("title", [os.path.splitext(os.path.basename(filename))[0]])[0]
    publish_date = meta.get("date", [parse_time(os.path.getctime(md_file), "%Y-%m-%d")])[0]
    info['article_index'][pinyname] = {
        "filename": filename,
        "modify_time": parse_time(os.path.getmtime(filename)),
        "title": title,
        "summary": meta.get("summary", [u""])[0],
        "authors": meta.get("authors", [u"匿名"]),
        "publish_date": publish_date,
        "tags": meta.get("tags", [])
    }

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
    filename = os.path.splitext(os.path.basename(mdfile))[0]   #file_base_name是文件名，不带扩展名的
    filename_py = str2pinyin(decode_str(filename,info),info['pinyin_name'])
    info['pinyin_name'].add(filename_py)
    out_path = os.path.join(info['outdir'], filename_py + ".html")
    html = render(mdfile,filename_py)
    save_html(out_path, html)


def convertall():
    for f in info['mdfiles']:
        each_file(f)
    dump_index(info)


def render_tags_html(tags):     # """渲染tags的html
    tags_html = ""
    for tag in tags:
        tags_html += TAG_HTML_TEMPLATE.format(tag=tag)
    return tags_html

def render_authors_html(authors):     # """渲染作者html
    authors_html = ""
    for author in authors:
        authors_html += AUTHOR_HTML_TEMPLATE.format(author=author)
    return authors_html


def render_title_html(title):    # """渲染标题html
    title_html = ""
    if title.strip() != "":
        title_html = TITLE_HTML_TEMPLATE.format(title_str=title)
    return title_html

if __name__ == "__main__":
    clear_scan()
    convertall()

