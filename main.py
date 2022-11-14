import base64
import json
import hashlib
import hmac
from datetime import datetime
import time
from urllib.parse import parse_qs, unquote_plus, parse_qsl
from urllib.parse import urlparse
import requests
import urllib3
from bs4 import BeautifulSoup
import sys
import data2
from headers import *
from data2 import *
from requests_html import HTMLSession
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

######################################################################
username = ''  # fill your user name here
password = ''  # fill your password here


######################################################################

def get_introspect_portal(response):
    return 'https://auth.cityu.edu.hk' + \
           response.text.split('function(e,t){return t=Te(e,t),Ee(e,e.getIssuerOrigin()+"')[1].split(
               '",t,{withCredentials:!0})}(e,t).')[0]


def finding_js(html_full, num):
    htmlForJs = html_full.text
    soup = BeautifulSoup(htmlForJs, 'lxml')
    jsfile = str(soup.select('script', type='text/javascript')[num].get('src'))
    return jsfile


def finding_js2(html_full, num):
    htmlForJs = html_full.text
    soup = BeautifulSoup(htmlForJs, 'lxml')
    jsfile = (str(soup.select('script', type='text/javascript')[num]).split('mainScript.src = "')[1].split('";')[0])
    return jsfile


def finding_iframe_link(html_full, num):
    htmlForJs = html_full.text
    soup = BeautifulSoup(htmlForJs, 'lxml')
    jsfile = (
        str(soup.select('script', type='text/javascript')[num]).split('"accountChooserDiscoveryUrl":"')[1].split('"};')[
            0])
    return jsfile


def finding_token(html_full, num):
    htmlForJs = html_full.text
    soup = BeautifulSoup(htmlForJs, 'lxml')
    tokenAuth = (
        str(soup.select('script', type='text/javascript')[num]).split('","helpLinks":{"help":')[0].split(
            '"stateToken":"')[
            1])
    tokenAuth = tokenAuth.replace("\\x3D", "")
    tokenAuth = tokenAuth.replace('\\x2D', "-")
    return tokenAuth


def finding_lib_js(html_full, num):
    htmlForJs = html_full.text
    soup = BeautifulSoup(htmlForJs, 'lxml')
    jsfile = 'https://login.okta.com' + (str(soup.select('script', type='text/javascript')[num]['src']))
    return jsfile


def finding_devicefingerprint_link(html_full):
    htmlForJs = html_full.text
    return 'https://auth.cityu.edu.hk' + (htmlForJs.split('src:e.oktaDomainUrl+"')[1].split('"})')[0])


def redirect_link_extraction(respond):
    htmlForRedirect = respond.text
    soup = BeautifulSoup(htmlForRedirect, 'lxml')
    links = str(soup.find_all('meta'))
    if links.find('url') != -1:
        lower = True

    try:
        redirectLink = links.split(";URL=", 1)[1].split('" ')[0]
        return str(redirectLink)
    except:
        error = True

    if error is True:
        redirectLink = (links.split(";url=", 1)[1].split('" ')[0])
        return str(redirectLink)

    return None


def find_SAMLResponse(html_full):
    htmlForJs = html_full.text
    autodypted = htmlForJs.split('name="SAMLResponse" type="hidden" value="')[1].split('"/>')[0]
    autodypted = autodypted.replace('&#x3d;', '%3D')
    autodypted = autodypted.replace('&#x2b;', '%2B')
    return autodypted


def get_SSO_link(html_full):
    htmlForJs = html_full.text
    soup = BeautifulSoup(htmlForJs, 'html.parser')
    return soup.find('div', {"id": "container"}).find('form').get('action')


s = HTMLSession()
count = 1

firstRespond = s.get('https://banweb.cityu.edu.hk/', headers=headers1, verify=False)
redirect1 = redirect_link_extraction(firstRespond)

secondResponse = s.get(redirect1, headers=headers2, verify=False)

redirect2 = redirect_link_extraction(secondResponse)

thirdResponse = s.get(redirect2, headers=headers3,
                      verify=False, allow_redirects=False)

