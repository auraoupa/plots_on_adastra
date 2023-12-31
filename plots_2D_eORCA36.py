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

dep=0



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
        data=ds[var][ttime].squeeze()
    else:
        data=ds[var][ttime,lev].squeeze()
    return data

filein = '/lus/work/NAT/gda2307/aalbert/eORCA36.L121/eORCA36.L121-I/votemper_MP026-eORCA36_MP026.nc'
filemask = '/lus/work/NAT/gda2307/aalbert/eORCA36.L121/eORCA36.L121-I/eORCA36.L121-MAA2023_mesh_mask_v4.nc'

dsmask=xr.open_dataset(filemask)
navlev=dsmask['nav_lev']

lev=np.where(np.abs(navlev-dep)==np.min(np.abs(navlev-dep)))[0]

tmask=dsmask['tmask'][0,lev]
sst=get_data2D(filein,'votemper',0,lev)

plotname ='plots/map_temp_init_eORCA36'+str(dep)+'m.png'
fig = plt.figure(figsize=(30,30))
one_map_noproj(fig, 1,1,1,  sst,   'degC', tmask, cmocean.cm.thermal, -5, 30, 'init temperature eORCA36 '+str(dep)+'m');
plt.savefig(plotname)

filein = '/lus/work/NAT/gda2307/aalbert/eORCA36.L121/eORCA36.L121-I/vosaline_MP026-eORCA36_MP026.nc'
plotname ='plots/map_salt_init_eORCA36'+str(dep)+'m.png'
sss=get_data2D(filein,'vosaline',0,lev)

fig = plt.figure(figsize=(30,30))
one_map_noproj(fig, 1,1,1,  sss,   'PSI', tmask, cmocean.cm.haline, 30, 35, 'init salinity eORCA36 '+str(dep)+'m')
plt.savefig(plotname)

