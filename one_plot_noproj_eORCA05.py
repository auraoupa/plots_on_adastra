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

def one_map_noproj(fig, sub, filein, var, lev, ttime, cmap, vmin, vmax, title):

    ds=xr.open_dataset(filein)

    data=ds[var][ttime,lev]

    if (var == 'votemper'):
        unit = 'deg C'
    if (var == 'vosaline'):
        unit = 'PSU'
    elif (var == 'vozocrtx'):
        unit = 'ms-1'

    ax = fig.add_subplot(sub)

    pcolor=ax.pcolormesh(data,cmap=cmap,vmin=vmin,vmax=vmax)
    fig.subplots_adjust(right=0.8)

    cbar = plt.colorbar(pcolor,orientation='horizontal',shrink=0.75, pad=0.1,label=unit)
    ax.set_title(title,size=17,y=1.08)
    

filein = '/lus/work/NAT/gda2307/aalbert/eORCA05.L121/eORCA05.L121-AGDA004-S/1h/2012/eORCA05.L121-AGDA004_y2012m01d01.1h_gridT.nc'
filemask = '/lus/work/NAT/gda2307/aalbert/eORCA05.L121/eORCA05.L121-I/eORCA05.L121_mesh_mask_4.2.nc'
var = 'votemper'
lev = 0
proj = ccrs.Orthographic(central_latitude=30.0, central_longitude=-30.0)
reg = 'global'
cmap = cmap=cmocean.cm.thermal
vmin = -2
vmax = 30
ttime=23

title = 'Surface temperature at lev = '+str(lev)+' and time = '+str(ttime)
plotname ='map_temp_eORCA05.L121-AGDA004_lev'+str(lev)+'_time'+str(ttime)+'.png'
fig = plt.figure(figsize=(20,20))
sub = 111
one_map_noproj(fig, sub, filein, var, lev, ttime, cmap, vmin, vmax, title);
plt.savefig(plotname)
