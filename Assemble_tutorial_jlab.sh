# Amir's tutorial

mkdir -p /data/tutorial/amir
cd /data/tutorial/amir
wget -N http://archive.ics.uci.edu/ml/machine-learning-databases/00279/SUSY.csv.gz
yes n | gunzip SUSY.csv.gz

# Ilija's tutorial
mkdir -p /data/tutorial/ilija
cd /data/tutorial/ilija

# Ben's tutorial
mkdir -p /data/tutorial/Ben
cd /data/tutorial/Ben
wget -nc https://data.mendeley.com/archiver/pvn3xc3wy5?version=1 -O CaloGAN.zip
yes n | unzip CaloGAN.zip

mkdir -p /ML_platform_tests/tutorial/Ben
cd /ML_platform_tests/tutorial/Ben
git clone https://github.com/hep-lbdl/CaloGAN.git
cd /ML_platform_tests/tutorial/Ben/CaloGAN/models
echo "positron: '/data/tutorial/Ben/eplus.hdf5'" > particles.yaml
# python -m train particles.yaml

# setup ROOT
cd /opt/root/
source bin/thisroot.sh
# copy ROOT kernel into Jupyter
mkdir -p /root/.local/share/jupyter/kernels
cp -r $ROOTSYS/etc/notebook/kernels/root ~/.local/share/jupyter/kernels
 
# install root-pandas and root-numpy
pip2 install root-pandas
pip3 install root-pandas

# for Max's tutorial
ln -s /usr/lib/x86_64-linux-gnu/libxml2.so.2.9.3 /usr/lib/x86_64-linux-gnu/libxml2.so

mkdir /root/.jupyter/
wget https://raw.githubusercontent.com/ivukotic/ML_platform_tests/master/jupyter_notebook_config.py
mv jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py
export SHELL=/bin/bash

jupyter lab --allow-root
