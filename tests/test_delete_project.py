from model.project import Project
import random


# def test_delete_project_by_id(app, db):
#     if len(db.get_project_list()) == 0:
#         app.project.create_project(Project(name='lala', status='development'))
#     old_projects = db.get_project_list()
#     random_project = random.choice(old_projects)
#     app.project.delete_project_by_id(random_project.id)
#     new_projects = db.get_project_list()
#     old_projects.remove(random_project)
#     assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)

def test_delete_project_by_id(app, config):
    if len(app.soap.get_projects_list(config['webadmin']["login"], config['webadmin']["password"])) == 0:
        app.project.create_project(Project(name='lala', status='development'))
    old_projects = app.soap.get_projects_list(config['webadmin']["login"], config['webadmin']["password"])
    random_project = random.choice(old_projects)
    app.project.delete_project_by_id(random_project.id)
    new_projects = app.soap.get_projects_list(config['webadmin']["login"], config['webadmin']["password"])
    old_projects.remove(random_project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)