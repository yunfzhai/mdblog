title: Flask的一些偏门
summary: g对象、静态文件的使用
authors: yanfzhai
date: 2017-12-15
tags: python Flask


# **Flask中的g对象**

Flask中的g对象是个很好的东西，主要用于在一个请求的过程中共享数据。可以随意给g对象添加属性来保存数据，非常的方便，下面的代码是一个使用g对象的例子。下面的这个例子会使用random随机产生一个0~9的整数，并使用g.x保存并记录debug日志:


```python
# encoding=utf-8
from flask import Flask,g
import random

app = Flask(__name__)

@app.before_request 
def set_on_g_object():
    x = random.randint(0,9)
    app.logger.debug('before request g.x is {x}'.format(x=x))
    g.x = x

@app.route("/") 
def test():
    g.x=1000
    return str(g.x)

@app.after_request 
def get_on_g_object(response):
    app.logger.debug('after request g.x is{g.x}'.format(g=g)) 
    return response
```

# Flask中静态文件的处理

### 1.add_url_rule的用法

Flask中提供了url_for来实现创建url，只是生成一个url。在前面的博文中谈论过如果要生成一个css样式的静态文件的url需要使用url_for('static',filename='style.css')来创建相应的url。但是如果我有一个目录attachment的目录存放一些文件的话是没法通过url_for来生成的，默认url_for只可以为static和一些view_func建立url如果要想通过url_for为attachment来添加url就必须添加一个add_url_rule。

```python
# encoding=utf-8
from flask import Flask 
from flask import g 
from flask import send_from_directory 
from flask import url_for 
import random

app = Flask(__name__)

@app.route("/") 
def test(): 
    return "url创建方式一"

def hello(): 
    return "url创建方式二" 

app.add_url_rule("/index/",endpoint="hello",view_func=hello)

@app.route('/url1') 
def Create_url1(): 
    return url_for('static',filename="style.css")

app.add_url_rule('/attachment/<path:filename>',endpoint='attachment',build_only=True)
@app.route('/url2') 
def Create_url2(): 
    return url_for('attachment',filename="upload.txt")

```

### 2.send_from_directory的用法

send_from_directory主要用于下载文件：
下面是一个文件的下载实例

```python

# encoding=utf-8
from flask import Flask 
from flask import g 
from flask import send_from_directory 
from flask import url_for import os.path

app = Flask(__name__)
dirpath = os.path.join(app.root_path,'upload')
@app.route("/download/<path:filename>") 
def downloader(filename): 
    return send_from_directory(dirpath,filename,as_attachment=True)

```

首选在application下建立一个upload目录，构造upload目录的绝对路径。
然后通过浏览器输入指定文件的文件名来下载。
### 3.static_url_path和static_folder的用法

static_url_path主要用于改变url的path的，静态文件放在static下面，所以正常情况url是static/filename ，但是可以通过static_url_path来改变这个url

static_folder主要是用来改变url的目录的，默认是static，可以通过这个变量来改变静态文件目录。

```python

# encoding=utf-8
from flask import Flask 
from flask import g 
from flask import send_from_directory 
from flask import url_for 
import os.path
app = Flask(__name__,static_url_path="/test")
@app.route("/") 
def static_create(): 
    return url_for('static',filename='style.css')

```

### 4.静态页面缓存和文件索引
SEND_FILE_MAX_AGE_DEFAULT 这个变量用于配置静态文件缓存的时间，Flask默认缓存时间是12hours
例如:app.comfig['SEND_FILE_MAX_AGE_DEFAULT']=2592000 将其缓存时间改为了30天。
Flask不能实现文件索引的功能，也就是无法列出文件名，这个需要web server(Nginx 或 Apache)来实现。
### 5、session 对象
session 也是一个 request context 的变量，但它把数据保存到了 cookie 中并发送到了客户端，客户端再次请求的时候又带上了cookie
