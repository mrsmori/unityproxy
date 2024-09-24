import re
from typing import Union, Tuple, Dict

from ..exceptions import invalid_params


class DataValidator:
    __IP_REGEX: re.Pattern = re.compile("((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}")
    __PROXY_TYPES: Tuple[str] = ("http", "socks4", "socks5")
    __PYSOCKS_TYPES: Dict[int, str] = {1: "socks4", 2: "socks5", 3: "socks5"}
    
    def _validate_ip(self, ip: str) -> bool:
        if not isinstance(ip, str):
            raise invalid_params.InvalidIpType(f"expected string object, got {type(ip).__name__!r}")
        
        if re.match(self.__IP_REGEX, ip) == None:
            raise invalid_params.InvalidIpValue("does not match regex")
    
    def _validate_port(self, port: Union[str, int]):
        if not isinstance(port, (int, str)):
            raise invalid_params.InvalidPortType(f"expected string or int object, got {type(port).__name__!r}")
        
        if isinstance(port, str) and not port.isdigit():
            raise invalid_params.InvalidPortType("port value should be valid integer")
        
    def _convert_proxy_type(self, proxy_type: Union[str, int]) -> str:
        if not isinstance(proxy_type, (str, int)):
            raise invalid_params.InvalidTypeProxyType(f"expected string or int object, got {type(proxy_type).__name__!r}")
        
        if isinstance(proxy_type, int) or proxy_type.isdigit():
            proxy_type = self.__PYSOCKS_TYPES.get(int(proxy_type))
            if proxy_type is None:
                raise invalid_params.InvalidTypeProxyValue(f"int proxy type is not in pysocks range (1, 2, 3)")
            return proxy_type

        if isinstance(proxy_type, str):
            lower_proxy = proxy_type.strip().lower()
            if not lower_proxy in self.__PROXY_TYPES:
                raise invalid_params.InvalidTypeProxyType(f"str proxy type is invalid")
            return lower_proxy
        
        raise invalid_params.InvalidTypeProxyValue("unconvertable proxy")

    @staticmethod
    def _search_ip(line: str) -> re.Match:
        return re.search(DataValidator.__IP_REGEX, line)
        
