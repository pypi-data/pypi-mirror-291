import glob
import json
import subprocess
import os
import platform
from threading import Thread
import time
import requests
class Proxy():
    """
    代理类
    """
    system_list={"Windows":"win", "Linux":"linux", "Darwin":"mac"}
    def __init__(self, port:int=0,porxy_port:int=0):
        self.port =port 
        self.port_proxy = porxy_port
        self.baseurl=f"http://127.0.0.1:{self.port}"
        self.process=None
        self._th=Thread(target=self._init_proxy,daemon=True)
        self.start()
        # self._init_proxy()
    def setdynamicProxy(self,proxyurl:str) ->dict:
        """
        设置动态代理ip\n
        :param proxyurl 代理url\n
        :return dict 返回结果\n
        ps:切换ip直接重新调用本方法,proxyurl传新的代理url即可\n
        """
        if not proxyurl:
            raise RuntimeError("代理url不能为空")
        
        data=self._sendrequest("start",url=proxyurl)
        # print("打印响应结果：",data)
        return data
        
    def setdirectProxy(self)->dict:
        """
        设置直连代理\n
        :return dict 返回结果
        """
        data=self._sendrequest("start",url="")
        # print("打印响应结果：",data)
        return data
    def stopProxy(self,url:str) ->dict:
        """
        停止代理\n
        :param url 代理url\n
        :return dict 返回结果\n
        注意这里的url是setdirectProxy或setdynamicProxy方法返回中的url
        """
        data=self._sendrequest("close",url)
        # print("打印响应结果：",data)
        return data
    def _init_proxy(self):
        """
        初始化代理
        """
        print("初始化代理")
        executable_path=self._getexecuteFile()
        shell=[executable_path]
        if self.port != 0:
            shell.append(f'--port={self.port}')
        if self.port_proxy != 0:
            shell.append(f'--proxy_port={self.port_proxy}')
       
        self.process=subprocess.Popen(shell,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if self.process.pid >=0:
            print(f"代理服务启动成功,进程id:{self.process.pid},http端口:{self.port},代理端口:{self.port_proxy}")
        # 等待程序执行完成
        stdout, stderr = self.process.communicate()
        if self.process.returncode != 0:
            # 如果返回码非0，表示程序有错误发生
            raise RuntimeError(f"代理启动失败:{stderr.decode()}")
    def start(self):
        # 启动线程
        self._th.start()
    def terminate(self):
        """
        终止当前代理进程
        """
        if self.process:
            self.process.kill()
            print("代理自动销毁")
    def killsearchName(self,name:str):
        """
        根据进程名称进行终止
        """
        p=subprocess.Popen('taskkill /f /im {}'.format('apiproxy.exe'))
        p.wait(2)
    def getexecuteName(self,executable_path:str) ->str:
        """
        根据程序路径获取当前进程名称
        """
        if not executable_path:
            raise RuntimeError("未找到程序路径")
        name=os.path.basename(executable_path)
        return name
    def __del__(self):
        """
        类销毁时执行,销毁代理
        """
        pass
        # self.terminate()
           
    def _getexecuteFile(self) ->str:
        """
        获取执行文件路径
        """
        __file_path=os.path.abspath(__file__)
        data_files = {}
        directories = glob.glob(os.path.join(os.path.dirname(__file_path), "dependencies/*"))
        for directory in directories:
            if "exe" in directory:
                data_files["win"]=directory
            elif "linux" in directory:
                data_files["linux"]=directory
            elif "mac" in directory:
                data_files["mac"]=directory
        
        if len(data_files)<=0:
            raise RuntimeError("未找到依赖文件")
        system_name = platform.system()
        system_name=self.system_list.get(system_name,"")
        executable_path=data_files.get(system_name,None)
        if executable_path is None:
            raise RuntimeError("未找到依赖文件")
        return executable_path
    def _sendrequest(self,_method:str,**kwargs)->dict:
        """
        与代理服务器进行通信\n
        :param _method 请求方法\n
        :param kwargs 请求参数\n
        :return dict 返回结果
        """
        header={
            "Content-Type":"application/json"
        }
        data=json.dumps(kwargs)
        url=f"{self.baseurl}/{_method}"
        response=requests.post(url,headers=header,data=data)
        return response.json()
if __name__ == "__main__":
    a=Proxy(8993,8996)
    a.setdynamicProxy("socks://127.0.0.1:10808")
    # print(a._getexecuteFile())
    while True:
        try:
            time.sleep(1)
            
            print("测试")
        except KeyboardInterrupt:
            break



