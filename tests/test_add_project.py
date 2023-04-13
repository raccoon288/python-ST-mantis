from model.project import Project
from generator.project import random_string


def test_add_project(app, db, json_projects):
    project = json_projects
    assert project.name != "" or project.name is not None
    old_projects = db.get_project_list()
    app.project.create_project(project)
    new_projects = db.get_project_list()
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
