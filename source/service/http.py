#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib, urllib2

class Page():
    _URL = None
    _RequestHeaders = None
    _RequestCookies = None
    _RequestData = None
    _ResponseCode = None
    _ResponseHeaders = None
    _ResponseCookies = None
    _ResponseData = None
    
    def __init__(self, URL):
        self._URL = URL
    
    def Refresh(self):
        RequestHeaders = {}
        RequestCookies = ""
        RequestData = {}
        
        self._ClearResponse()
        
        if self._RequestHeaders <> None:
            for header in self._RequestHeaders:
                RequestHeaders.update({header.get_Name():header.get_Value()})
        
        if self._RequestCookies <> None:
            for cookie in self._RequestCookies:
                RequestCookies = RequestCookies + cookie.get_Name() + "=" + cookie.get_Value() + ";"
            RequestHeaders.update({"Cookie":RequestCookies})
            
        if self._RequestData <> None:
            for data in self._RequestData:
                RequestData.update({data.get_Name():data.get_Value()})
            RequestData = urllib.urlencode(RequestData)
        else:
            RequestData = None
            
        try:
            myRequest = urllib2.Request(self._URL, RequestData, RequestHeaders)
            myResponse = urllib2.urlopen(myRequest)
        except urllib2.URLError as e:
            raise HTTPError(e)
        
        self._ResponseCode = myResponse.getcode()
        self._ResponseData = myResponse.read()
        
        self._ResponseHeaders = []
        for header in myResponse.info():
            self._ResponseHeaders.append(Header(header,myResponse.info().getheader(header)))
            if header == "set-cookie":
                self._ResponseCookies = []

                for cookie in myResponse.info().getheader(header).split(';'):
                    try:
                        self._ResponseCookies.append(Cookie(cookie.split('=')[0].strip(), cookie[len(cookie.split('=')[0])+1:].strip()))
                    except:
                        pass
    
    def get_URL(self):
        return self._URL
    
    def set_RequestHeaders(self, *args):
        self._RequestHeaders = args
        self._ClearResponse()
    
    def get_RequestHeaders(self):
        return self._RequestHeaders
    
    def set_RequestCookies(self, *args):
        self._RequestCookies = args
        self._ClearResponse()
    
    def get_RequestCookies(self):
        return self._RequestCookies
    
    def set_RequestData(self, *args):
        self._RequestData = args
        self._ClearResponse()
    
    def get_RequestData(self):
        return self._RequestData

    def get_ResponseCode(self):
        return self._ResponseCode
    
    def get_ResponseData(self):
        return self._ResponseData
    
    def get_ResponseHeaders(self):
        return self._ResponseHeaders
    
    def get_ResponseCookies(self):
        return self._ResponseCookies
    
    def _ClearResponse(self):
        _ResponseCode = None
        _ResponseHeaders = None
        _ResponseCookies = None
        _ResponseData = None

class HTTP_Property:
    name = ""
    value = ""
    
    def __init__(self, name="", value=""):
        self.name = name
        self.value = value
    
    def set_Name(self,value):
        self.name = value
    
    def get_Name(self):
        return self.name
    
    def set_Value(self,value):
        self.value = value
    
    def get_Value(self):
        return self.value
    
class Cookie(HTTP_Property):
    pass

class Header(HTTP_Property):
    pass

class Data(HTTP_Property):
    pass

class HTTPError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)