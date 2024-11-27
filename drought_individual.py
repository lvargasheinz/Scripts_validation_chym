#make sure to run "export GDAL_MAX_BAND_COUNT=259200" on bash if needs more bands
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
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy
from pylab import figure, cm
from matplotlib.colors import LogNorm
from osgeo import gdal
#from mpl_toolkits.axes_grid1 import make_axes_locatable
import openturns
import openturns as ot
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
from scipy.stats import gumbel_r , gumbel_l



## Import the coordinates and station name for each grid point
lon=os.environ.get('lon')
lat=os.environ.get('lat')
station=os.environ.get('station')


## Define layer name, model name list, maximum number of timesteps allowed (a), and filename.
layer_name='dis'
models=[ 'ICTP-RegCM4-7_NCC-NorESM1-M_r1', 'ICTP-RegCM4-7_MPI-M-MPI-ESM-MR_r1', 'ICTP-RegCM4-7_MOHC-HadGEM2-ES_r1',   'GERICS-REMO2015_NCC-NorESM1-M_r1',  'GERICS-REMO2015_MPI-M-MPI-ESM-LR_r1', 'GERICS-REMO2015_MOHC-HadGEM2-ES_r1' ]
a=10800
filename=join('extracted_{'+str(lon)+'}_{'+str(lat)+'}.nc')

## Initialize array and import data from models and define array for all return periods which will be calculated (here 2 to 100)
TR=np.linspace(2,100,100)
data=np.zeros((np.size(models),a))
QRP=np.zeros((np.size(models),np.size(TR)))
valor=1-1/TR


for i in range(np.size(models)):
 pathresult=join('/home/netapp-clima/scratch/lvargas/SAM/'+models[i]+'/points_arg_min/')       
 nc_results = [f for f in listdir(pathresult) if isfile(join(pathresult, f)) if f.startswith("") and f.endswith(join(filename))]
 ds_results = [gdal.Open("NETCDF:{0}:{1}".format(pathresult + f, layer_name)) for f in nc_results]#aqui tem problema pra abrir td
 results = [f.ReadAsArray(0, 0, f.RasterXSize, f.RasterYSize) for f in ds_results]
 results = np.asarray(results)
 y=results.flatten()
 y[y<0]=np.nan
 y=y[~(np.isnan(y))]
## For nulled/non-discharge points, nothing wiil be calculated. This should not happen as we have only selected grid points with large drainage areas, but it is a precaution,
 if np.size(y)==0 or np.size(y)==1:
      a=a+1
      QRP[i,:]=QRP[i,:].fill(np.nan)#np.nan
 else:
  y_list = [[element] for element in y]
  sample = ot.Sample(y_list)
  distWeibullMax = ot.WeibullMaxFactory().buildAsWeibullMax(sample)
  for k in range(np.size(TR)):
   f=distWeibullMax.computeQuantile(1/TR[k])
   QRP[i,k]=np.asarray(f)



## THIS IGNORES FROZEN SEASON FOR STATION DATA	
## Import station data as pandas dataframe
stationname=station
df=pd.read_excel(join('/path/to/station/data/from/excel/file/'+stationname))

## Converts data read as string to datetime format and is then masked to include only years of interest.
df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')
start_date='01/01/1976'
end_date='31/12/2005'
mask = (df['Fecha'] >= start_date) & (df['Fecha'] <= end_date)
df = df.loc[mask]

## Yearly maximums of the station point are calculated and used to get the discharge for the different return periods
Qmin_obs=df.groupby(lambda x: df['Fecha'][x].year)["Caudal Medio Diario [m3/seg]"].min()
Qmin_obs=np.asarray(Qmin_obs)
y=Qmin_obs.flatten()
y[y<0]=np.nan
y=y[~(np.isnan(y))]
QRP_obs=np.zeros((np.shape(TR)))
y_list = [[element] for element in y]
sample = ot.Sample(y_list)
distWeibullMax = ot.WeibullMaxFactory().buildAsWeibullMax(sample)
for k in range(np.size(TR)):
   f=distWeibullMax.computeQuantile(1/TR[k])
   QRP_obs[k]=np.asarray(f)






## The 5th, 50th and 95th percentiles for the ensemble of models are chosen for easier plotting
Q5=np.percentile(QRP,5,0)
Q50=np.percentile(QRP,50,0)
Q95=np.percentile(QRP,95,0)


fig,ax = plt.subplots(figsize=(10,5))

plt.plot(TR,Q5,'b',label="5th Percentile")
plt.plot(TR,Q50,'r',label="50th Percentile")
plt.plot(TR,Q95,'g',label="95th Percentile")
plt.plot(TR,QRP_obs,'k.',label='Station Data')


plt.legend(fontsize="12")
plt.xticks(np.linspace(0, 100,11))
plt.xlim(right=105,left=-5)
plt.ylabel('Discharge [m3/s]',fontsize=15)
plt.xlabel('Return Period [Years]',fontsize=15)
plt.grid(True, which="both")
plt.grid(True, which="both")
plt.savefig(join('./drought/'+filename+'.png'),bbox_inches='tight',dpi=300)
plt.show()

