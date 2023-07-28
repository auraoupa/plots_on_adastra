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

dir1='/lus/work/NAT/gda2307/aalbert/DEV/DCM_4.2rk3/DCMTOOLS/NEMOREF/NEMO4_oldbr63/cfgs/WED025_TEST/EXP00/'
dir2='/lus/work/NAT/gda2307/aalbert/DEV/DCM_4.2rk3/DCMTOOLS/NEMOREF/NEMO4_oldbr63/cfgs/WED025_RK3/EXP00/'
filemask='/lus/work/NAT/gda2307/aalbert/DEV/DCM_4.2rk3/DCMTOOLS/NEMOREF/NEMO4_oldbr63/cfgs/WED025_TEST/EXP00/mesh_mask_merg.nc'

dsmask=xr.open_dataset(filemask)
tmask=dsmask['tmask'][0,0]

fileT1=dir1+'WED025_5d_20000101_20000130_grid_T.nc'
fileT2=dir2+'WED025_5d_20000101_20000130_grid_T.nc'

sst1=get_data2D(fileT1,'thetao',5,0)
sst2=get_data2D(fileT2,'thetao',5,0)

sss1=get_data2D(fileT1,'so',5,0)
sss2=get_data2D(fileT2,'so',5,0)

ssh1=get_data2D(fileT1,'zos',5,-1)
ssh2=get_data2D(fileT2,'zos',5,-1)

fileI1=dir1+'WED025_5d_20000101_20000130_icemod.nc'
fileI2=dir2+'WED025_5d_20000101_20000130_icemod.nc'

sit1=get_data2D(fileI1,'sithic',5,-1)
sit2=get_data2D(fileI2,'sithic',5,-1)

sic1=get_data2D(fileI1,'siconc',5,-1)
sic2=get_data2D(fileI1,'siconc',5,-1)

fig = plt.figure(figsize=(30,50))
one_map_noproj(fig, 5,3,1,  sst1,   'degC', tmask, cmocean.cm.thermal, -2,  5, 'WED025 Ref Surface Temperature after 30d');
one_map_noproj(fig, 5,3,2,  sst2,   'degC', tmask, cmocean.cm.thermal, -2,  5, 'WED025 RK3 Surface Temperature after 30d');
one_map_noproj(fig, 5,3,3,sst2-sst1,'degC', tmask, cmocean.cm.balance, -1,  1, 'WED025 RK3-Ref Surface Temperature after 30d');
one_map_noproj(fig, 5,3,4,  sss1,    'PSI' , tmask, cmocean.cm.haline , 30, 35, 'WED025 Ref Surface Salinity after 30d');
one_map_noproj(fig, 5,3,5,  sss2,    'PSI' , tmask, cmocean.cm.haline , 30, 35, 'WED025 RK3 Surface Salinity after 30d');
one_map_noproj(fig, 5,3,6,sss2-sss1, 'PSI' , tmask, cmocean.cm.balance , -1, 1, 'WED025 RK3-Ref Surface Salinity after 30d');
one_map_noproj(fig, 5,3,7,  ssh1,    'm'   , tmask, 'tab20c'          , -1,-0.6, 'WED025 Ref Surface Height after 30d');
one_map_noproj(fig, 5,3,8,  ssh2,    'm'   , tmask, 'tab20c'          , -1,-0.6, 'WED025 RK3 Surface Height after 30d');
one_map_noproj(fig, 5,3,9,ssh2-ssh1, 'm'   , tmask, cmocean.cm.balance, -0.1,0.1, 'WED025 RK3-Ref Surface Height after 30d');
one_map_noproj(fig, 5,3,10, sit1,    'm'   , tmask, cmocean.cm.ice    ,  0, 10, 'WED025 Ref Ice Thickness after 30d');
one_map_noproj(fig, 5,3,11, sit2,    'm'   , tmask, cmocean.cm.ice    ,  0, 10, 'WED025 RK3 Ice Thickness after 30d');
one_map_noproj(fig, 5,3,12,sit2-sit1,'m'   , tmask, cmocean.cm.balance,  -1, 1, 'WED025 RK3-Ref Ice Thickness after 30d');
one_map_noproj(fig, 5,3,13, sic1,    ''    , tmask, cmocean.cm.ice    ,  0,  1, 'WED025 Ref Ice Concentration after 30d');
one_map_noproj(fig, 5,3,14, sic2,    ''    , tmask, cmocean.cm.ice    ,  0,  1, 'WED025 RK3 Ice Concentration after 30d');
one_map_noproj(fig, 5,3,15,sic2-sit1,''    , tmask, cmocean.cm.balance,  -1,  1, 'WED025 RK3-Ref Ice Concentration after 30d');

plotname ='plots/all_surf_maps_WED025-TEST-RK3_oldbr63-diff_30d.png'
plt.savefig(plotname)

fig = plt.figure(figsize=(20,50))
one_map_noproj(fig, 5,2,1,  sst1,   'degC', tmask, cmocean.cm.thermal, -2,  5, 'WED025 Ref Surface Temperature after 30d');
one_map_noproj(fig, 5,2,2,  sst2,   'degC', tmask, cmocean.cm.thermal, -2,  5, 'WED025 RK3 Surface Temperature after 30d');
one_map_noproj(fig, 5,2,3,  sss1,    'PSI' , tmask, cmocean.cm.haline , 30, 35, 'WED025 Ref Surface Salinity after 30d');
one_map_noproj(fig, 5,2,4,  sss2,    'PSI' , tmask, cmocean.cm.haline , 30, 35, 'WED025 RK3 Surface Salinity after 30d');
one_map_noproj(fig, 5,2,5,  ssh1,    'm'   , tmask, 'tab20c'          , -1,-0.6, 'WED025 Ref Surface Height after 30d');
one_map_noproj(fig, 5,2,6,  ssh2,    'm'   , tmask, 'tab20c'          , -1,-0.6, 'WED025 RK3 Surface Height after 30d');
one_map_noproj(fig, 5,2,7, sit1,    'm'   , tmask, cmocean.cm.ice    ,  0, 10, 'WED025 Ref Ice Thickness after 30d');
one_map_noproj(fig, 5,2,8, sit2,    'm'   , tmask, cmocean.cm.ice    ,  0, 10, 'WED025 RK3 Ice Thickness after 30d');
one_map_noproj(fig, 5,2,9, sic1,    ''    , tmask, cmocean.cm.ice    ,  0,  1, 'WED025 Ref Ice Concentration after 30d');
one_map_noproj(fig, 5,2,10, sic2,    ''    , tmask, cmocean.cm.ice    ,  0,  1, 'WED025 RK3 Ice Concentration after 30d');

plotname ='plots/all_surf_maps_WED025-TEST-RK3_oldbr63_30d.png'
plt.savefig(plotname)
