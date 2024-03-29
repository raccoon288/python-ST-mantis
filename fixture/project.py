class ProjectHelper:
    def __init__(self, app):
        self.app = app

    def create_project(self, project):
        wd = self.app.wd
        self.open_manage_projects_page()
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        self.fill_project_form(project)
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        self.open_manage_projects_page()

    def open_manage_projects_page(self):
        wd = self.app.wd
        if not (
                wd.current_url.endswith("/manage_proj_page.php") and
                len(wd.find_elements_by_xpath("//input[@value='Create New Project']")) > 0):
            wd.find_element_by_link_text("Manage").click()
            wd.find_element_by_link_text("Manage Projects").click()

    def fill_project_form(self, project):
        wd = self.app.wd
        wd.find_element_by_name("name").send_keys(project.name)
        if project.status is not None:
            wd.find_element_by_name("status").send_keys(project.status)
        if project.inherit == 0 or project.inherit is not None:
            wd.find_element_by_name("inherit_global").click()
        if project.view_state is not None:
            wd.find_element_by_name("view_state").send_keys(project.view_state)
        wd.find_element_by_name("description").send_keys(project.description)

    def delete_project_by_id(self, id):
        wd = self.app.wd
        self.open_manage_projects_page()
        wd.find_element_by_xpath("//a[@href='manage_proj_edit_page.php?project_id=%s']" % id).click()
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        self.open_manage_projects_page()




