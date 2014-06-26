#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
from kivy.utils import platform
if platform == 'android':
    from jnius import autoclass, PythonJavaClass, java_method, cast
    from android import activity
    from android.runnable import run_on_ui_thread

class AndroidWrapper:
    #Singleton
    __metaclass__ = Singleton
    
    def Toast(self, msg, length_long=False):
        if platform != 'android': return False
        
        self._Toast(msg, length_long)
        
    @run_on_ui_thread
    def _Toast(self, msg, length_long=False):
        Toast = autoclass('android.widget.Toast')
        context = autoclass('org.renpy.android.PythonActivity').mActivity   
        
        duration = Toast.LENGTH_LONG if length_long else Toast.LENGTH_SHORT
        String = autoclass('java.lang.String')
        c = cast('java.lang.CharSequence', String(msg))
        t = Toast.makeText(context, c, duration)
        t.show()