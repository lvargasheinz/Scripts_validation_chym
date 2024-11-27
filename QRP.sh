#!/bin/bash
#SBATCH -p esp
#SBATCH -t 24:00:00

export calculation="Q100"
for model in  GERICS-REMO2015_MOHC-HadGEM2-ES_r1  GERICS-REMO2015_MPI-M-MPI-ESM-LR_r1 GERICS-REMO2015_NCC-NorESM1-M_r1 ICTP-RegCM4-7_MOHC-HadGEM2-ES_r1  ICTP-RegCM4-7_MPI-M-MPI-ESM-MR_r1 ICTP-RegCM4-7_NCC-NorESM1-M_r1 
do 
export model="$model"
echo $model
cd /home/netapp-clima/scratch/lvargas/SAM/$model
python3 /home/netapp-clima/scratch/lvargas/SAM/scripts/QRP.py
done
