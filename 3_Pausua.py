import getpass
import urllib.parse

import requests
from bs4 import BeautifulSoup
import urllib3

user = ''
password = ''
cookie = ''
loginToken = ''
uriEskaera = ''


def datuak_eskatu():
    global user #Aldagai globalak bihurtzeko eta bere balioa globalki aldatzeko
    global password
    user = input("Sartu eGelako erabiltzailea, mesedez: ")

    try:
        password = getpass.getpass(prompt='Pasahitza: ', stream=None)
    except Exception as error:
        print('ERROR', error)
    else:
        print('Password entered:', password)


def eskaera_1():
    global cookie
    global loginToken
    global uriEskaera
# GET /login/index.php HTTP / 1.1
# Host: egela.ehu.eus
    metodoa = 'GET'
    uria = "https://egela.ehu.eus/login/index.php"
    goiburuak = {'Host': 'egela.ehu.eus'}

    erantzuna = requests.get(uria, headers=goiburuak, allow_redirects=False)
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print("1.Eskaeraren metodoa eta URIa :", metodoa, uria)
    print("1.Eskaera: " + str(kodea) + " " + deskribapena)
    #Cookia lortu
    cookie = erantzuna.headers['Set-Cookie'].split(';')[0]
    print("1.Eskaeraren Cookia: ", cookie)

    #Location URL-a dagoen begiratu

    if ('Location' in erantzuna.headers) is False:
        uriEskaera = uria

    print("URI ESKAERA ", uriEskaera)
    #LoginToken lortu nahi
    html = erantzuna.content

    #HTML parseatuko dugu

    soup = BeautifulSoup(html, 'html.parser')
    token = soup.find('input', {'name': 'logintoken'})

    if token.has_attr('value'):
        loginToken = token['value']
        print("Login Token: ", loginToken)

def eskaera_2():
    global uriEskaera
    global cookie
    print(uriEskaera)
    metodoa = "POST"
    # POST / login / index.php
    # HTTP / 1.1
    # Host: egela.ehu.eus
    # Cookie: MoodleSessionegela = 8lbkbfufvtbr9agthn02peal4hn2dnd0
    # Content - Type: application / x - www - form - urlencoded
    # Content - Length: 78
    #
    # logintoken = QCcDskOLf5BMyHTPpb1vuatiUvy21xMF & username = 909854 & password = Euiti2020
    goiburuak = {'Host': 'egela.ehu.eus',
                 'Cookie': cookie,
                 'Content-Type': 'application/x-www-form-urlencoded'}
    edukia = {'logintoken': loginToken,
              'username': user,
              'password': password}
    edukia_encoded = urllib.parse.urlencode(edukia)
    goiburuak['Content-Length'] = str(len(edukia_encoded))
    erantzuna = requests.post(uriEskaera, headers=goiburuak, data=edukia, allow_redirects=False)

    print("2.Eskaeraren metodoa eta URIa :", metodoa, uriEskaera)
    print("2.Eskaeraren edukia", edukia)
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print("2.Eskaera: " + str(kodea) + " " + deskribapena)
    # Cookia berria lortu
    cookie = erantzuna.headers['Set-Cookie'].split(';')[0]
    print("2.Eskaeran Cookia: ", cookie)
    if ('Location' in erantzuna.headers) is True:
        uriEskaera = erantzuna.headers['Location']

    print("2.Eskaeran LOCATION: ", uriEskaera)


def eskaera_3():
    global uriEskaera
    print(uriEskaera)
    metodoa = "GET"
    # GET / login / index.php?testsession = 55890
    # HTTP / 1.1
    # Host: egela.ehu.eus
    # Cookie: MoodleSessionegela = 0mflt9n2juknpcrkrd977tut1l8k41ct
    goiburuak = {'Host': uriEskaera.split('/')[2],
                 'Cookie': cookie}
    erantzuna = requests.get(uriEskaera, headers=goiburuak, allow_redirects=False)
    print("3.Eskaeraren metodoa eta URIa :", metodoa, uriEskaera)
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print("3.Eskaera: " + str(kodea) + " " + deskribapena)
    if ('Location' in erantzuna.headers) is True:
        uriEskaera = erantzuna.headers['Location']
    print("3.Eskaeran Cookia: ", cookie)
    print("3.Eskaeran LOCATION: ", uriEskaera)
def eskaera_4():
    global uriEskaera
    print(uriEskaera)
    metodoa = "GET"
    # GET / HTTP / 1.1
    # Host: egela.ehu.eus
    # Cookie: MoodleSessionegela = 0mflt9n2juknpcrkrd977tut1l8k41ct
    goiburuak = {'Host': uriEskaera.split('/')[2],
                 'Cookie': cookie}

    erantzuna = requests.get(uriEskaera, headers=goiburuak, allow_redirects=False)
    print("3.Eskaeraren metodoa eta URIa :", metodoa, uriEskaera)
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print("4.Eskaera " + str(kodea) + " " + deskribapena)
    print("4.Eskaeran Cookia: ", cookie)
    html = erantzuna.content

    # HTML parseatuko dugu

    soup = BeautifulSoup(html, 'html.parser')
    izena = soup.find('span', {'class': 'usertext mr-1'})
    errenkadak = soup.find_all('div', {'class': 'info'})
    for idx, errenkada in enumerate(errenkadak):
        irakasgaiak = errenkada.h3.a.text
        if (irakasgaiak == 'Web Sistemak'):
            uriEskaera = errenkada.a['href']
            print("Irakasgaia: ", irakasgaiak)
            print("Eskaera: ", uriEskaera)

def eskaera_5():

    # Web Sistema ikasgaiko eskaera egindo da metodo honetan.
    # GET / course / view.php?id = 57996
    # HTTP / 1.1
    # Host: egela.ehu.eus
    # Cookie: MoodleSessionegela = u47586166f8ag046jf14eau8vbhjr1a2
    metodoa = 'GET'
    goiburuak = {'Host': uriEskaera.split('/')[2],
                 'Cookie': cookie}

    erantzuna = requests.get(uriEskaera, headers=goiburuak, allow_redirects=False)
    print("5.Eskaeraren metodoa eta URIa :", metodoa, uriEskaera)
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print("5.Eskaera " + str(kodea) + " " + deskribapena)
    print("5.Eskaeran Cookia: ", cookie)
    html = erantzuna.content
    soup = BeautifulSoup(html, 'html.parser')
    #print(html)
if __name__ == '__main__':
    datuak_eskatu()
    eskaera_1()
    eskaera_2()
    eskaera_3()
    eskaera_4()
    eskaera_5()
