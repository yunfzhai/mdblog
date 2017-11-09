# ---------------------------------------
from markdown import Markdown
import codecs
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
    
with codecs.open('./in/About.md', "r", "utf-8") as f:
    text = f.read()     
    html = md.convert(text)
    print(md.Meta)