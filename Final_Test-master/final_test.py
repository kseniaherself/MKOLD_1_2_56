import re
import urllib.request
import os

def download_page():
    page_url = 'http://web-corpora.net/Test2_2016/short_story.html'
    try:
        req = urllib.request.Request(page_url)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
        regScript = re.compile('<script>.*?</script>', flags=re.U | re.DOTALL)
        regComment = re.compile('<!--.*?-->', flags=re.U | re.DOTALL)
        clean_text = regScript.sub(" ", html)
        clean_text = regComment.sub(" ", clean_text)
        clean_text = regTag.sub(" ", clean_text)
        clean_text = clean_text.replace('&nbsp;', ' ')
        clean_text = clean_text.replace('&quot;', '"')
        data = re.sub('&.*?;', '', clean_text)
        return data
    except:
        print('Error at', page_url)
        return

def page_search(data):
    f = open('wordslist.txt', 'w', encoding='utf-8')
    f.close()
    i = 0
    arr_S = []
    data = data.split()
    #print('Задание 1:')        #можно раскомментировать для красоты, под этой записью выпадет список слов из задания 1
    for word in data:
        res = re.search(r'\b([сС].*?)\b', word)
        if res:
            i += 1
            arr_S.append(res.group(1))
            #print(res.group(1))    #другой способ вывода на экран
    f = open('wordslist.txt', 'a', encoding='utf-8')
    for elem in arr_S:
        f.write(str(elem) + ' ')
        print(str(elem))
    f.close()

def mystem_taxt():
    f = open('mystemF.txt', 'w', encoding='utf-8')
    f.close()
    os.system('./mystem -ncid wordslist.txt mystemF.txt')

def verbs_search():
    f = open('mystemF.txt', 'r', encoding='utf-8')
    text = f.readlines()
    f.close()
    #print('Задание 2:')        #если раскомментировать, будет наглядно где начинается список слов из второго задания
    for line in text:
        res1 = re.match('.*(=V).*', line)
        if res1:
            regex2 = '(.*?){.*?'
            res2 = re.search(regex2, line)
            print(res2.group(1))

def main ():
    val1 = download_page()
    val2 = page_search(val1)
    val3 = mystem_taxt()
    val4 = verbs_search()

main()