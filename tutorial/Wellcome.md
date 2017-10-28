# Welcome to the Machine Learning Platform

Our goal is to provide an out-of-the-box working platform for most machine learning needs of high energy physics and astrophysics. For this we have been given access to the GPU and storage resources of the [Pacific Research Platform](http://prp.ucsd.edu/). 
Each Jupyter instance has access to one GPU (GTX 1080 or TitanX), a shared storage space in the directory labeled `/data/`, and a cloned repository with ML example codes used for the [EFI Data Analytics for Physics workshop](https://efi.uchicago.edu/content/efi-data-analytics-physics), October 30 - November 1, 2017.

Each instance should be considered transient so if you want to keep your code, have a copy elsewhere (locally on your computer, github,...).


Jupyter comes with Python2, Python3 and ROOT kernels.
ROOT 6.10 is installed in default location.

Most of ML libraries are installed. If you need additial packages feel free to install them using `pip2 install xxx` or `pip3 install xxx` commands. If you think the missing package would be of wider use please contact Ilija Vukotic <mailto:ivukotic@cern.ch> and we will consider it for inclusion.

In case anything is messed up with your Jupyter instance let us know and we will recreate it (you would loose all the data). The new instance will be accessible at the same address as the old one.
