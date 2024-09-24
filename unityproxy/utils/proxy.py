import re
from typing import Optional, Literal, Union, Callable

from unityproxy import types
from .validator import DataValidator
from ..exceptions import invalid_params


class Proxy(DataValidator):
    __SEPARATORS = "[:;@,]"
    __PROXY_WITH_CREDS_REGEX = "(\w+)" + __SEPARATORS + "(\w+)" + __SEPARATORS + "(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" + __SEPARATORS + "(\d+)"
    __REVERSE_PROXY_WITH_CREDS_REGEX = "(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" + __SEPARATORS + "(\d+)" + __SEPARATORS + "(\w+)" + __SEPARATORS + "(\w+)"
    __PROXY_REGEX = "(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" + __SEPARATORS + "(\d+)"


    def __init__(self, ip: str, port: Union[int, str], type_: Union[types.PROXY_TYPEHINT, int], login: Optional[str] = None, password: Optional[str] = None) -> None:
        self._validate_ip(ip)
        self._validate_port(port)
        self.__type = self._convert_proxy_type(type_)
        self.__ip = ip
        self.__port = int(port)
        self.__login = login
        self.__password = password

        self.to = ConvertProxyTo(self)

    @property
    def type_(self) -> str:
        return self.__type
    
    @type_.setter
    def type_(self, value: Union[types.PROXY_TYPEHINT, int]):
        self.__port = self._convert_proxy_type(value)

    @property
    def ip(self) -> str:
        return self.__ip
    
    @ip.setter
    def ip(self, value: str) -> str:
        self._validate_ip(value)
        self.__ip = value
    
    @property
    def port(self) -> int:
        return self.__port
    
    @port.setter
    def port(self, value):
        self._validate_port(value)
        self.__port = value
    
    @property 
    def login(self) -> str:
        return self.__login
    
    @login.setter
    def login(self, value):
        self.__login = value
    
    @property
    def password(self) -> str:
        return self.__password
    
    @password.setter
    def password(self, value):
        self.__password = value
    
    @classmethod
    def from_regex(self, line: str, regex: Union[re.Pattern, str], proxy_type: types.PROXY_TYPEHINT, login_after_ip: bool=False, empty_creds: bool=False) -> 'Proxy':
        server = None
        port = None
        login = None
        password = None

        if not isinstance(line, str):
            raise TypeError(f"expected string object, got {type(line).__name__!r}")

        if not isinstance(line, (str, re.Pattern)):
            raise TypeError(f"expected re.Pattern or string object, got {type(regex).__name__!r}")
        
        searched = re.search(regex, line)
        if not searched:
            raise ValueError(f"line does not match regex")
        groups = list(searched.groups())

        if empty_creds:
            if len(groups) != 2:
                raise ValueError(f"regex output should contains 2 values")
            server, port = groups[0], groups[1]
        
        else:
            if len(groups) != 4:
                raise ValueError(f"regex output should contains 4 values")
            if login_after_ip:
                server, port, login, password = groups[0], groups[1], groups[2], groups[3]
            else:
                login, password, server, port = groups[0], groups[1], groups[2], groups[3]
        
        return Proxy(ip=server, port=port, type_=proxy_type, login=login, password=password)

 

    @classmethod
    def from_line(cls, line: str, proxy_type: types.PROXY_TYPEHINT="socks5", custom_parser: Callable=None) -> 'Proxy':
        if isinstance(custom_parser, Callable):
            parsed = custom_parser(line)
            if not isinstance(parsed, Proxy):
                raise invalid_params.InvalidCustomParserReturnType(f"custom parser should return Proxy type. {type(parsed).__name__!r} founded")
            return parsed
        
        #TODO beautify mb
        try:
            return cls.from_regex(line, cls.__PROXY_WITH_CREDS_REGEX, proxy_type=proxy_type, login_after_ip=False, empty_creds=False)
        except:...
        try:
            return cls.from_regex(line, cls.__REVERSE_PROXY_WITH_CREDS_REGEX, proxy_type=proxy_type, login_after_ip=True, empty_creds=False)
        except:
            ...
        try:
            return cls.from_regex(line, cls.__PROXY_REGEX, proxy_type=proxy_type, login_after_ip=False, empty_creds=True)
        except:
            ...
        
        raise invalid_params.CanNotParseProxy("can not parse proxy")



    def __repr__(self) -> str:
        return f"<Proxy ip={self.ip!r} port={self.port!r} type={self.type_!r} login={self.login!r} password={self.password!r}>"


class ConvertProxyTo:


    def __init__(self, proxy: Proxy) -> None:
        self.__obj = proxy

    def line(self) -> str:
        if not self.__obj.login:
            return f"{self.__obj.type_}://{self.__obj.ip}:{self.__obj.port}"
        return f"{self.__obj.type_}://{self.__obj.login}:{self.__obj.password}@{self.__obj.ip}:{self.__obj.port}"
    
    def requests(self) -> dict:
        line = self.line()
        return {
            "http": line,
            "https": line
        }

    def httpx_line(self) -> str:
        return self.line()

    def httpx_dict(self) -> dict:
        line = self.line()
        return {
            "http://": line,
            "https://": line
        }
    
    def aiohttp_line(self) -> str:
        return self.line()

    def telethon(self) -> dict:
        try: 
            import socks
            proxy_types = socks.PROXY_TYPES
        except ImportError:
            proxy_types = {"SOCKS4": 1, "SOCKS5": 2, "HTTP": 3}

        return (
            proxy_types.get(self.__obj.type_.upper()),
            self.__obj.ip,
            self.__obj.port,
            self.__obj.login,
            self.__obj.password
        )
    
    def pyrogram(self) -> dict:
        return {
            "scheme": self.__obj.type_,
            "hostname": self.__obj.ip,
            "port": self.__obj.port,
            "username": self.__obj.login,
            "password": self.__obj.password
        }
    