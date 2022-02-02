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

# mkdir /workspace/
# mkdir /root/.jupyter/
# wget https://raw.githubusercontent.com/ivukotic/ML_platform_tests/master/private_jupyter_notebook_config.py
# mv private_jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py

wget https://raw.githubusercontent.com/ivukotic/ML_platform_tests/master/add_lozinka.py
python3 add_lozinka.py "$1"

if [ "$2" != "" ]; then
    echo "Git Repo $2 requested..."
    cd /workspace/
    git clone $2
fi

cp -r /ML_platform_tests/tutorial /workspace/

export SHELL=/bin/bash

jupyter lab --allow-root --ServerApp.allow_password_change=False --no-browser --config=/root/.jupyter/jupyter_notebook_config.py
