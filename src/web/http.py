import urllib, urllib2

class HTTP:
    def GetPageResponse(self, page, data={}, headers={}):
        Request_Page = page#urllib.urlencode(page)
        Request_Headers = headers
        Request_Data = urllib.urlencode(data)
        
        Request = urllib2.Request(Request_Page, Request_Data, Request_Headers)
        try:
            Response = urllib2.urlopen(Request)
        except urllib2.URLError, e:
            raise HTTPError(e)
        except:
            print "Warning: Unexpected error at web.http.HTTP().GetPageResponse()"
            raise HTTPError("Warning: Unexpected error at web.http.HTTP().GetPageResponse()")
        else:
            return HTTPResponse(Response)

class HTTPResponse:
    Response = None
    _Data = None
    _Headers = None
    
    def __init__(self, Response):
        self._Headers = Response.info()
        self._Data = Response.read()
        self._Code = Response.getcode()
        self._URL = Response.geturl()
    
    #Response URL (check if page was redirected)
    def URL(self):
        return self._URL
    
    #HTTP Response Code
    def Code(self):
        return self._Code
    
    def Cookies(self):
        return self._Headers.getheader('Set-Cookie')
    
    def Data(self):
        return self._Data
    
    def Header(self, header):
        try: 
            Out = self._Headers.getheader(header)
        except:
            Out = None
        finally:
            return Out

class HTTPError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)
