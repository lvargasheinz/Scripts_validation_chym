
In order to match the grid points of the river network produced by CHyM to the coordinates of each station, use the following MatLab script:

nearest_point.m  


In order to extract those same grid points from a large NetCDF file comprising the whole river network to individual NetCDF files, use the following shell script: 

points.sh


_________________________________________________________________________________________________________________________________________________________________


FLOW DURATION CURVES

-> First merge the timeframe you want to study into a single NetCDF file (calc.sh)

-> Extract the grid points of interest from your merged file (points.sh)

-> Using plot_all.sh to go through all points, plot individually for each point of interest the data from all models and from station data (flow_dur_individual.py)


_________________________________________________________________________________________________________________________________________________________________


PEAK DISCHARGE CURVES

-> First merge the timeframe you want to study into a single NetCDF file and calculate the yearly maximum for all points (calc.sh)

-> Extract the grid points of interest from your yearly maximum file (points.sh)

-> Using plot_all.sh to go through all points, lot individually for each point of interest the data from all models and from station data (peak_dis_individual.py)


_________________________________________________________________________________________________________________________________________________________________


LOW DISCHARGE CURVES

-> First merge the timeframe you want to study into a single NetCDF file (calc.sh) and follow the steps in temp.sh to get a yearly seven day minimum that takes into account the frost season

-> Extract the grid points of interest from your yearly minimum file (points.sh)

-> Using plot_all.sh to go through all points, lot individually for each point of interest the data from all models and from station data (drought_individual.py)



