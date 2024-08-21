#*************
# File: test.py 
# Description: 
# Step 1: Load the DTU_ADN 60 kV network. 
# Step 2: Update the load and generation values for the 60 kV network corresponding to the timestamp 
# Step 3: Run a power flow for the 60 kV network
# ---end of file
# Author: Aeishwarya Baviskar
# email: aeish@dtu.dk
#------------------------------


# User Defined functions
from DTU_ADN import DTU_ADN  # import DTU_ADN class

main_net_dataset = DTU_ADN()  # load the main network dataset

# main_net_dataset.net = 60 kV network 

# select a time-stamp for power flow
t0 = 100 

# load the generation and demand values at that time stamp
main_net_dataset.gen_and_demand_net_60(t0)

# run power flow and save results in pf_result network dataset
pf_result = DTU_ADN.runpf(main_net_dataset.net)

## *** end of file *** ##