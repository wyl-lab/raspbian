from flask import Flask
from flask import escape
from flask import url_for

app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1>Hello Totoro!</h1>  \
    <img src=" http://helloflask.com/totoro.gif ">'

@app.route('/home')
def home():
    return '欢迎来到智能家居系统'

@app.route('/home/camera')
def camera():
    return '实时影像链接'

@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % escape(name)

@app.route('/userEscape/<name>')
def userEscape(name):
    return '欢迎你,%s' % escape(name)

@app.route('/test1')
def test1_url_for():
    # 下面是一些调用示例（请在命令行窗口查看输出的 URL）：
    print(url_for('hello'))  # 输出：/
    # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
    url = url_for('userEscape', name='wyl')
    
    print('url :' + url)  # 输出：/user/wyl
    print(url_for('userEscape', name='zxp'))  # 输出：/user/zxp
    print(url_for('test1_url_for'))  # 输出：/test

    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
    print(url_for('test1_url_for', num=2))  # 输出：/test?num=2
    return 'Test page'

