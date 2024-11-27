#import pynhd
import pandas
import geopandas
import requests
import matplotlib.pyplot as plt
import contextily
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import geopandas as gpd
from pysheds.grid import Grid
import mplleaflet
from os.path import isfile, join
from os import listdir
import os
from osgeo import gdal
from netCDF4 import Dataset

## Import model and month data 
month=os.environ.get('month')
model=os.environ.get('model')


## Define size of grid being looked at 
lon_size = 1017 ;
lat_size = 1183 ;
region_size=lon_size*lat_size

## Open temperature data
pathresult='path/to/temperature/data/of/model/'
nc_results = [f for f in listdir(pathresult) if isfile(join(pathresult, f)) if f.startswith("") and f.endswith(join("mon"+month+".nc"))]
ds_map=[gdal.Open("NETCDF:{0}:{1}".format(pathresult + f,"tas")) for f in nc_results]
tas = [f.ReadAsArray(0, 0, f.RasterXSize, f.RasterYSize) for f in ds_map]
tas=np.flip(tas,0)
tas=tas[0]
tas[tas>1e10]=np.nan

## Open mean discharge data to separate where there is no discharge (aka no river network) and where there is 
pathresult='path/to/discharge/data/of/model/'
nc_results = [f for f in listdir(pathresult) if isfile(join(pathresult, f)) if f.startswith("") and f.endswith("mean_his.nc")]
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
latitude=np.flip(latitude,0)
ds = [gdal.Open("NETCDF:{0}:{1}".format(pathresult + f,"dis")) for f in nc_results]#aqui tem problema pra abrir td
mean = [f.ReadAsArray(0, 0, f.RasterXSize, f.RasterYSize) for f in ds]
mean=np.asarray(mean)
mean=np.flip(mean,0)
mean=mean[0]
mean[mean>1e8]=np.nan
mean[mean<0.5]=np.nan
lon2d, lat2d = np.meshgrid(longitude, latitude)

## Flattens arrays for loop
lonf=lon2d.flatten()
latf=lat2d.flatten()
meanf=mean.flatten()
tasf=tas.flatten()
b=np.zeros((np.shape(latf)))
for i in range(region_size):
 ## Only looks inside river network
 if ~np.isnan(meanf[i]):
  grid = Grid.from_raster(join('/home/netapp-clima/scratch/lvargas/SAM/fdm.tiff'))
  fdir = grid.read_raster(join('/home/netapp-clima/scratch/lvargas/SAM/fdm.tiff'))
  dirmap = (1, 2, 3, 4, 5, 6, 7, 8)
  acc = grid.accumulation(fdir, dirmap=dirmap)
  x_snap, y_snap = lonf[i],latf[i] 
  catch=grid.catchment(x=x_snap, y=y_snap, fdir=fdir, dirmap=dirmap,xytype='coordinate')
  a=np.asarray(catch)*tas
  c=a
  c[np.isnan(c)]=0
  a[np.equal(a,0)]=np.nan
  if np.nanmean(a)>273.15:
    b[i]=1
  else:
    b[i]=-1
  del grid

b=b.reshape((np.shape(tas)))
result=b

pathresult='output/path/'

## Writes a new netcdf file called frost01.nc for example to set which points are in a frost season that month
try: ncfile.close()  # just to be safe, make sure dataset is not already open.
except: pass
ncfile = Dataset(join(pathresult+'frost'+month+'.nc') ,mode='w',format='NETCDF4_CLASSIC')
print(ncfile)
lat_dim = ncfile.createDimension('lat', lat_size)     # latitude axis
lon_dim = ncfile.createDimension('lon', lon_size)    # longitude axis
time_dim = ncfile.createDimension('time', None) # unlimited axis (can be appended to).
ncfile.title=join('postproc')
ncfile.subtitle=model
lat.units = 'degrees_north'
lat.long_name = 'latitude'
lon = ncfile.createVariable('lon', np.float32, ('lon',))
lon.units = 'degrees_east'
lon.long_name = 'longitude'
time = ncfile.createVariable('time', np.float64, ('time',))
time.units = 'seconds since 1976-01-01 00:00:00 UTC'
time.long_name = 'time'
Q = ncfile.createVariable('por',np.float64,('time','lat','lon')) # note: unlimited dimension is leftmost
Q.standard_name = 'Peak_discharge' # this is a CF standard name
lat[:]=latitude
lon[:]=longitude

nlats = len(lat_dim); nlons = len(lon_dim);# ntimes = 3

# Write latitudes, longitudes.
# Note: the ":" is necessary in these "write" statements
# create a 3D array of random numbers
data_arr=np.zeros((1,lat_size,lon_size))
data_arr[0]=result

ncfile.close(); print('Dataset is closed!')
