import json
import os
from queue import Queue
from io import TextIOWrapper
from copy import deepcopy
from typing import List, Union, Callable
from functools import wraps

from .proxy import Proxy
from ..types import PROXY_TYPEHINT


class UnityProxy:

    def __init__(self, ignore_parse_errors: bool = True, custom_parser: Callable=None) -> None:
        if not isinstance(ignore_parse_errors, bool):
            raise TypeError(f"expected bool object, got {type(ignore_parse_errors).__name__!r}")
        if custom_parser is not None and  not isinstance(custom_parser, Callable):
            raise TypeError(f"expected callable object, got {type(custom_parser).__name__!r}")
        
        self.__ignore_err = ignore_parse_errors
        self.__custom_parser = custom_parser
        self.__proxies: list[Proxy] = []

        self.__iteration_index = -1

        self.from_ = UnityAddFrom(self)
        self.to = UnityConvertTo(self)

    def ignore_errors(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            if self.__ignore_err:
                try:
                    return method(self, *args, **kwargs)
                except Exception as err:
                    print(f"ignored error in {method.__name__}: {err}")
            else:
                return method(self, *args, **kwargs)
        return wrapper

    @ignore_errors
    def add_by_line(self, line: str, proxy_type: PROXY_TYPEHINT):
        self.__proxies.append(Proxy.from_line(line, proxy_type, self.__custom_parser))

    @ignore_errors
    def add_by_values(self, ip: str, port: int, type_: PROXY_TYPEHINT, login: str=None, password: str=None):
        self.__proxies.append(Proxy(ip=ip, port=port, type_=type_, login=login, password=password))
        
    def remove(self, proxy: Proxy):
        self.__proxies.remove(proxy)

    def __len__(self) -> int:
        return len(self.__proxies)
    
    def __iter__(self):
        return self
    
    def __next__(self) -> Proxy:
        self.__iteration_index += 1
        if self.__iteration_index >= len(self.__proxies):
            self.__iteration_index = -1
            raise StopIteration
        return self.__proxies[self.__iteration_index]
    
    def __getitem__(self, i: int) -> Proxy:
        return self.__proxies[i]



class UnityAddFrom:

    def __init__(self, unity: UnityProxy) -> None:
        self.__obj = unity

    def reader(self, fp: TextIOWrapper, proxy_type: PROXY_TYPEHINT) -> UnityProxy:
        line = fp.readline()
        while line:
            self.__obj.add_by_line(line, proxy_type)
            line = fp.readline()
        return self.__obj
    
    def txt_file(self, path: str, proxy_type: PROXY_TYPEHINT):
        if not os.path.exists(path):
            raise FileNotFoundError("file to parse can not be found")
        with open(path, "r", encoding="utf-8") as f:
            self.reader(f, proxy_type)
        return self.__obj
    
    def json_file(self, path: str, proxy_type: PROXY_TYPEHINT):
        if not os.path.exists(path):
            raise FileNotFoundError("file to parse can not be found")
        
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if not isinstance(data, (list, tuple)):
            raise ValueError("Can not parse this file")
        
        for el in data:
            ip = el.get("ip")
            port = el.get("port")
            login = el.get("username") or el.get("login")
            password = el.get("password")
            self.__obj.add_by_values(ip=ip, port=port, type_=proxy_type, login=login, password=password)
        
        return self.__obj
        

        
class UnityConvertTo:


    def __init__(self, unity: UnityProxy) -> None:
        self.__obj = unity

    def list(self) -> List[Proxy]:
        # mb from copy import deepcopy
        return [deepcopy(proxy) for proxy in self.__obj]
    
    def queue(self) -> Queue[Proxy]:
        q = Queue()
        for proxy in self.__obj:
            q.put(deepcopy(proxy))
        return q
