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


filein = '/lus/work/NAT/gda2307/aalbert/eORCA36.L121/eORCA36.L121-I/votemper_MP026-eORCA36_MP026.nc'
filemask = '/lus/work/NAT/gda2307/aalbert/eORCA36.L121/eORCA36.L121-I/eORCA36.L121-MAA2023_mesh_mask_v4.nc'

plotname ='plots/map_temp_init_eORCA36_sections.png'
ds=xr.open_dataset(filein)
data=ds['votemper'][0,0]
dsmask=xr.open_dataset(filemask)
tmask=dsmask['tmask'][0,0]

fig = plt.figure(figsize=(15,15))
datam=np.ma.array(data,mask=1-tmask)

ax = fig.add_subplot(111)

pcolor=ax.pcolormesh(datam,cmap=cmocean.cm.thermal,vmin=-5,vmax=30)
ax.plot([4062, 4135], [9181, 9181],color='mediumseagreen',linewidth=3, label='Bering')
ax.plot([9600,9945], [10145,10145],color='lightseagreen',linewidth=3, label='Fram')
ax.plot([8331,8812], [9955,9955],color='silver',linewidth=3, label='Baffin')
ax.plot([9232,9466], [9272,9146],color='teal',linewidth=3, label='Denmark')
ax.plot([9741,10077], [9091,8737],color='yellow',linewidth=3, label='Iceland-Scotland')
ax.plot([7435,7434], [7003,7106],color='blue',linewidth=3, label='Cuba-Florida')
ax.plot([7446,7498], [7154,7154],color='navy',linewidth=3, label='Florida-Bahamas')
ax.plot([7914,8004], [3790,2954],color='orange',linewidth=3, label='Drake')
ax.plot([2725,2724], [4696,2732],color='gold',linewidth=3, label='Australia-Antartica')
ax.plot([1524,1524], [5854,5359],color='magenta',linewidth=3, label='Indonesian throughflow')
ax.plot([11763,11934], [5563,5563],color='crimson',linewidth=3, label='Mozambique')
ax.plot([11050,11050], [2576,4832],color='goldenrod',linewidth=3, label='South Africa')
ax.plot([12823,12823], [2794,4108],color='whitesmoke',linewidth=3, label='Kerguelen')
ax.plot([3504,3504], [2386,4300],color='lightgrey',linewidth=3, label='Campbell')
ax.plot([11406,12959], [5258,5258],color='black',linewidth=3)
ax.plot([0,1578], [5258,5258],color='black',linewidth=3, label='Africa-Australia')
ax.plot([2835,7797], [5258,5258],color='darkblue',linewidth=3, label='Australia-America')
ax.plot([8634,10861], [5258,5258],color='darkgreen',linewidth=3, label='America-Africa')
fig.legend(loc='outside right upper')


fig.subplots_adjust(right=0.8)

cbar = plt.colorbar(pcolor,orientation='horizontal',shrink=0.75, pad=0.1,label='degC')
ax.set_title('init temperature eORCA36',size=17,y=1.08)
plt.savefig(plotname)
