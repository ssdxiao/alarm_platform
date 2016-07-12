import httplib

URL="https://test.isurpass.com.cn/iremote"
user="thirdparter_tecus"
password="2c9c8047fbef41b3b496b8553eb1e1fa897314"


class HttpClient:
    def __init__(self, url, port=80, timeout=10):
        self.client = httplib.HTTPConnection(url, port, timeout)

    def get(self, url):
        self.client.request("GET", url)
        data = {}
        rep = self.client.getresponse()
        data["status"] = rep.status
        data["reason"] = rep.reason
        data["data"] = rep.read()
        return data


if __name__ == "__main__":
    client = HttpClient(URL)
    print client.get("/")
