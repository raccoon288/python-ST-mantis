from suds.client import Client
from suds import WebFault
from model.project import Project


class SoapHelper:
    def __init__(self, app):
        self.app = app

    def can_login(self, username, password, config):
        client = Client(config['web']['baseUrl'] + "/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_projects_list(self, config):
        client = Client(config['web']['baseUrl'] + "/api/soap/mantisconnect.php?wsdl")
        project_list = []
        objects = client.service.mc_projects_get_user_accessible(
            config['webadmin']["login"], config['webadmin']["password"])
        for row in objects:
            (id, name) = (row.id, row.name)
            project_list.append(Project(id=str(id), name=name))
        return project_list
