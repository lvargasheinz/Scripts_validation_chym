#!/bin/bash
#SBATCH -p esp
#SBATCH -t 24:00:00

##Add here the model/folders you wish to extract the grid points from
for model in MODEL1 MODEL2 MODEL3
do 

mkdir $model/points

## Change field1, field2 and field3 if necessary, i.e. if the csv file does not contain the longitude as the first column and the latitude as the second column
while IFS=, read -r field1 field2 field3
do
    echo "$field1 and $field2"

    ### Change the name for the file you wish to extract the point data from
    ncks -v dis -d lon,$field1 -d lat,$field2 ./$model/your_file.nc  $model/points/extracted_{$field1}_{$field2}.nc
done <  coord_SAM_model.csv

done
