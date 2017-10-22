# setup ROOT
cd /opt/root/
source bin/thisroot.sh
# copy ROOT kernel into Jupyter
mkdir -p /root/.local/share/jupyter/kernels
cp -r $ROOTSYS/etc/notebook/kernels/root ~/.local/share/jupyter/kernels

mkdir /root/.jupyter/
wget https://raw.githubusercontent.com/ivukotic/ML_platform_tests/master/jupyter_notebook_config.py
mv jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py
jupyter lab --allow-root
