import base64
import json
import hashlib
import hmac
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


s = requests.Session()

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

# s.get('https://ok12static.oktacdn.com/assets/js/vendor/lib/fingerprint2.min.68ab45bd98459cb766f3ab26d086e5f5.js',
#       headers=headersfor3Js, verify=False, allow_redirects=False)
# s.get('https://ok12static.oktacdn.com/assets/js/jquery-1.12.4.05ced5937a65bd185b03749fdd833c98.js',
#       headers=headersfor3Js, verify=False, allow_redirects=False)
# s.get('https://ok12static.oktacdn.com/assets/js/vendor/lib/crypto-js.eac8c800a39bc533f58390e6c0eef9bf.js',
#       headers=headersfor3Js, verify=False, allow_redirects=False)

jessionid_fromdeviceFingerprint = twelfthResponse.cookies.get('JSESSIONID')

cookies_Nonce = {
    't': 'default',
    'DT': introspect_DT,
    'oktaStateToken': token,
    'JSESSIONID': jessionid_fromdeviceFingerprint,
}

nonceRespond = s.post('https://auth.cityu.edu.hk/api/v1/internal/device/nonce', cookies=cookies_Nonce,
                      headers=headers_Nonce, verify=False)

jsessionid_fromNonce = {'JSESSIONID': nonceRespond.cookies.get('JSESSIONID'), }


version_of_okta_signin_widget = fifthResponse.url.split('okta-signin-widget/')[1].split('/js/ok')[0]
version_of_okta_auth_js = fifthResponse.text.split('okta-auth-js/".concat("')[1].split('"')[0]

nonce = json.loads(nonceRespond.text)['nonce']
devfingerprintHash = 'd8856a0b4564f53281d9e45921b348d3'
devfingerprintHash = devfingerprintHash.encode('utf-8')
fingerprintHmac = hmac.new(nonce.encode('utf-8'), devfingerprintHash, digestmod=hashlib.sha256).hexdigest()
headers13['X-Device-Fingerprint'] = nonce+'|'+ fingerprintHmac + '|d8856a0b4564f53281d9e45921b348d3'

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
    'JSESSIONID': jsessionid_fromNonce,
}


redirect12 = json.loads(ninthResponse.text)['_links']['next']['href']
time.sleep(5)
print(headers13['X-Device-Fingerprint'])
print(nonceRespond.cookies.get('JSESSIONID'))
# thirteenthResponse = s.post('https://auth.cityu.edu.hk/api/v1/authn', cookies=cookies13, headers=headers13, json=json_data13,verify=False,allow_redirects=False)
# print(nonceRespond.cookies.get('JSESSIONID'))
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

# print(thirteenthResponse.url)
# print(thirteenthResponse.text)
# thirteenthResponse_json_elements = json.loads(thirteenthResponse.text)
#
# redirect13 = thirteenthResponse_json_elements['_links']['next']['href']
#
# cookies14 = {
#     't': authn_t_indefault,
#     'DT': authn_DT,
#     'oktaStateToken': thirteenthResponse_json_elements['stateToken'],
#     'JSESSIONID': thirteenthResponse.cookies.get('JSESSIONID'),
# }
#
# params14 = {
#     'stateToken': token,
# }
#
# fourteenthResponse = s.get('https://auth.cityu.edu.hk/login/step-up/redirect', params=params14, cookies=cookies14,
#                            headers=headers14, verify=False)
#
# stepup_SAMLResponse = find_SAMLResponse(fourteenthResponse)
#
# cookies15 = {
#     'JSESSIONID': thirdResponse.cookies.get('JSESSIONID'),
# }
#
# data15 = 'SAMLResponse='+ stepup_SAMLResponse+'&RelayState='+ str(params4['RelayState'])
#
#
# redirect14 = get_SSO_link(fourteenthResponse)
#
# fifteenthResponse = s.post(redirect14, cookies=cookies15, headers=headers15, data=data15, verify=False,allow_redirects=False)
#
# ssb_jsessionid = fifteenthResponse.cookies.get('JSESSIONID')
#
# cookies16 = {
#     'JSESSIONID': ssb_jsessionid,
# }
#
# redirect15 = 'https://banids.cityu.edu.hk'+fifteenthResponse.headers.get('Location')
#
# sixteenthResponse = s.get(redirect15, cookies=cookies16, headers=headers16, verify=False)
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
