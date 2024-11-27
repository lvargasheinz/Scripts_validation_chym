#make sure to run "export GDAL_MAX_BAND_COUNT=259200" on bash if needs more bands

from netCDF4 import Dataset
from scipy.stats import gumbel_r , gumbel_l
from osgeo import gdal
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
from os.path import isfile, join
from os import listdir
import matplotlib.pyplot as plt
import matplotlib
import netCDF4 as nc
from scipy import sparse

import matplotlib.pyplot as plt

import numpy as np
from numpy import exp
from scipy.special import factorial
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import statsmodels.api as sm
from statsmodels.api import Poisson
from scipy import stats
from scipy.stats import norm
from statsmodels.iolib.summary2 import summary_col

import numpy as np
import scipy.stats as st
import statsmodels.datasets
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

simulation=os.environ.get('model')
calculation = os.environ.get('calculation')
	
lon_size = 1017 ;
lat_size = 1183 ;

if calculation=="Q10":
	TR=10
elif calculation=="Q50":
	TR=50
elif calculation=="Q100":
	TR=100
print('Loading now')
#TR=10
pathresult=join("/home/netapp-clima/scratch/lvargas/SAM/"+simulation+"/")

nc_results = [f for f in listdir(pathresult) if isfile(join(pathresult, f)) if f.startswith("") and f.endswith("yrmax_his.nc")]
ds = [gdal.Open("NETCDF:{0}:{1}".format(pathresult + f,"dis")) for f in nc_results]
yrmax=[f.ReadAsArray(0, 0, f.RasterXSize, f.RasterYSize) for f in ds]
yrmax=np.asarray(yrmax)
yrmax=yrmax[0]
print(np.shape(yrmax))
#yrmax[yrmax>100000]=0 #np.nan
#yrmax[np.equal(yrmax,0)]=np.nan

ds_lon = [gdal.Open("NETCDF:{0}:{1}".format(pathresult + f,"lon")) for f in nc_results]#aqui tem problema pra abrir td
longitude = [f.ReadAsArray(0, 0, f.RasterXSize, f.RasterYSize) for f in ds_lon]
ds_lat = [gdal.Open("NETCDF:{0}:{1}".format(pathresult + f,"lat")) for f in nc_results]#aqui tem problema pra abrir td
latitude = [f.ReadAsArray(0, 0, f.RasterXSize, f.RasterYSize) for f in ds_lat]
latitude=np.asarray(latitude)
longitude=np.asarray(longitude)
latitude=latitude[0]
latitude=latitude[0]
longitude=longitude[0]
longitude=longitude[0]
print('Loaded')
#print(yrmax)
#exit 
media =np.mean(yrmax,0) # Yauyos[Yauyos>0].mean()
std = np.std(yrmax,0)
tabs= np.arange(-5000,18000,25)
dist=np.zeros((5,lat_size,lon_size))
Q10=np.zeros((lat_size,lon_size))
size = np.size(tabs)
valor=1-1/TR
a=0
print(lat_size,lon_size)
for i in range(lat_size):
	for j in range(lon_size):
		y = yrmax[:,i,j]
		y = y[~(np.isnan(y))]
		y = y[~(y>10000)]
		non_zero_count = sum(1 for value in y if value != 0)             
#		print(np.size(y))
#		print(y)
		if np.size(y)==0 or np.size(y)==1 or np.all(y == y[0]) or non_zero_count == 1:
			a=a+1
			Q10[i,j]=0
		else:
			print(y)
			params = gumbel_r.fit(y)
			scale = params[-1]
			arg = params[:-2]
			loc = params[-2]	#	Q10[i,j] = gumbel_l.ppf([0.9],dist[i,j])# loc=media[i,j], scale=std[i,j])
			Q10[i,j]=gumbel_r.ppf([valor],loc=loc, scale=scale)
print(a)
Q10[np.isnan(Q10)]=0








print('Done calculating')


Q10=np.flip(Q10, 0)




try: ncfile.close()  # just to be safe, make sure dataset is not already open.
except: pass
ncfile = Dataset(join(pathresult+calculation+'.nc') ,mode='w',format='NETCDF4_CLASSIC') 
print(ncfile)
lat_dim = ncfile.createDimension('lat', lat_size)     # latitude axis
lon_dim = ncfile.createDimension('lon', lon_size)    # longitude axis
time_dim = ncfile.createDimension('time', None) # unlimited axis (can be appended to).
for dim in ncfile.dimensions.items():
    print(dim)

ncfile.title=join('testenc'+calculation)
print(ncfile.title)

ncfile.subtitle=calculation
print(ncfile.subtitle)
print(ncfile)

# Define two variables with the same names as dimensions,
# a conventional way to define "coordinate variables".
lat = ncfile.createVariable('lat', np.float32, ('lat',))
lat.units = 'degrees_north'
lat.long_name = 'latitude'
lon = ncfile.createVariable('lon', np.float32, ('lon',))
lon.units = 'degrees_east'
lon.long_name = 'longitude'
time = ncfile.createVariable('time', np.float64, ('time',))
time.units = 'seconds since 1976-01-01 00:00:00 UTC'
time.long_name = 'time'
# Define a 3D variable to hold the data
Q = ncfile.createVariable('peak_discharge',np.float64,('time','lat','lon')) # note: unlimited dimension is leftmost
Q.standard_name = 'Peak_discharge' # this is a CF standard name
lat[:]=latitude
lon[:]=longitude

nlats = len(lat_dim); nlons = len(lon_dim);# ntimes = 3

# Write latitudes, longitudes.
# Note: the ":" is necessary in these "write" statements
# create a 3D array of random numbers
data_arr=np.zeros((1,lat_size,lon_size))
data_arr[0]=np.flip(Q10,0)
# Write the data.  This writes the whole 3D netCDF variable all at once.
Q[:,:,:] = data_arr  # Appends data along unlimited dimension
print("-- Wrote data, temp.shape is now ", Q.shape)
# read data back from variable (by slicing it), print min and max
print("-- Min/Max values:", Q[:,:,:].min(), Q[:,:,:].max())

ncfile.close(); print('Dataset is closed!')

