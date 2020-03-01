#-*-coding:utf-8-*-
#coding:utf-8

from cefpython3 import cefpython
import platform
import sys,json
from threading import Thread
import time
from flask_cors import *
from flask import Flask



class runcef():
    def __init__(self):
        pass

    def dojs(self):
        # 设置初始cookie，初始的cookie必须对应‘SESSION=caec8ba1-2aa7-47a1-86f6-af72c67d736a;’
        self.br.GetMainFrame().ExecuteJavascript('document.cookie="HM4hUBT0dDOn80S=TwreMojvHWI4WoJB4VgVv_salJWmc.kx3bJsjCQdBqK7PRMVpFaFGCPj_7diKwxq;"')
        self.br.GetMainFrame().ExecuteJavascript('document.cookie="SESSION=caec8ba1-2aa7-47a1-86f6-af72c67d736a;"')
        self.br.GetMainFrame().ExecuteJavascript('document.cookie="HM4hUBT0dDOnenable=true;"')
        self.br.GetMainFrame().ExecuteJavascript('document.cookie="HM4hUBT0dDOn80T=42K9BAw6n8TGSkuEMI4UBSWshjAxFt.j84271vTPgttvlgEl9t_Lb_uOzzFFH5pBK9Zph2paZy1mrlg1Bi8kPgAOICH7lMVlmWhpy41idlRb8VNwV3x2GZYR46wsvOHKtvvuIfTUnYrP9gl1EQ1nDuS8_toEFs6zuWRIv8ZiNaLlABv7d4vzkaFURL5M5vlH7X_oJRfxnmFU_NVcq4iy4sbtvHUmIAbZPRjkJmSJvUhz2W0bOyp7xleYJCyFB7suNk4TBP_uTmzml7ty3f0DN2P9KNdPrRmQr6YeJH.x3IR41kmC.iV680yznfen0xCW.WGDNs4yBzctUXn7qY_Thjq1SJGK829WcTNipOYFTQQ0fN55E9md3GwU.dUSKVXc54Dq"')
        # 获取url参数，cookie
        self.br.GetMainFrame().ExecuteJavascript('get_url(wss._$yV("/website/parse/rest.q4w"))')
        self.br.GetMainFrame().ExecuteJavascript('get_cookie(wss._$ms(746,2))')
    #

    def main(self):
        self.check_versions()
        sys.excepthook = cefpython.ExceptHook  # To shutdown all CEF processes on error
        # commandLineSwitches={'proxy-server': '192.168.1.117:8888'}
        cefpython.Initialize()
        self.br = cefpython.CreateBrowserSync()
        self.br.LoadUrl("http://wenshu.court.gov.cn/website/wenshu/181217BMTKHNT2W0/index.html")
        # self.br.SetClientHandler(ClientHandler())
        # self.br.ShowDevTools()

        js = cefpython.JavascriptBindings()
        js.SetFunction("get_url", self.get_url)
        js.SetFunction("get_cookie", self.get_cookie)

        self.br.SetJavascriptBindings(js)

        cefpython.MessageLoop()
        cefpython.Shutdown()

    # 获取加密链接
    def get_url(self,js_callback=None):
        print('url',js_callback)
        self.url = js_callback

    # 获取加密cookie
    def get_cookie(self,js_callback=None):
        print('cookie', js_callback)
        self.cookie = js_callback

    def check_versions(self):
        ver = cefpython.GetVersion()
        assert cefpython.__version__ >= "57.0", "CEF Python v57.0+ required to run this"


def runflask():
    global cef
    app = Flask(__name__)
    CORS(app, resources={r"/getparam/": {"origins": "*"}})
    @app.route("/getparam")
    def test():
        cef.dojs()
        data = {
            "cookie": cef.cookie,
            "url": cef.url
        }
        return json.dumps(data)
    app.run(host='0.0.0.0')


if __name__ == '__main__':
    thr = Thread(target=runflask)
    thr.start()
    cef = runcef()
    cef.main()