redirect3 = thirdResponse.headers.get('Location').split('?')[0]

thirdUrl = thirdResponse.headers.get('Location')

parsed_url = urlparse(thirdUrl)

params4 = {'SAMLRequest': parsed_url.query.split('SAMLRequest=')[1].split('&RelayState=')[0],
           'RelayState': parsed_url.query.split('RelayState=')[1].split('&SigAlg=')[0],
           'SigAlg': parsed_url.query.split('SigAlg=')[1].split('&Signature=')[0],
           'Signature': parsed_url.query.split('Signature=')[1]}

cookiesfrom3 = {'JSESSIONID': thirdResponse.cookies.get('JSESSIONID'), }

fourthResponse = s.get(redirect3, params=params4, cookies=cookiesfrom3, headers=headers4, verify=False)

cookiesfrom4 = {'JSESSIONID': fourthResponse.cookies.get('JSESSIONID'), }

redirect4 = finding_js(fourthResponse, 0)

fifthResponse = s.get(redirect4, cookies=cookiesfrom4, headers=headers5, verify=False)

redirect5 = finding_js2(fourthResponse, 1)

sixthResponse = s.get(redirect5, cookies=cookiesfrom4, headers=headers6, verify=False)

sixResJS = 'initLoginPage' + (redirect5.split('/initLoginPage')[1])

redirect6 = redirect4.split('/js/ok')[0] + '/labels/json/country_zh_TW.json'

seventhResponse = s.get(redirect6, cookies=cookiesfrom4, headers=headers7, verify=False)

redirect7 = redirect4.split('/js/ok')[0] + '/labels/json/login_zh_TW.json'

eightResponse = s.get(redirect7, cookies=cookiesfrom4, headers=headers8, verify=False)

token = finding_token(fourthResponse, 1)

redirect8 = get_introspect_portal(fifthResponse)

cookies9 = {
    'JSESSIONID': fourthResponse.cookies.get('JSESSIONID'),
    't': fourthResponse.cookies.get('t'),
    'DT': fourthResponse.cookies.get('DT'),
}

referer9 = 'https://auth.cityu.edu.hk/signin/refresh-auth-state/' + token

headers9['Referer'] = referer9

json_data9 = {
    'stateToken': token,
}

ninthResponse = s.post(redirect8, cookies=cookies9, headers=headers9, json=json_data9)

cookiesfrom9 = {'JSESSIONID': ninthResponse.cookies.get('JSESSIONID'), }

# getting finger_Print coolies
introspect_jsessionID = ninthResponse.cookies.get('JSESSIONID')
introspect_okta_stateToken = token
introspect_DT = fourthResponse.cookies.get('DT')
introspect_t = fourthResponse.cookies.get('t')
# end of getting finger_Print


redirect9 = 'https://login.okta.com/discovery/iframe.html'

tenthResponse = s.get(redirect9, cookies=cookiesfrom9, headers=headers10, verify=False)

redirect10 = finding_lib_js(tenthResponse, 0)

headers11['Referer'] = redirect9

eleventhResponse = s.get(redirect10, cookies=cookiesfrom9, headers=headers11, verify=False)

cookies12 = {
    't': 'default',
    'DT': introspect_DT,
    'JSESSIONID': ninthResponse.cookies.get('JSESSIONID'),
    'oktaStateToken': introspect_okta_stateToken,
}

redirect11 = finding_devicefingerprint_link(fifthResponse)

twelfthResponse = s.get(redirect11, cookies=cookies12, headers=headers12, verify=False)

jessionid_fromdeviceFingerprint = twelfthResponse.cookies.get('JSESSIONID')

json_data13 = {
    'password': password,
    'username': username,
    'options': {
        'warnBeforePasswordExpired': True,
        'multiOptionalFactorEnroll': True,
    },
    'stateToken': token,
}
cookies13 = {
    't': 'default',
    'DT': introspect_DT,
    'oktaStateToken': token,
    'JSESSIONID': jessionid_fromdeviceFingerprint,
}

