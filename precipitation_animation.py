import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
import pygrib
from datetime import datetime, timedelta

# Set up the figure with high resolution
plt.style.use('seaborn-v0_8-paper')
fig = plt.figure(figsize=(15, 10), dpi=300)
ax = plt.axes(projection=ccrs.PlateCarree())

# Create custom colormap with more color gradients
precip_cmap = LinearSegmentedColormap.from_list('precip', 
    ['#FFFFFF', '#E6F3FF', '#A6F28F', '#3DBC3D', '#238E23', '#465ACE', '#7F00FF'], N=256)

# Read GRIB file
grib_file = '/Users/samirafarzana/Downloads/file/42f58b70626d038b6d053a844f1cd1ae.grib'

# Store hourly precipitation data
hourly_data = []

try:
    grbs = pygrib.open(grib_file)
    
    # Process each message in the GRIB file
    for grb in grbs:
        if 'precip' in grb.name.lower() or 'tp' in grb.shortName.lower():
            data, lats, lons = grb.data()
            # Convert from meters to millimeters for better visualization
            data = data * 1000  # convert to mm
            hourly_data.append({
                'date': grb.validDate,
                'data': data,
                'lats': lats,
                'lons': lons
            })
    
    grbs.close()
    
    # Sort data by date
    hourly_data.sort(key=lambda x: x['date'])
    
    print(f"\nAnalyzing precipitation data from {hourly_data[0]['date']} to {hourly_data[-1]['date']}")
    print(f"Total number of time steps: {len(hourly_data)}")
    
except Exception as e:
    print(f"Error processing GRIB file: {str(e)}")
    raise

# Set up the base map
ax.coastlines(resolution='10m', linewidth=0.8)
ax.add_feature(cfeature.BORDERS, linewidth=0.8, color='0.3')
ax.add_feature(cfeature.LAND, alpha=0.1)
ax.add_feature(cfeature.OCEAN, alpha=0.1)
gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
gl.top_labels = False
gl.right_labels = False

# Initialize the plot with the first frame
mesh = ax.pcolormesh(hourly_data[0]['lons'], hourly_data[0]['lats'], 
                    hourly_data[0]['data'], 
                    transform=ccrs.PlateCarree(),
                    cmap=precip_cmap, shading='auto')

# Add colorbar
cbar = plt.colorbar(mesh, orientation='horizontal', pad=0.05, 
                   label='Precipitation (mm)', fraction=0.046)
cbar.ax.tick_params(labelsize=10)

# Title placeholder
title = ax.text(0.5, 1.05, '', fontsize=14, ha='center', transform=ax.transAxes)

def update(frame):
    """Update function for animation"""
    # Clear previous precipitation data
    mesh.set_array(hourly_data[frame]['data'].ravel())
    
    # Update title with current date
    current_date = hourly_data[frame]['date']
    title.set_text(f'Total Precipitation - {current_date.strftime("%B %d, %Y %H:%M")}')
    
    # Update colorbar limits based on current data
    vmax = max(d['data'].max() for d in hourly_data)
    if vmax == 0:
        vmax = 1  # Prevent all-zero colormap
    mesh.set_clim(vmin=0, vmax=vmax)
    
    return mesh, title

# Create animation
anim = FuncAnimation(fig, update, frames=len(hourly_data), 
                    interval=500,  # 0.5 seconds between frames
                    blit=True, repeat=True)

# Save animation with high quality
print("\nGenerating animation...")
anim.save('precipitation_animation.gif', 
         writer='pillow', fps=2,  # 2 frames per second
         dpi=300)
print("Animation saved as 'precipitation_animation.gif'")

plt.close()
