# create input data directory
mkdir -p /data/CaloGAN/inputs/
cd /data/CaloGAN/inputs
wget -nc https://data.mendeley.com/archiver/pvn3xc3wy5?version=1 -O CaloGAN.zip
yes n | unzip CaloGAN.zip

mkdir -p /ML_platform_tests/tutorial/Ben
cd /ML_platform_tests/tutorial/Ben
git clone https://github.com/hep-lbdl/CaloGAN.git
cd /ML_platform_tests/tutorial/Ben/CaloGAN/models
echo "positron: '/data/CaloGAN/inputs/eplus.hdf5'" > particles.yaml
export SHELL=/bin/bash

python train.py "$@"
