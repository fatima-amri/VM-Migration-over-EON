## Energy-Aware Inter-DC VM Migration Over Elastic Optical Networks
This repository contains the code for the submission "Energy-Aware Inter-Data Center VM Migration Over Elastic Optical Networks" to Globecom 2023.
#

### Steps to Reproduce Results

To reproduce the results in this project, please follow these steps:
1. Clone the repository to your local machine:

``` git clone https://github.com/fatima-amri/VM-Migration-over-EON.git ```

2. Install the required Python libraries. You can do this using pip:

``` pip install numpy``` 

Other libraries that are required to be installed are, Networkx, Math and Collections, Deque.

Open the project in your preferred Python IDE. We recommend using PyCharm.
Run the main .py file in your Python IDE. This will run the simulations and generate the results.

Please note that you need to repeat the simulation for different number of requests and plot the figures.
To plot the figures, you will need MATLAB installed on your machine. Open the .m files in MATLAB and run it.

Note: The code was tested with Python 3.9.6 and MATLAB R2017a.

#

### Topologies

Our code can be used with various network topologies in different scales. For the experiments reported in our paper, we used the NSFNET topologies, which are included in this repository. Due to the page size limitation, we only report the results for the NSFNET topologies. However, we have also included two other topologies in this repository, one smaller (Six-node) and one larger (USNET), that can be used for testing purposes. 
To use a different topology, simply provide the corresponding topology as input to the script.

#

#### Files Description

`MigrationFunctions.py:` This is the main migration code file which includes the Controller checkup, MAB and optical grooming functions of the proposed algorithms for inter-DC VM migration using MAB and CMAB.

`SideFunctions.py:` This code file contains required functions that are called in the `MigrationFunctions.py`.

`Main.py:` This is the code file that contains the run and result retrieval section.

`Figures/:` This folder contains the figures generated by Matlab that show the simulation results for different scenarios and parameters on NSFNET topologies.

`Topology.txt:` This folder includes different topologies that can be used in the simulations.
  

