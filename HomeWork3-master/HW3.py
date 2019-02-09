import urllib.request as ur
import re

def freqL(words):
    dictionary = {}
    for word in words:
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1
    return dictionary

def sets(text, regex):
    res = str(re.findall(regex, text, flags=re.DOTALL))
    regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
    regComment = re.compile('<!--.*?-->', flags=re.U | re.DOTALL)
    regS = re.compile('\\\.', flags=re.U)
    regSp = re.compile(' +')
    regPunct = re.compile("\\,|\\.|\\!|\\?|\\[|\\]|\\'")
    clean_t = regPunct.sub(' ', res)
    clean_t = regComment.sub('', clean_t)
    clean_t = regTag.sub(' ', clean_t)
    clean_t = regS.sub(' ', clean_t)
    clean_t = regSp.sub(' ', clean_t)
    s = clean_t.lower()
    s = s.split(' ')
    for elem in s:
        if elem == '':
            s.remove(elem)
    frL = freqL(s)
    set0 = set(s)
    #if '' in set0:
    #   set0.remove('')
    return set0, frL

def arr0(el1):
    url = el1
    response = ur.urlopen(url)
    text = response.read().decode('utf-8')
    regex = 'class="js-mediator-article">(.*)<p style="margin-bottom:10px;"><b>Ульяна Леденева </b></p>'
    set0 = sets(text, regex)
    return set0

def arr1(el1):
    url = el1
    response = ur.urlopen(url)
    text = response.read().decode('utf-8')
    regex = '<p>&nbsp;</p>(.*?)</div>'
    set0 = sets(text, regex)
    return set0

def arr2(el1):
    url = el1
    response = ur.urlopen(url)
    text = response.read().decode('windows-1251')
    regex = 'style="display:inline;">(.*?)</div>'
    set0 = sets(text, regex)
    return set0

def arr3(el1):
    url = el1
    response = ur.urlopen(url)
    text = response.read().decode('UTF-8')
    regex = "<div class='summary2' itemprop='headline description'>(.*?)<div style=\"margin: 5px; 0\">"
    set0 = sets(text, regex)
    return set0

def commonW(s1, s2, s3, s4):
    text = open('commonWords.txt', 'w', encoding='utf-8')
    a = s1 & s2 & s3 & s4
    l = list(a)
    l.sort()
    for elem in l:
        text.write(elem + '\n')
    text.close()

def uniqE(s1, s2, s3, s4):
    text = open('uniqWords.txt', 'w', encoding='utf-8')
    a = s1 ^ s2 ^ s3 ^ s4
    l = list(a)
    l.sort()
    x = []
    y = set()
    for elem in l:
        x.append(elem)
        y.add(elem)
        text.write(elem + '\n')
    text.close()
    return x, y     #x массив общих слов в алфавитном порядке. y – множество

def commonFreq(uniqSet, frq1, frq2, frq3, frq4):
    frq1.update(frq2)
    frq1.update(frq3)
    frq1.update(frq4)
    fr = set()
    for key in frq1:
        if frq1[key] > 1:
            fr.add(key)
    com = uniqSet & fr
    print('в задании эксплицитно не выражено, в каком виде должны выводиться данные, '
          'но здесь они выводятся как множество (в рандомном порядке): \n' + str(com),
            '\n а ещё они записываются в файл в алфавитном порядке, если действовать по условию предыдущего задания')
    text = open('uniqWordsFreq.txt', 'w', encoding='utf-8')
    l = list(com)
    l.sort()
    for elem in l:
        text.write(elem + '\n')
    l = str(text)
    text.close()

def main():
    arr = ['https://rueconomics.ru/210888-uchenye-uznali-kak-pobedit-autizm', 'http://vistanews.ru/science/95645',
           'http://informing.ru/2016/12/02/genetiki-obnaruzhili-klyuch-k-lecheniyu-autizma.html',
           'http://oane.ws/2016/12/02/avstriyskie-genetiki-nashli-sposob-lecheniya-autizma.html']
    set1, frq1 = arr0(arr[0])       #возвращает множество уникальных элементов, возвращает частотный словарь
    set2, frq2 = arr1(arr[1])
    set3, frq3 = arr2(arr[2])
    set4, frq4 = arr3(arr[3])
    commonW(set1, set2, set3, set4)
    uniqList, uniqSet = uniqE(set1, set2, set3, set4)     #записывает файл; возвращает массив, упорядоченный по алфавиту
    commonFreq(uniqSet, frq1, frq2, frq3, frq4)

main()