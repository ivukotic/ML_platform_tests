# Wellcome to ML platform

We are trying to provide out-of-the-box working platform for most ML needs of high energy physics and astrophysics needs. 
Each jupyter instance has access to one GPU (GTX 1080 or TitanX), shared (among instances) storage space in directory /data/, and already cloned repository with ML example codes used for Enrico Fermi Institue ML workshop.

Each instance should be considered transient so if you want to keep your code, have a copy elsewhere (locally on your computer, github,...)


Jupyter comes with Python2, Python3 and ROOT kernels.
ROOT 6.10 is installed in default location.

Most of ML libraries are installed, if you need additial packages feel free to install them usign pip2 install xxx or pip3 install xxx commands.
If you think the missing package would be of wider use please contact Ilija Vukotic <mailto:ivukotic@cern.ch> and we will consider it for inclusion.

In case anything is messed up with your Jupyter instance let us know and we will recreate it (you would loose all the data). The new instance will be accessible at the same address as the old one.
