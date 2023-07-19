import numpy as np
import xarray as xr

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.util as cutil

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import cmocean
import dask

ds=xr.open_dataset('/lus/work/NAT/gda2307/aalbert/DEV/DCM_4.2rk3/DCMTOOLS/NEMOREF/NEMO4/cfgs/WED025_TEST/EXP00/WED025_5d_20000101_20000130_grid_T.nc')
mask=xr.open_dataset('/lus/work/NAT/gda2307/aalbert/DEV/DCM_4.2rk3/DCMTOOLS/NEMOREF/NEMO4/cfgs/WED025_TEST/EXP00/mesh_mask_merg.nc')

tt=0
data=ds.tos[tt]
lon=mask.glamt[0]
lat=mask.gphit[0]
tmask=mask.tmaskutil
datam=np.ma.array(data,mask=1-tmask)

projection=ccrs.SouthPolarStereo()
#projection=ccrs.Orthographic(central_latitude=-70.0, central_longitude=-40.0)
#projection=ccrs.PlateCarree()
fig, ax = plt.subplots(subplot_kw=dict(projection=projection), figsize=(10,9))
#ax.set_global()
ax.set_extent([-90, 10, -90, -60], crs=ccrs.PlateCarree())

#-- add coastal outlines
#ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.5)
#ax.background_img(name='BM', resolution='low')

gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='k', zorder=3)
#gl.xlabel_style = {'size':10}
#gl.ylabel_style = {'size':10}
gl.top_labels   = True
gl.right_labels = True
gl.bottom_labels   = False
gl.left_labels = True
#ax.set_title('WED025 surface temperature at t='+str(tt))

cnf1  = ax.pcolormesh(lon, lat, datam,
                          cmap=cmocean.cm.thermal,
                          vmin=-2,
                          vmax=5,
#                          shading='flat',
                          transform=ccrs.PlateCarree())
fig.colorbar(cnf1,shrink=0.8)

plt.savefig('plot_tos_WED025.png')
