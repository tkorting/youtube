# Subscribe to my channel, share and like my videos at
# http://youtube.com/tkorting
#
# Feel free to use and share this code.
#
# Thales Sehn Körting

# importing libraries
# needed to open GeoTIFF files
from osgeo import gdal
from gdalconst import *
# needed to create plots
import matplotlib.pyplot as plt
# needed to manipulate arrays
import numpy as np
# needed to compute mode from arrays
from scipy import stats

# define the file names for t1 and t2 images
filename_t1 = "t1_clip.tif"
filename_t2 = "t2_clip_register.tif"
# define constants
rows = 500
columns = 700
figure_border = 25
# load the datasets
dataset_t1 = gdal.Open(filename_t1, GA_ReadOnly) 
dataset_t2 = gdal.Open(filename_t2, GA_ReadOnly) 
# get the reference for the first bands of t1 and t2
ndvi_t1 = dataset_t1.GetRasterBand(1)
ndvi_t2 = dataset_t2.GetRasterBand(1)

# plot the histograms for both bands
plt.figure(figsize=(10, 8))
plt.plot(ndvi_t1.GetHistogram(), label="$I_{t_1}$")
plt.plot(ndvi_t2.GetHistogram(), label="$I_{t_2}$")
plt.legend()
plt.grid(b=True, color='gray', linestyle='--', linewidth=0.5);
plt.savefig("histograms_t1xt2.png", format='png', dpi=200)
plt.close()

# compute NDTS
array_t1 = ndvi_t1.ReadAsArray()[0:rows, 0:columns].astype(float)
array_t2 = ndvi_t2.ReadAsArray()[0:rows, 0:columns].astype(float)
array_ndts = (array_t2 - array_t1) / (array_t2 + array_t1)
# create figure to display original NDTS
output_fig, (ndts_ax, histogram_ax) = plt.subplots(figsize=(10, 3), ncols=2)
ndts_ax.imshow(array_ndts, cmap="gray")
ndts_ax.set_xlim([0 - figure_border, columns + figure_border])
ndts_ax.set_ylim([rows + figure_border, 0 - figure_border])
histogram_ax.hist(array_ndts.ravel(), bins=200, range=(-1.0, 1.0))
histogram_ax.grid(b=True, color='gray', linestyle='--', linewidth=0.5);
output_fig.savefig("ndts.png", format='png', dpi=200)
plt.close()

# compute square of NDTS
array_square_ndts = array_ndts * array_ndts
# create figure to display square of NDTS
output_fig, (square_ndts_ax, histogram_ax) = plt.subplots(figsize=(10, 3), ncols=2)
square_ndts_ax.imshow(array_square_ndts, cmap="gray")
square_ndts_ax.set_xlim([0 - figure_border, columns + figure_border])
square_ndts_ax.set_ylim([rows + figure_border, 0 - figure_border])

histogram_ax.hist(array_square_ndts.ravel(), bins=200, range=(-0.25, 0.25))
histogram_ax.grid(b=True, color='gray', linestyle='--', linewidth=0.5);
output_fig.savefig("square_ndts.png", format='png', dpi=200)
plt.close()

# apply threshold to highlight change detection
threshold = 0.1
threshold_array_square_ndts = array_square_ndts > threshold
# create figure to display change detection
output_fig, threshold_ax = plt.subplots(figsize=(10, 8), ncols=1)
threshold_ax.imshow(threshold_array_square_ndts, cmap="gray")
threshold_ax.set_xlim([0 - figure_border, columns + figure_border])
threshold_ax.set_ylim([rows + figure_border, 0 - figure_border])
output_fig.savefig("threshold_square_ndts.png", format='png', dpi=200)
plt.close()

# apply 3x3 mode filter to remove noise
mode_threshold_array_square_ndts = threshold_array_square_ndts
for i in range(1,rows):
	for j in range(1,columns):
		values = np.array(threshold_array_square_ndts[i-1:i+2, j-1:j+2])
		mode_threshold_array_square_ndts[i, j] = stats.mode(values.ravel())[0][0]
# create figure to display filtered change detection
output_fig, threshold_ax = plt.subplots(figsize=(10, 8), ncols=1)
threshold_ax.imshow(mode_threshold_array_square_ndts, cmap="gray")
threshold_ax.set_xlim([0 - figure_border, columns + figure_border])
threshold_ax.set_ylim([rows + figure_border, 0 - figure_border])
output_fig.savefig("mode_threshold_square_ndts.png", format='png', dpi=200)
plt.close()
