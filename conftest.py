import pytest
from fixture.application import Application
from fixture.db import DbFixture
import json
import os.path
import importlib
import jsonpickle
import ftputil


fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        abs_path = os.path.abspath(__file__)
        dir_name = os.path.dirname(abs_path)
        config_file = os.path.join(dir_name, file)
        with open(config_file) as file:
            target = json.load(file)
    return target


@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))

@pytest.fixture()
def app(request, config):
    global fixture
    browser = request.config.getoption("--browser")
    web_url = config['web']
    web_admin = config['webadmin']
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_url["baseUrl"])
    # fixture.session.ensure_login(login=web_admin["login"], password=web_admin["password"])
    return fixture


@pytest.fixture(scope="session")
def db(request, config):
    db_config = config['db']
    dbfixture = DbFixture(host=db_config['host'], name=db_config["name"],
                          user=db_config["user"], password=db_config['password'])
    def fin():
        dbfixture.destroy()
    request.addfinalizer(fin)
    return dbfixture


@pytest.fixture(scope="session", autouse=True)
def configer_server(request, config):
    install_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    def fin():
        restore_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    request.addfinalizer(fin)


def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            remote.remove("config_inc.php.bak")
        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php", "config_inc.php.bak")
        remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_inc.php"), "config_inc.php")


def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            if remote.path.isfile("config_inc.php"):
                remote.remove("config_inc.php")
            remote.rename("config_inc.php.bak", "config_inc.php")

@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")


def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])
        elif fixture.startswith("json_"):
            testdata = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])


def load_from_module(module):
    return importlib.import_module("data.%s" % module).testdata


def load_from_json(file):
    abs_path = os.path.abspath(__file__)
    dir_name = os.path.dirname(abs_path)
    file_path = os.path.join(dir_name, "data/%s.json" % file)
    with open(file_path) as f:
        return jsonpickle.decode(f.read())
