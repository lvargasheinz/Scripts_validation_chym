#!/bin/bash
#SBATCH -p long
#SBATCH -t 24:00:00


## Insert the path to a csv file with longitude, latitude and station name data for all grid points
for line in $(cat "path/to/coordinates_file.csv"); do

  ## Adjust according to column placement inside the csv file
  field1=$(echo "$line" | cut -d, -f1)
  field2=$(echo "$line" | cut -d, -f2)
  field3=$(echo "$line" | cut -d, -f3)
  echo $field1 $field2 $field3

  export lon="$field1"
  export lat="$field2"
  export station="$field3"

  ## Run as wished 
#  python3 flow_dur_indiviual.py
#  python3 peak_dis_individual.py
#  python3 drought_individual.py

done
