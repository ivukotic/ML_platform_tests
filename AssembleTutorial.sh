# Amir's tutorial

mkdir -p /data/tutorial/amir
cd /data/tutorial/amir
wget -N http://archive.ics.uci.edu/ml/machine-learning-databases/00279/SUSY.csv.gz
gunzip SUSY.csv.gz

# Ilija's tutorial
mkdir -p /data/tutorial/ilija
cd /data/tutorial/ilija

mkdir /root/.jupyter/
wget https://raw.githubusercontent.com/ivukotic/ML_platform_tests/master/jupyter_notebook_config.py
mv jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py
jupyter notebook --allow-root
