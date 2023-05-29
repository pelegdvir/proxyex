from http.client import HTTPConnection

from classification.classifier import Classifier
from content.suites.mock_suite import MockSuite

PROXY_IP = '127.0.0.1'
PROXY_PORT = 8001

classifier = Classifier(suite=MockSuite())


def run():
    conn = HTTPConnection(f"{PROXY_IP}:{PROXY_PORT}", timeout=1)
    conn.request("POST", '/try', body=b'great')
    res = conn.getresponse()
    conn.close()
    print(res.status)

    conn = HTTPConnection(f"{PROXY_IP}:{PROXY_PORT}", timeout=1)
    conn.request("POST", '/try', body=b'worse')
    res = conn.getresponse()
    conn.close()
    print(res.status)


run()
