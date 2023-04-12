from model.project import Project


def test_add_project(app, db):
    old_projects = db.get_project_list()
    app.project.create_project(Project(name='lala', status='development', inherit=0, view_state='public', description='desc'))
    new_projects = db.get_project_list()
    old_projects.append(Project(name='lala', status='development', inherit=0, view_state='public', description='desc'))
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
