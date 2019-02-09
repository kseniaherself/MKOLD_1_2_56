from flask import Flask
from flask import render_template
from flask import request
#from flask import redirect, url_for
import re
import json
from collections import Counter

app = Flask(__name__)

@app.route('/')
def index1():
    if request.args:
        text = open('data.csv', 'a', encoding='utf-8')
        text.write(request.args['gender'] + '\t' + request.args['age'] + '\t' +
                        request.args['name'] + '\t' + request.args['friend'] + '\t' +
                        request.args['enemy'] + '\t' + request.args['neighbour'] + '\t' +
                        request.args['stranger'] + '\t' + request.args['guest'] + '\t' +
                        request.args['host'] + '\n')
        text.close()
    return render_template('formaQ.html')

@app.route ('/stats')
def index2():
    text = open('data.csv', 'r', encoding='utf-8')
    f = text.readlines()
    text.close()
    mask = 0
    UAF = 0
    UAM = 0
    MAF = 0
    MAM = 0
    EF = 0
    EM = 0
    AM = 0
    AF = 0
    fem = 0
    stranger = []
    for line in f:
        l = line.split('\t')
        stranger.append(l[6])
        if l[0] == 'мужской':
            mask += 1
            if l[1]=='under18':
                UAM +=1
            else:
                if l[1] == '18-35':
                    MAM += 1
                else:
                    if l[1]== '36-50':
                        EM += 1
                    else:
                        AM += 1
        else:
            fem += 1
            if l[1] == 'under18':
                UAF += 1
            else:
                if l[1] == '18-35':
                    MAF += 1
                else:
                    if l[1] == '36-50':
                        EF += 1
                    else:
                        AF += 1
    fm = round((fem/mask)*100, 2)
    cntr = Counter(stranger)
    mc = Counter.most_common(cntr, 2)
    ind = []
    for elem in mc:
        for el in elem:
            ind.append(el)
    for element in ind:
        a1 = ind[0]
        a2 = ind[1]
        a3 = ind[2]
        a4 = ind[3]
    return render_template('formaStats.html', fm=fm, UAF=UAF, UAM=UAM, MAF=MAF, MAM=MAM,
                           EF=EF, EM=EM, AM=AM, AF=AF, a1 = a1, a2 = a2, a3 = a3, a4 = a4)

@app.route('/json')
def index3():
    text = open('data.csv', 'r', encoding='utf-8')
    f = text.read()
    text.close()
    ff = f.split('\n')
    a=[]
    for elem in ff:
        a.append(elem.split('\t'))
    jsonStr = json.dumps(a, ensure_ascii = False)
    return render_template('formaJ.html', js = jsonStr)

@app.route('/search')
def index4():
    return render_template('formaSzuk.html')

@app.route('/results')
def index5():
    text = open('data.csv', 'r', encoding='utf-8')
    f = text.read()
    text.close()
    a = f.split()
    if request.args:
        requ = request.args['req']
        mac = re.findall(requ, f)
        i = 0
        if mac:
            for elem in mac:
                i += 1
            req1 = 'ваше слово встречается '+str(i)
        else:
            req1 = 'никто из пользователей не предлагал такой перевод какого-либо слова'
        return render_template('formaResults.html', req1=req1)

if __name__ == '__main__':
    app.run()