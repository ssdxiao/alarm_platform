
import urllib2
import urllib
from utils.log import log
import json
from utils.config import MAIN_USER
from utils.config import MAIN_PASSWD

class HttpClient:
    def __init__(self, url, timeout=10):
        self.url = url
        self.token = ""

    def post(self, url, values):

        try:
            url = self.url + url
            data = urllib.urlencode(values)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            data= response.read()
            log.debug(data)
            data = json.loads(data)
            return data
        except:
            print "post request error"
            return None


    def get_token(self):
        values = {'code': MAIN_USER, 'password': MAIN_PASSWD}
        data = self.post("/thirdpart/login", values)
        if data :
            if data["resultCode"] == 0:
                self.token = data["token"]
                return self.token
            else:
                log.error("get token error")

        return None

    def get_alarm(self,id):
        values = {'lastid': id, 'token': self.token}
        data = self.post("/thirdpart/event/queryevent", values)
        if data:
            if data["resultCode"] == 0:
                if data.has_key("events"):
                    return data["events"]
                else:
                    return []
            else:
                log.error( "get event error")

        return None

    def releasealarm(self, zwaveid, user):
        values = {'zwavedeviceid': zwaveid, 'token': self.token, "employeename" : user}
        print values
        data = self.post("/thirdpart/zufang/unalarmdevicewarning", values)
        if data:
            if data["resultCode"] == 0:
                log.debug("release alarm ok")
            else:
                log.debug("release alarm error")


class HttpsClient:
    def __init__(self, url, timeout=10):
        self.url = url
        self.token = ""

    def get(self, url):

        try:
            url = self.url + url
            print url
            urllib2.urlopen(url)
        except:
            print "get request error"

    def sync_alarm(self, user):
        if user:
            self.get("/fresh_alarm?id=%s"%id)        


 
