import sys
from notebook.auth import passwd
print('lozinka:', sys.argv[1])
lozinka = passwd(sys.argv[1])
print('adding hash', lozinka)
with open("/root/.jupyter/jupyter_notebook_config.py", "a") as myfile:
    myfile.write("c.NotebookApp.password = '" + lozinka + "'\n")
