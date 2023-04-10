import pytest
from fixture.application import Application
import json
import os.path


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


@pytest.fixture()
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--target"))['web']
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_config["baseUrl"])
    return fixture


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
