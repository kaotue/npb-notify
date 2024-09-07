import os
import time
import urllib.request

INTERVAL_SECONDS = float(os.getenv('INTERVAL_SECONDS', 1.5))


class BaseSelector:
    def __init__(self, url):
        self.url = url

    def download(self):
        req = urllib.request.Request(self.url)
        with urllib.request.urlopen(req) as res:
            html = res.read()
            time.sleep(INTERVAL_SECONDS)
            return html
