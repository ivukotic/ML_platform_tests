# setup ROOT
cd /opt/root/
source bin/thisroot.sh
# copy ROOT kernel into Jupyter
mkdir -p /root/.local/share/jupyter/kernels
cp -r $ROOTSYS/etc/notebook/kernels/root ~/.local/share/jupyter/kernels
 
# install root-pandas and root-numpy
pip2 install root-pandas
pip3 install root-pandas

pip2 install RISE
pip3 install RISE
jupyter-nbextension install rise --py --sys-prefix
jupyter-nbextension enable rise --py --sys-prefix

mkdir /workspace/
mkdir /root/.jupyter/
wget https://raw.githubusercontent.com/ivukotic/ML_platform_tests/master/private_jupyter_notebook_config.py
mv private_jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py

wget https://raw.githubusercontent.com/ivukotic/ML_platform_tests/master/add_lozinka.py
python add_lozinka.py "$@"

export SHELL=/bin/bash

jupyter lab --allow-root
