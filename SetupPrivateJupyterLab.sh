# setup ROOT
cd /opt/root/
source bin/thisroot.sh
# copy ROOT kernel into Jupyter
mkdir -p /root/.local/share/jupyter/kernels
cp -r $ROOTSYS/etc/notebook/kernels/root ~/.local/share/jupyter/kernels
 
python3.8 -m pip --no-cache-dir install  root-pandas 

# With RISE, a Jupyter notebook extension, you can instantly turn your jupyter notebook into a live reveal.js-based presentation.
jupyter-nbextension install rise --py --sys-prefix
jupyter-nbextension enable rise --py --sys-prefix

if [ "$1" != "" ]; then
    echo "Git Repo $1 requested..."
    cd /workspace/
    git clone $1
fi

cp -r /ML_platform_tests/tutorial /workspace/

export SHELL=/bin/bash

# setting up users
if [ "$OWNER" != "" ]; then
    /sync_users_debian.sh -u root.atlas-af -g root.atlas-af -e https://api.ci-connect.net:18080
    su - $OWNER
    
    jupyter lab --ServerApp.allow_password_change=False --no-browser --config=/usr/local/etc/jupyter_notebook_config.py

else
    jupyter lab --allow-root --ServerApp.allow_password_change=False --no-browser --config=/usr/local/etc/jupyter_notebook_config.py
fi 
