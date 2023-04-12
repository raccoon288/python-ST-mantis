from model.project import Project
import random
import string
import os
import jsonpickle
import getopt
import sys


try:
    opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["number of projects", "file"])
except getopt.GetoptError as err:
    sys.exit(2)

n = 5
f = "data/projects.json"

for o, a in opts:
    if o == "-n":
        n = int(a)
    elif o == "-f":
        f = a


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + " "*10
    random_len = random.randrange(maxlen)
    random_line = [random.choice(symbols) for i in range(random_len)]
    return prefix + "".join(random_line)


status_list = ['development', 'release', 'stable', 'obsolete']
state_list = ['public', 'private']

testdata = [
            Project(name=random_string("name", 10),
                    status=random.choice(status_list),
                    inherit=random.randint(0, 1),
                    view_state=random.choice(state_list),
                    description=random_string("description", 20))
            for i in range(n)
           ]

abs_path = os.path.abspath(__file__)
dir_name = os.path.dirname(abs_path)
file = os.path.join(dir_name, "..", f)
with open(file, "w") as out:
    jsonpickle.set_encoder_options("json", indent=2)
    out.write(jsonpickle.encode(testdata))
