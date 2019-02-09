import urllib.request as ur
import re
import json
from flask import Flask
from flask import render_template
from flask import request

def openF(way):
    text = open(way, 'r', encoding='utf-8')
    f = text.read()
    text.close()
    regex = '-lexeme\\\n lex: (.*?)\\\n .*? gramm: (.*?)\\\n .*? trans_ru: (.*?)\\\n'
    res = re.findall(regex, f, flags=re.DOTALL)
    if res:
        d = {}
        for elem in res:
            a = []
            a.append(elem[1])
            a.append(elem[2])
            a = tuple(a)
            d[elem[0]] = a
        fj = open('data.json', 'a', encoding='utf-8')
        json.dump(d, fj)
        fj.close()
        return d

def openJ(ud):
    rd = {}
    for k,v in ud.items():
        a = str(k) + "', '" + str(v[0])
        rd[v[1]] = a
    fj = open('dataRus.json', 'a', encoding='utf-8')
    json.dump(rd, fj)
    fj.close()


def main():
    filenames = ['udm_lexemes_ADJ.txt', 'udm_lexemes_IMIT.txt']
    fjs = open('data.json', 'w', encoding='utf-8')
    fjs.close()
    a = []
    dict = {}
    for elem in filenames:
        d0 = openF(elem)
        dict.update(d0)
    print(dict)
    ftxt = open('data.txt', 'w', encoding='utf-8')
    ftxt.write(str(dict))
    ftxt.close()
    openJ(dict)

app = Flask(__name__)

@app.route('/')
def index1():
    if request.args:
        uW = request.args['req']
    return render_template('formaS.html')

@app.route ('/results')
def index2():
    text = open('data.txt', 'r', encoding='utf-8')
    f = text.read()
    text.close()
    requ = request.args['req']
    regex = "'requ': ('.*?', '(.*?)'),"
    mac = re.findall(regex, f, flags=re.I)
    if mac:
        return render_template('formaReq.html', req=mac)

if __name__ == '__main__':
    main()
    app.run(debug='true')