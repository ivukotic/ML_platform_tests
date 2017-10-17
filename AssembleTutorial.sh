# Amir's tutorial

mkdir -p /data/tutorial/amir
cd /data/tutorial/amir
wget https://github.com/UTA-HEP-Computing/DSatHEP-Tutorial/blob/master/IntroToDLwithKeras.ipynb
wget http://archive.ics.uci.edu/ml/machine-learning-databases/00279/SUSY.csv.gz
gunzip SUSY.csv.gz

# Ilija's tutorial
mkdir -p /data/tutorial/ilija
cd /data/tutorial/ilija

jupyter notebook --allow-root
