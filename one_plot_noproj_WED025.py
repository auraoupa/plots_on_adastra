import numpy as np
import numpy.ma as ma

import xarray as xr

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.util as cutil
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker

import cmocean
import dask

def one_map_noproj(fig, sub, filein, filemask, var, lev, ttime, cmap, vmin, vmax, title):

    ds=xr.open_dataset(filein)

    data=ds[var][ttime,lev]

    if (var == 'votemper') or (var == 'thetao'):
        unit = 'deg C'
        mask = 'tmask'
    if (var == 'vosaline'):
        unit = 'PSU'
    elif (var == 'vozocrtx'):
        unit = 'ms-1'

    dsmask=xr.open_dataset(filemask)
    tmask=dsmask[mask][0,lev]
    datam=np.ma.array(data,mask=1-tmask)

    ax = fig.add_subplot(sub)

    pcolor=ax.pcolormesh(datam,cmap=cmap,vmin=vmin,vmax=vmax)
    fig.subplots_adjust(right=0.8)

    cbar = plt.colorbar(pcolor,orientation='horizontal',shrink=0.75, pad=0.1,label=unit)
    ax.set_title(title,size=17,y=1.08)
    

filein = '/lus/work/NAT/gda2307/aalbert/DEV/DCM_4.2rk3/DCMTOOLS/NEMOREF/NEMO4/cfgs/WED025_TEST/EXP00/WED025_5d_20000101_20000301_grid_T.nc'
filemask='/lus/work/NAT/gda2307/aalbert/DEV/DCM_4.2rk3/DCMTOOLS/NEMOREF/NEMO4_oldbr63/cfgs/WED025_TEST/EXP00/mesh_mask_merg.nc'
var = 'thetao'
unit = 'degC'
lev = 0
cmap = cmap=cmocean.cm.thermal
vmin = -2
vmax = 5
ttime = 8

title = 'WED025 Ref Temperature at lev = '+str(lev)+' and time = '+str(ttime)
plotname ='map_temp_WED025-TEST_lev'+str(lev)+'_time'+str(ttime)+'.png'
fig = plt.figure(figsize=(20,20))
sub = 111
one_map_noproj(fig, sub, filein, filemask, var, lev, ttime, cmap, vmin, vmax, title);
plt.savefig(plotname)
