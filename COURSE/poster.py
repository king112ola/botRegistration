import sys
import requests
import json
from bs4 import BeautifulSoup


def mprint(x):
    sys.stdout.write(x)

    return


headers = {'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'}

mprint('[-] Initialization...')
s = requests.session()
s.headers.update(headers)
print("done")


mprint('[-] Gathering JSESSIONID..')

# This  should redirect us to the login page 
# On looking at the page source we can find that 
# in the submit form 6 values are submitted (at least at the time of this script)
# try to take those values out using beautiful soup 
# and then do a post request. On doing post https://login.oracle.com/mysso/signon.jsp 
# we will be given message we have the data which is more than necessary
# then it will take us to the form where we have to submit data here 
# https://login.oracle.com/oam/server/sso/auth_cred_submit
# once done we are signed in and doing and requests.get(url) will get you the page you want.

r = s.get("company's local url- a link which requires authentication")
if r.status_code != requests.codes.ok:
    exit(1)
print("done")

c = r.content
soup = BeautifulSoup(c,'lxml')
svars = {}

for var in soup.findAll('input',type="hidden"):
    svars[var['name']] = var['value']


s = requests.session()
r = s.post('https://login.oracle.com/mysso/signon.jsp', data=svars)

mprint('[-] Trying to submit credentials...')

data = {
        'v': svars['v'],
        'OAM_REQ': svars['OAM_REQ'],
        'site2pstoretoken': svars['site2pstoretoken'],
        'locale': svars['locale'],
        'ssousername': "kingyli25",
        'password': "Zyxzz083xqau",
}

r = s.post('https://login.oracle.com/oam/server/sso/auth_cred_submit', data=data)

r = s.get("company's local url- a link which requires authentication")
# dumping the html page to html file
with open('test.html','w') as f:
    f.write(r.content)