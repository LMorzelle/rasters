
from pathlib import Path
import numpy as np
import rioxarray
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import Normalize

def create_comparison_figure(dem_path: Path, swiss_dem_path: Path, vmin=5, vmax=5, crop_size=2000, xtickdelta=1000, ytickdelta=1000):
    # Load the DEM file


    dem = rioxarray.open_rasterio(dem_path, masked=True)  # Open the DEM file using rioxarray
    swiss_dem = rioxarray.open_rasterio(swiss_dem_path, masked=True)  # Open the DEM file using rioxarray
    # Reproject dem to match swiss_dem
    dem_reprojected = dem.rio.reproject_match(swiss_dem)

    dem_reprojected = dem_reprojected.assign_coords({
        "x": swiss_dem.x,
        "y": swiss_dem.y,
    })
        # Calculate the difference between the reprojected DEM and swiss_dem
    dem_diff = dem_reprojected - swiss_dem
    dem_diff = dem_diff.rio.slice_xy(dem.x.min().item(), dem.y.min().item(), dem.x.max().item(), dem.y.max().item())
    dem_diff_subset = dem_diff.isel(x=slice(0, None, 10), y=slice(0, None, 10))
    # Find the center coordinates of dem_diff_subset
    center_x = dem_diff_subset.x.mean().item()
    center_y = dem_diff_subset.y.mean().item()

    # Select a subset of the dem_reprojected data array by slicing the x and y coordinates from 0 to 30000 with a step of 10

    fig, ax = plt.subplots(figsize=(10, 7))
    cax = dem_diff_subset.plot(cmap='terrain', ax=ax, add_colorbar=False, vmin=vmin, vmax=vmax)
    ax.set_xlim(center_x - crop_size, center_x + crop_size)
    ax.set_ylim(center_y - crop_size, center_y + crop_size)


    ax.set_title('')

    ax.set_aspect('equal')
    ax.ticklabel_format(style='plain', axis='y')
    ax.set_yticklabels(ax.get_yticklabels(), rotation=90, va='center')
    ax.ticklabel_format(style='plain', axis='x')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center')
    ax.xaxis.set_major_locator(plt.MultipleLocator(xtickdelta))
    ax.yaxis.set_major_locator(plt.MultipleLocator(ytickdelta))

    divider = make_axes_locatable(plt.gca())
    axBar = divider.append_axes("right", '5%', pad='15%')
    axHist = divider.append_axes("right", '30%', pad='1%')

    # Remove y and x ticks
    axBar.yaxis.set_ticks([])
    axBar.xaxis.set_ticks([])
    axBar.yaxis.set_label_position('left')
    axBar.set_ylabel('difference (m)')

    axHist.yaxis.set_ticks([])
    axHist.xaxis.set_ticks([])

    cbar = plt.colorbar(cax, cax=axBar)

    axBar.yaxis.set_ticks_position('left')

    # get hist data
    bin_width = 0.05  # 10 cm in meters
    bins = np.arange(vmin, vmax + bin_width, bin_width)
    N, bins, patches = axHist.hist(np.ndarray.flatten(dem_diff.values), bins=bins, orientation='horizontal')

    norm = Normalize(bins.min(), bins.max())
    # set a color for every bar (patch) according 
    # to bin value from normalized min-max interval
    for bin, patch in zip(bins, patches):
        color = cm.terrain(norm(bin))
        patch.set_facecolor(color)

    axHist.set_ylim(vmin, vmax)

    plt.show()