redirect12 = json.loads(ninthResponse.text)['_links']['next']['href']
time.sleep(3)
thirteenthResponse = s.post(redirect12, cookies=cookies13, headers=headers13, json=json_data13, verify=False)

thirteenthResponse_json_elements = json.loads(thirteenthResponse.text)

redirect13 = thirteenthResponse_json_elements['_links']['next']['href']

cookies14 = {
    't': 'default',
    'DT': introspect_DT,
    'oktaStateToken': thirteenthResponse_json_elements['stateToken'],
    'JSESSIONID': thirteenthResponse.cookies.get('JSESSIONID'),
}

params14 = {
    'stateToken': token,
}

fourteenthResponse = s.get('https://auth.cityu.edu.hk/login/step-up/redirect', params=params14, cookies=cookies14,
                           headers=headers14, verify=False)

stepup_SAMLResponse = find_SAMLResponse(fourteenthResponse)

cookies15 = {
    'JSESSIONID': thirdResponse.cookies.get('JSESSIONID'),
}

data15 = 'SAMLResponse=' + stepup_SAMLResponse + '&RelayState=' + str(params4['RelayState'])

redirect14 = get_SSO_link(fourteenthResponse)

while count < 5:
    fifteenthResponse = s.post(redirect14, cookies=cookies15, headers=headers15, data=data15, verify=False,
                               allow_redirects=False)  # SSO

    cookies16 = {
        'JSESSIONID': fifteenthResponse.cookies.get('JSESSIONID'),
    }

    redirect15 = 'https://banids.cityu.edu.hk' + fifteenthResponse.headers.get('Location')
    sixteenthResponse = s.get('https://banids.cityu.edu.hk/ssomanager/c/auth/SSB', cookies=cookies16, headers=headers16,
                              verify=False)  # SSB
    print(sixteenthResponse)
    print(sixteenthResponse.text)
    print(sixteenthResponse.cookies.get('SESSID'))
    if sixteenthResponse.cookies.get('SESSID') == None:
        print('no sessid came from sixteenthRespond')

    # cookies17 = {
    #     'IDMSESSID': username,
    # }
    #
    # headers17 = {
    #     'Host': 'banweb.cityu.edu.hk',
    #     'Cache-Control': 'max-age=0',
    #     'Upgrade-Insecure-Requests': '1',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    #     'Sec-Fetch-Site': 'same-site',
    #     'Sec-Fetch-Mode': 'navigate',
    #     'Sec-Fetch-Dest': 'document',
    #     'Sec-Ch-Ua': '"(Not(A:Brand";v="8", "Chromium";v="101"',
    #     'Sec-Ch-Ua-Mobile': '?0',
    #     'Sec-Ch-Ua-Platform': '"Windows"',
    #     'Referer': 'https://auth.cityu.edu.hk/',
    #     'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    #     'Connection': 'close',
    # }
    #
    # seventeenthResponse = s.get('https://banweb.cityu.edu.hk/pls/PROD/hwsupics_cityu.P_PromptPICS', cookies=cookies17, headers=headers17, verify=False)
    # print(seventeenthResponse)
    # print(seventeenthResponse.cookies.get('SESSID'))
    #
    #
    # print(seventeenthResponse.text)

    # cookies18 = {
    #     'SESSID': seventeenthResponse.cookies.get('SESSID'),
    #     'IDMSESSID': username,
    # }

    #
    # params18 = {
    #     'name': 'bmenu.P_MainMnu',
    # }
    #
    # eighteenthResponse = s.get('https://banweb.cityu.edu.hk/pls/PROD/twbkwbis.P_GenMenu', params=18, cookies=cookies18, headers=headers18, verify=False)
    # print(eighteenthResponse)
    # print(eighteenthResponse.text)

    x = input()
    if x == 'go':
        print('yes')
        cookiesRegMenu = {
            'SESSID': sixteenthResponse.cookies.get('SESSID'),
            'IDMSESSID': username,
        }

        headersRegMenu = {
            'Host': 'banweb.cityu.edu.hk',
            'Sec-Ch-Ua': '"(Not(A:Brand";v="8", "Chromium";v="101"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://banweb.cityu.edu.hk/pls/PROD/twbkwbis.P_GenMenu?name=bmenu.P_MainMnu',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'close',
        }

        paramsRegMenu = {
            'name': 'amenu.P_RegMnu',
        }
        time.sleep(1)
        regMenuResponse = s.get('https://banweb.cityu.edu.hk/pls/PROD/twbkwbis.P_GenMenu', params=paramsRegMenu,
                                cookies=cookiesRegMenu, headers=headersRegMenu, verify=False)
        print('----------------------------------------------------------------------------------------------------')
        print(regMenuResponse)
        print(regMenuResponse.text)

        cookiesRegMainMenu = {
            'SESSID': regMenuResponse.cookies.get('SESSID'),
            'IDMSESSID': username,
        }

        headersRegMainMenu = {
            'Host': 'banweb.cityu.edu.hk',
            'Sec-Ch-Ua': '"(Not(A:Brand";v="8", "Chromium";v="101"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://banweb.cityu.edu.hk/pls/PROD/twbkwbis.P_GenMenu?name=amenu.P_RegMnu',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'close',
        }

        paramsRegMainMenu = {
            'name': 'amenu_cityu.P_CrseRegMnu',
        }
        time.sleep(2)
        regMainMenuResponse = s.get('https://banweb.cityu.edu.hk/pls/PROD/twbkwbis.P_GenMenu', params=paramsRegMainMenu,
                                    cookies=cookiesRegMainMenu, headers=headersRegMainMenu, verify=False)

        print(regMainMenuResponse)
        print(regMainMenuResponse.text)

        cookiesShowAddDropinRegMainMenu = {
            'SESSID': regMainMenuResponse.cookies.get('SESSID'),
            'IDMSESSID': username,
        }

        headersShowAddDropinRegMainMenu = {
            'Host': 'banweb.cityu.edu.hk',
            'Sec-Ch-Ua': '"(Not(A:Brand";v="8", "Chromium";v="101"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://banweb.cityu.edu.hk/pls/PROD/twbkwbis.P_GenMenu?name=amenu_cityu.P_CrseRegMnu',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'close',
        }
        time.sleep(1)
        showAddDropResponse = s.get('https://banweb.cityu.edu.hk/pls/PROD/bwskfreg.P_AltPin',
                                    cookies=cookiesShowAddDropinRegMainMenu,
                                    headers=headersShowAddDropinRegMainMenu, verify=False)

        print(showAddDropResponse)
        print(showAddDropResponse.text)

        cookiesFinalAddDropPage = {
            'SESSID': showAddDropResponse.cookies.get('SESSID'),
            'WDB_GATEWAY_LOGOUT': 'YES',
            'IDMSESSID': username,
        }

        headersFinalAddDropPage = {
            'Host': 'banweb.cityu.edu.hk',
            'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': '"(Not(A:Brand";v="8", "Chromium";v="101"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'https://banweb.cityu.edu.hk',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://banweb.cityu.edu.hk/pls/PROD/bwskfreg.P_AltPin',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'close',
        }

        dataFinalAddDropPage = 'term_in=202206'
        time.sleep(1)
        finalAddDropPageResponse = s.post('https://banweb.cityu.edu.hk/pls/PROD/bwskfreg.P_AltPin',
                                          cookies=cookiesFinalAddDropPage,
                                          headers=headersFinalAddDropPage, data=dataFinalAddDropPage, verify=False)

        print(finalAddDropPageResponse)
        print(finalAddDropPageResponse.text)

        cookiesForRefreshAddDrop = {
            'SESSID': finalAddDropPageResponse.cookies.get('SESSID'),
            'WDB_GATEWAY_LOGOUT': 'YES',
            'IDMSESSID': username,
        }

        headersForRefreshAddDrop = {
            'Host': 'banweb.cityu.edu.hk',
            'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': '"(Not(A:Brand";v="8", "Chromium";v="101"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://banweb.cityu.edu.hk/pls/PROD/twbkwbis.P_GenMenu?name=amenu_cityu.P_CrseRegMnu',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'close',
        }
        time.sleep(1)
        refreshAddDropresponse = s.get('https://banweb.cityu.edu.hk/pls/PROD/bwskfreg.P_AltPin',
                                       cookies=cookiesForRefreshAddDrop,
                                       headers=headersForRefreshAddDrop, verify=False)
        print(refreshAddDropresponse)
        print(refreshAddDropresponse.text)

        cookiesForClyde = {
            'TESTID': 'set',
            'SESSID': refreshAddDropresponse.cookies.get('SESSID'),
            'IDMSESSID': username,
        }

        refreshTime = 15  # 15 second refresh

        currentTime = False
        while currentTime == False:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Current Time =", current_time)
            if current_time == '08:45:00':
                print('Found')
                break
        time.sleep(1)
        clydeAdd = 1
        while clydeAdd < 3:
            headersForClyde = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://banweb.cityu.edu.hk/pls/PROD/bwckcoms.P_Regs',
                'Origin': 'https://banweb.cityu.edu.hk',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
            }

            dataForClyde = [
                ('term_in', '202206'),
                ('RSTS_IN', 'DUMMY'),
                ('assoc_term_in', 'DUMMY'),
                ('CRN_IN', 'DUMMY'),
                ('start_date_in', 'DUMMY'),
                ('end_date_in', 'DUMMY'),
                ('SUBJ', 'DUMMY'),
                ('CRSE', 'DUMMY'),
                ('SEC', 'DUMMY'),
                ('LEVL', 'DUMMY'),
                ('CRED', 'DUMMY'),
                ('GMOD', 'DUMMY'),
                ('TITLE', 'DUMMY'),
                ('MESG', 'DUMMY'),
                ('REG_BTN', 'DUMMY'),
                ('MESG', 'DUMMY'),
                ('RSTS_IN', ''),
                ('assoc_term_in', '202206'),
                ('CRN_IN', '10393'),
                ('start_date_in', '06/06/2022'),
                ('end_date_in', '07/23/2022'),
                ('SUBJ', 'EE'),
                ('CRSE', '4222'),
                ('SEC', 'C01'),
                ('LEVL', 'Bachelor\'s Degree'),
                ('CRED', '    3.000'),
                ('GMOD', 'Letter grade'),
                ('TITLE', 'Digital Forensics'),
                ('RSTS_IN', 'RW'),
                ('CRN_IN', '10241'),
                ('assoc_term_in', ''),
                ('start_date_in', ''),
                ('end_date_in', ''),
                ('RSTS_IN', 'RW'),
                ('CRN_IN', ''),
                ('assoc_term_in', ''),
                ('start_date_in', ''),
                ('end_date_in', ''),
                ('RSTS_IN', 'RW'),
                ('CRN_IN', ''),
                ('assoc_term_in', ''),
                ('start_date_in', ''),
                ('end_date_in', ''),
                ('RSTS_IN', 'RW'),
                ('CRN_IN', ''),
                ('assoc_term_in', ''),
                ('start_date_in', ''),
                ('end_date_in', ''),
                ('RSTS_IN', 'RW'),
                ('CRN_IN', ''),
                ('assoc_term_in', ''),
                ('start_date_in', ''),
                ('end_date_in', ''),
                ('RSTS_IN', 'RW'),
                ('CRN_IN', ''),
                ('assoc_term_in', ''),
                ('start_date_in', ''),
                ('end_date_in', ''),
                ('RSTS_IN', 'RW'),
                ('CRN_IN', ''),
                ('assoc_term_in', ''),
                ('start_date_in', ''),
                ('end_date_in', ''),
                ('RSTS_IN', 'RW'),
                ('CRN_IN', ''),
                ('assoc_term_in', ''),
                ('start_date_in', ''),
                ('end_date_in', ''),
                ('RSTS_IN', 'RW'),
                ('CRN_IN', ''),
                ('assoc_term_in', ''),
                ('start_date_in', ''),
                ('end_date_in', ''),
                ('RSTS_IN', 'RW'),
                ('CRN_IN', ''),
                ('assoc_term_in', ''),
                ('start_date_in', ''),
                ('end_date_in', ''),
                ('regs_row', '1'),
                ('wait_row', '0'),
                ('add_row', '10'),
                ('REG_BTN', 'Submit Changes'),
            ]

            ClydeResponse = s.post('https://banweb.cityu.edu.hk/pls/PROD/bwckcoms.P_Regs', cookies=cookiesForClyde,
                                   headers=headersForClyde, data=dataForClyde)
            print(ClydeResponse)
            print(ClydeResponse.text)
            print('the cookie of clyde:')
            print(ClydeResponse.cookies.get('SESSID'))
            clydeAdd = clydeAdd + 1
            if ClydeResponse.cookies.get('SESSID') == None:
                print('no sessid came from sixteenthRespond')
            else:
                cookiesForClyde['SESSID'] = ClydeResponse.cookies.get('SESSID')

        count = 10
        break
    else:
        time.sleep(5)
        if 'break in' or 'System Error' in sixteenthResponse.text:  ## most likely to get in at 3 third time
            count = count + 1
        else:
            sessid = sixteenthResponse.cookies.get('SESSID')
            count = 10

