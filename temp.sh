#!/bin/bash
#SBATCH -p long
#SBATCH -t 24:00:00


for model in MODEL1 MODEL2 MODEL3 
do

## Go to each model's folder
cd $model

## Calculates the running mean for a seven-day window for each grid point and split it by month
cdo runmean,7 merged.nc week_mean.nc
cdo splitmon week_mean.nc week_mean_mon


mkdir masked_by_frost

## For each month, the river network is divided into points where the average temperature of the contributing basin is positive or negative
for month in 01 02 03 04 05 06 07 08 09 10 11 12  
do
	export model="$model"
	export month="$month"
	echo $simulation
	echo $month
	python3 basin.py 
	## Puts negative values whenever the frost season is present and thus should not be considered for the final result
	cdo mul /path/for/temperature/data/$model/frost$i week_mean_mon$i masked_by_frost/$i
done


## Recombines all months 
cdo mergetime  masked_by_frost/*.nc

## Eliminates all negative aka frost season data
cdo gtc,0 tmp.nc tmp2.nc
cdo setctomiss,0 tmp2.nc tmp3.nc
cdo mul tmp3.nc tmp.nc tmp4.nc

## Calculates the seven-day yearly minimum taking into account the frost season
cdo yearmin tmp4.nc q7.nc

rm tmp*.nc


cd ..
done

