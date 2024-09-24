import pytest


from unityproxy.utils.proxy import Proxy


def test_manual_data():
    Proxy(
        "120.0.0.3",
        80,
        "socks4",
    )
    Proxy(
        "120.0.0.3",
        80,
        "socks4",
        "login",
        "password"
    )

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
def test_from_line_with_creds(line: str):
    ip = "127.0.0.1"
    port = 8080
    login = "login"
    password = "password"

    created_line = line.format(login=login, password=password, ip=ip, port=port)

    data = Proxy.from_line(created_line)
    assert data.ip == ip
    assert data.port == port
    assert data.login == login
    assert data.password == password