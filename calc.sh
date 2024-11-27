#!/bin/bash
#SBATCH -p esp
#SBATCH -t 24:00:00

##Add here the model/folders you wish to work with

for model in MODEL1 MODEL2 MODEL3
do 

mkdir $model

cd $model

## Merges all CHyM output files into one for easier processing
cdo mergetime /path/to/the/CHyM/output/files/*.nc merged.nc 

## Chooses the maximum yearly values for each grid point
cdo yearmax merged.nc yrmax.nc 



done
