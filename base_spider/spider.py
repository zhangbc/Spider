import requests
from requests import Session,Request,exceptions
import logging,sys,math
from requests.exceptions import ReadTimeout
import urllib.request
import Throttle
from spidercache import cache
from  diskcache import DiskCache
import log
class base_spider:

    def __init__(self,delay=10,retry=0,header=None,cache=DiskCache(),proxies=None):
        self.retry=retry
        self.throttle = Throttle.Throttle(delay)
        self.cache=cache
        self.proxies=proxies
        self.header=header
        log.mylogging().info('start crawl')

    @cache(0)
    def get_content(self,url,timeout=5,maxretry=5):

        s = Session()
        req = Request('GET', url,headers=self.header)
        prepped = req.prepare()
        try:
            resp = s.send(prepped,proxies=self.proxies,timeout=timeout)
            return {'html':resp.content.decode('utf-8'),'code':resp.status_code}
        except exceptions.Timeout as e:
            self.retry += 1
            log.mylogging().error(str(e)+"try to retry {}".format(self.retry))
            if self.retry>=maxretry:
                log.mylogging().error("retry =5 return None".format(self.retry))
                self.retry=0
                resp=None
                return resp
            else:
                self.get_content(url,self.header,timeout,self.proxies,maxretry)

        except exceptions.HTTPError as e:
            self.retry += 1
            log.mylogging().error(str(e) + "try to retry {}".format(self.retry))
            if self.retry >= maxretry:
                log.mylogging().error("retry =5 return None".format(self.retry))
                self.retry = 0
                resp = None
                return resp
            else:
                self.get_content(url, self.header, timeout, self.proxies, maxretry)

        except exceptions.ConnectionError as e:
            self.retry += 1
            log.mylogging(). error(str(e) + "try to retry {}".format(self.retry))
            if self.retry >= maxretry:
                log.mylogging().error("retry =5 return None".format(self.retry))
                self.retry = 0
                resp = None
                return resp
            else:
                self.get_content(url, self.header, timeout, self.proxies, maxretry)

    def report(self,count, blockSize, totalSize):
            percent = int(count * blockSize * 100 / totalSize)
            sys.stdout.write("\r%d%%" % percent + ' complete')
            sys.stdout.write('[%-50s] %s' % ('=' * int(math.floor(count * blockSize * 50 / totalSize)), percent))
            sys.stdout.flush()

    def down_load_imge_video(self,url,path):
        log.mylogging().info("start to download")
        urllib.request.urlretrieve(url,path,reporthook=self.report)
        log.mylogging().info("download ok!")

