# First setup torrc

# Generate the hash
# tor --hash-password "yeah right, this is my passwd"

# Add the following lines to /etc/tor/torrc
# ControlPort 9051
# HashedControlPassword 16:04EC77612CC5BFF9606CA94B83473CF6BEF4373CC2D943FE1356C30FB6
# CookieAuthentication 1


import sys
import time
import requests

from stem import Signal
from stem.control import Controller

def newid():
  with Controller.from_port(port = 9051) as controller:
    controller.authenticate('yeah right, this is my passwd')
    controller.signal(Signal.NEWNYM)


PROXYHOST = 'localhost'
PROXYPORT = 9050
HOST = 'ifconfig.me'

while True:
  s = time.perf_counter()
  url = 'https://' + HOST
  print(f'[*] Requesting {url}')
  print(requests.get(url, proxies={'http': 'socks5h://%s:%s' % (PROXYHOST, PROXYPORT), 'https': 'socks5h://%s:%s' % (PROXYHOST, PROXYPORT)}).text)
  print('[*] Done')
  e = time.perf_counter()
  t = e - s
  if t < 10:
    print(f'sleeping {10-t}s')
    time.sleep(10-t)

  # torrc signals are limited to 1 each 10 seconds (I think)
  newid()
