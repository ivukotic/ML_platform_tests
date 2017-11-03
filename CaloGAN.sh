# create input data directory
mkdir -p /data/CaloGAN/inputs/
cd /data/CaloGAN/inputs
wget -nc https://data.mendeley.com/archiver/pvn3xc3wy5?version=1 -O CaloGAN.zip
yes n | unzip CaloGAN.zip

# create weight data directory
mkdir -p /data/CaloGAN/weights

#create output data directory
mkdir -p /data/CaloGAN/outputs

mkdir -p /ML_platform_tests/tutorial/CaloGAN
cd /ML_platform_tests/tutorial/
git clone https://github.com/ivukotic/sc2017_prp.git
cd /ML_platform_tests/tutorial/sc2017_prp
export SHELL=/bin/bash

#python train.py "$@"
#python generator.py /data/CaloGAN/weights/params_generator_epoch_049.hdf5 /data/CaloGAN/outputs/images1.h5
python "$@"
