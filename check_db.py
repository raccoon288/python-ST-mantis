import pymysql.cursors
from fixture.db import DbFixture

db = DbFixture(host="127.0.0.1", name="bugtracker", user="root", password="")

try:
    list = db.get_project_list()
    for l in list:
        print(l)
finally:
    db.destroy()
