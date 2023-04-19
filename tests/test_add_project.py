from model.project import Project


# def test_add_project(app, db, json_projects):
#     project = json_projects
#     assert project.name != "" or project.name is not None
#     old_projects = db.get_project_list()
#     app.project.create_project(project)
#     new_projects = db.get_project_list()
#     old_projects.append(project)
#     project_list = app.soap.get_projects_list("administrator", "root")
#     assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)

def test_add_project(app, config, json_projects):
    project = json_projects
    assert project.name != "" or project.name is not None
    old_projects = app.soap.get_projects_list(config)
    app.project.create_project(project)
    new_projects = app.soap.get_projects_list(config)
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
