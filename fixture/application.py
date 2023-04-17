from selenium import webdriver
from fixture.session import SessionHelper
from fixture.project import ProjectHelper
from fixture.james import JamesHelper
from fixture.signup import SignupHelper
from fixture.mail import MailHelper
from fixture.soap import SoapHelper


class Application:
    def __init__(self, browser, config):
        if browser == "firefox":
            self.wd = webdriver.Firefox(firefox_binary=r'C:\Program Files\Mozilla Firefox\firefox.exe')
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "opera":
            self.wd = webdriver.Opera()
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        self.wd.implicitly_wait(2)
        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)
        self.james = JamesHelper(self)
        self.signup = SignupHelper(self)
        self.mail = MailHelper(self)
        self.soap = SoapHelper(self)
        self.base_url = config['web']['baseUrl']
        self.config = config

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def open_home_page(self):
        wd = self.wd
        wd.get(self.base_url)

    def destroy(self):
        self.wd.quit()