# 最後 respond 翻黎的 SESSID = 下次 first request 的 SESSID
# GA 資料會接近上一次request


# i=0
# print(firstRespond.url)
# print(firstRespond.cookies.get('JSESSIONID'))
# i+=1
# print(secondResponse.url)
# print(secondResponse.cookies.get('JSESSIONID'))
# i+=1
# print(thirdResponse.url)
# print(thirdResponse.cookies.get('JSESSIONID'))
# i+=1
# print(fourthResponse.url)
# print(fourthResponse.cookies.get('JSESSIONID'))
# i+=1
# print(fifthResponse.url)
# print(fifthResponse.cookies.get('JSESSIONID'))
# i+=1
# print(sixthResponse.url)
# print(sixthResponse.cookies.get('JSESSIONID'))
# i+=1
# print(seventhResponse.url)
# print(seventhResponse.cookies.get('JSESSIONID'))
# i+=1
# print(eightResponse.url)
# print(eightResponse.cookies.get('JSESSIONID'))
# i+=1
# print(ninthResponse.url)
# print(ninthResponse.cookies.get('JSESSIONID'))
# i+=1
# print(tenthResponse.url)
# print(tenthResponse.cookies.get('JSESSIONID'))
# i+=1
# print(eleventhResponse.url)
# print(eleventhResponse.cookies.get('JSESSIONID'))
# i+=1
# print(twelfthResponse.url)
# print(twelfthResponse.cookies.get('JSESSIONID'))
# i+=1
# print(thirteenthResponse.url)
# print(thirteenthResponse.cookies.get('JSESSIONID'))
# i+=1
# print(fourteenthResponse.url)
# print(fourteenthResponse.cookies.get('JSESSIONID'))
# i+=1
# print(fifteenthResponse.url)
# print(fifteenthResponse.cookies.get('JSESSIONID'))
# i+=1
# print(sixteenthResponse.url)
# print(sixteenthResponse.cookies.get('JSESSIONID'))
#


# open('data1.py', 'w').close()
# open('data1.py', 'a').write("data = ['']")
# open('data2.py', 'w').close()
# open('data2.py', 'a').write("data = ['']")

# find "accountChooserDiscoveryUrl" in fourthResponse for getting "https://login.okta.com/discovery/iframe.html"
# print(firstRespond)
# print(secondResponse)
# print(thirdResponse)
# print(fourthResponse)
# print(fifthResponse)
# print(sixthResponse)
# print(seventhResponse)
# print(eightResponse)
# print(ninthResponse)
# print(tenthResponse)
# print(eleventhResponse)
# print(twelfthResponse)
# print(thirteenthResponse)
# print(fourteenthResponse)
# print(fifteenthResponse)
