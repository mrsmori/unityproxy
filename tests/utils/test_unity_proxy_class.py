import pytest

from unityproxy.utils.unity import UnityProxy
from unityproxy.exceptions import invalid_params as exceptions


@pytest.mark.parametrize("line", 
    (
        "{login}:{password}@{ip}:{port}",
        "{login}:{password}:{ip}:{port}",
        "{ip}:{port}@{login}:{password}",
        "{ip}:{port}:{login}:{password}",
        "{ip};{port};{login};{password}",
        "{login};{password};{ip};{port}",
        "{ip}@{port}@{login}@{password}",
    )
)
def test_ignore_errors_true(line: str):
    ip = "invalid"
    port = 8080
    login = "login"
    password = "password"
    created_line = line.format(login=login, password=password, ip=ip, port=port)

    unity = UnityProxy(ignore_parse_errors=True)
    unity.add_by_line(created_line, "socks5")

    assert (len(unity._UnityProxy__proxies) == 0)


@pytest.mark.parametrize("line", 
    (
        "{login}:{password}@{ip}:{port}",
        "{login}:{password}:{ip}:{port}",
        "{ip}:{port}@{login}:{password}",
        "{ip}:{port}:{login}:{password}",
        "{ip};{port};{login};{password}",
        "{login};{password};{ip};{port}",
        "{ip}@{port}@{login}@{password}",
    )
)
def test_ignore_errors_false(line: str):
    ip = "invalid"
    port = 8080
    login = "login"
    password = "password"
    created_line = line.format(login=login, password=password, ip=ip, port=port)

    unity = UnityProxy(ignore_parse_errors=False)

    with pytest.raises(exceptions.CanNotParseProxy):
        unity.add_by_line(created_line, "socks5")

    assert (len(unity._UnityProxy__proxies) == 0)
