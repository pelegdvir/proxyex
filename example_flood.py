from http.client import HTTPConnection
from time import sleep

from classification.classifier import Classifier
from content.suites.mock_suite import MockSuite

PROXY_IP = '127.0.0.1'
PROXY_PORT = 8001

classifier = Classifier(suite=MockSuite())


def run():
    for i in range(30):
        sleep(0.01)
        conn = HTTPConnection(f"{PROXY_IP}:{PROXY_PORT}", timeout=1)
        conn.request("GET", '/try')
        res = conn.getresponse()
        conn.close()
        print(res.status)


run()
