# create input data directory
mkdir -p /data-rook/CaloGAN/inputs/
cd /data-rook/CaloGAN/inputs
wget -nc https://data.mendeley.com/archiver/pvn3xc3wy5?version=1 -O CaloGAN.zip
yes n | unzip CaloGAN.zip

# create weight data directory
mkdir -p /data-rook/CaloGAN/weights

#create output data directory
mkdir -p /data-rook/CaloGAN/outputs

cd /ML_platform_tests/tutorial/
git clone https://github.com/ivukotic/sc2017_prp.git
cd /ML_platform_tests/tutorial/sc2017_prp
export SHELL=/bin/bash

#python train.py "$@"
#python generator.py /data-rook/CaloGAN/weights/params_generator_epoch_049.hdf5 /data-rook/CaloGAN/outputs/images1.h5
python "$@"
