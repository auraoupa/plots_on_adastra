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

def one_map_noproj(fig, nx, ny, pos, data, unit, mask, cmap, vmin, vmax, title):

    datam=np.ma.array(data,mask=1-mask)

    ax = fig.add_subplot(nx,ny,pos)

    pcolor=ax.pcolormesh(datam,cmap=cmap,vmin=vmin,vmax=vmax)
    fig.subplots_adjust(right=0.8)

    cbar = plt.colorbar(pcolor,orientation='horizontal',shrink=0.75, pad=0.1,label=unit)
    ax.set_title(title,size=17,y=1.08)

def get_data2D(filei,var,ttime,lev):
    ds=xr.open_dataset(filei)
    if (lev == -1):
        data=ds[var][ttime]
    else:
        data=ds[var][ttime,lev]

    return data

#filein = '/lus/work/NAT/gda2307/aalbert/eORCA36.L121/eORCA36.L121-I/vosaline_MP026-eORCA36_MP026.nc'
filein = '/lus/work/NAT/gda2307/aalbert/eORCA36.L121/eORCA36.L121-I/votemper_MP026-eORCA36_MP026.nc'
filemask = '/lus/work/NAT/gda2307/aalbert/eORCA36.L121/eORCA36.L121-I/eORCA36.L121-MAA2023_mesh_mask_v4.nc'

#plotname ='plots/map_salt_init_eORCA36.png'
plotname ='plots/map_temp_init_eORCA36.png'

#sss=get_data2D(filein,'vosaline',0,0)
sss=get_data2D(filein,'votemper',0,0)
dsmask=xr.open_dataset(filemask)
tmask=dsmask['tmask'][0,0]

fig = plt.figure(figsize=(15,15))
#one_map_noproj(fig, 1,1,1,  sss,   'PSI', tmask, cmocean.cm.haline, 30, 35, 'init salinity eORCA36');
one_map_noproj(fig, 1,1,1,  sss,   'degC', tmask, cmocean.cm.thermal, -5, 30, 'init temperature eORCA36');

plt.savefig(plotname)
