import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy
from pylab import figure, cm
from matplotlib.colors import LogNorm
from osgeo import gdal
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
from os.path import isfile, join
from os import listdir
import matplotlib.pyplot as plt
import matplotlib as mpl
import netCDF4 as nc
from scipy import sparse
from matplotlib.gridspec import GridSpec
import os
from matplotlib.ticker import MultipleLocator,FixedLocator, FixedFormatter
import pandas as pd

## Import the coordinates and station name for each grid point
lon=os.environ.get('lon')
lat=os.environ.get('lat')
station=os.environ.get('station')


## Define layer name, model name list, maximum number of timesteps allowed (a), and filename.
layer_name='dis'
models=[ 'ICTP-RegCM4-7_NCC-NorESM1-M_r1', 'ICTP-RegCM4-7_MPI-M-MPI-ESM-MR_r1', 'ICTP-RegCM4-7_MOHC-HadGEM2-ES_r1',   'GERICS-REMO2015_NCC-NorESM1-M_r1',  'GERICS-REMO2015_MPI-M-MPI-ESM-LR_r1', 'GERICS-REMO2015_MOHC-HadGEM2-ES_r1' ]
a=10800
filename=join('extracted_{'+str(lon)+'}_{'+str(lat)+'}.nc')

## Initialize array and import data from models 
data=np.zeros((np.size(models),a))

for i in range(np.size(models)):
 pathresult=join('/home/netapp-clima/scratch/lvargas/SAM/'+models[i]+'/points_arg/')       
 nc_results = [f for f in listdir(pathresult) if isfile(join(pathresult, f)) if f.startswith("") and f.endswith(join(filename))]
 ds_results = [gdal.Open("NETCDF:{0}:{1}".format(pathresult + f, layer_name)) for f in nc_results]
 results = [f.ReadAsArray(0, 0, f.RasterXSize, f.RasterYSize) for f in ds_results]
 results = np.asarray(results)
 b=results.flatten()
 data[i,:]=b[:a]


### This part needs adjusting according to the format of the station data

## Import station data as pandas dataframe
stationname=station 
df=pd.read_excel(join('/path/to/station/data/from/excel/file/'+stationname))

## Converts data read as string to datetime format and is then masked to include only years of interest.
df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')
start_date='01/01/1976'
end_date='31/12/2005'
mask = (df['Fecha'] >= start_date) & (df['Fecha'] <= end_date)
df = df.loc[mask]
data_obs=df['Caudal Medio Diario [m3/seg]']




### Plotting the figure
fig,ax = plt.subplots(figsize=(10,5))

## List of different blue shades for different models
blues=['deepskyblue','lightsteelblue','royalblue','lightskyblue','skyblue','teal','cyan','darkturquoise','dodgerblue'] 

for i in range(np.size(models)):
 data_sorted = np.sort(data[i])  ## Sort in ascending order data points
 samples = len(data_sorted)   ## Sees length of data
 exceedance = [(1-(x/samples))*100 for x in range(1, samples + 1)]  ## Calculates frequency at which each value is exceed
 plt.semilogy(exceedance,data_sorted,blues[i])  ## Plots results in a semilog graph

data_sorted = np.sort(data_obs)
samples = len(data_sorted)
exceedance = [(1-(x/samples))*100 for x in range(1, samples + 1)]
plt.semilogy(exceedance,data_sorted,'r--',linewidth=2)

data_sorted = np.sort(data_glofas)
samples = len(data_sorted)
exceedance = [(1-(x/samples))*100 for x in range(1, samples + 1)]
plt.semilogy(exceedance,data_sorted,'m--',linewidth=2)


plt.legend(fontsize="12")
plt.xticks(np.linspace(0, 100,11))
plt.ylabel('Discharge [m3/s]',fontsize=15)
plt.xlim(right=105,left=-5)
plt.xlabel('Exceedence [%]',fontsize=15)
plt.grid(True, which="both")
plt.savefig(join('./flowdur/'+filename+'.png'),bbox_inches='tight',dpi=300)
plt.show()
