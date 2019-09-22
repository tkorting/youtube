# Subscribe to my channel, share and like my videos at
# http://youtube.com/tkorting
#
# This source code is used to create a step-by-step
# animation about image enhancement. Feel free to 
# use and share this code.
#
# Thales Sehn Körting

# importing libraries
# needed to open GeoTIFF files
from osgeo import gdal
from gdalconst import *
# needed to create plots and squares
import matplotlib.pyplot as plt
import matplotlib.patches as patches
# needed to manipulate arrays
import numpy as np
# needed to compute mode from arrays
from scipy import stats
# needed to deal with colorbars
from mpl_toolkits.axes_grid1 import make_axes_locatable

# define constants
figure_border = 25
epsilon = 0.0001
max_y = 5000
max_steps = 500
square_side = 20
threshold_for_ndwi = 0.2
threshold_for_ship = 2

# define filenames
filename_rgb = "true_color_rgb.png" # available at https://apps.sentinel-hub.com/eo-browser/?lat=-24.1176&lng=-46.3688&zoom=12&time=2019-04-02
filename_green = "b03_green.png" 
filename_nir = "b08_nir.png" 

# load the datasets
dataset_rgb = gdal.Open(filename_rgb, GA_ReadOnly) 
dataset_green = gdal.Open(filename_green, GA_ReadOnly) 
dataset_nir = gdal.Open(filename_nir, GA_ReadOnly) 

# retrieve metadata from RGB raster
rows = dataset_rgb.RasterYSize
columns = dataset_rgb.RasterXSize
N = rows * columns
bands = 3

# get arrays to compute NDWI
array_green = dataset_green.GetRasterBand(1).ReadAsArray().astype(float)
array_nir = dataset_nir.GetRasterBand(1).ReadAsArray().astype(float)
array_ndwi = (array_green - array_nir)/(array_green + array_nir)

# get true color raster to show result
array_rgb = np.zeros((rows, columns, 3), dtype=np.uint8)
array_rgb[:,:,0] = dataset_rgb.GetRasterBand(1).ReadAsArray()
array_rgb[:,:,1] = dataset_rgb.GetRasterBand(2).ReadAsArray()
array_rgb[:,:,2] = dataset_rgb.GetRasterBand(3).ReadAsArray()

# print basic metadata
print ("image metadata:")
print (rows, "rows x", columns, "columns x", bands, "bands")

# create plot with ndwi band 
output_fig = plt.figure()
ndwi_ax = output_fig.add_subplot(111)
ndwi_img = plt.imshow(array_ndwi, cmap="gray")
ndwi_ax.set_xlim([0 - figure_border, columns + figure_border])
ndwi_ax.set_ylim([rows + figure_border, 0 - figure_border])
output_fig.savefig("results/output_ndwi.png", format='png', dpi=200)

# create animation for finding threshold in ndwi
min_R = np.percentile(array_ndwi.ravel(), 1)
max_R = np.percentile(array_ndwi.ravel(), 99)
thresholds = np.linspace(min_R, max_R, max_steps)
back_tresholds = np.linspace(max_R, threshold_for_ndwi, max_steps)
filename_in_animation = "animation/threshold_ndwi_step_"

step = 0
for threshold in np.concatenate((thresholds, back_tresholds)):
	print (step)

	output_fig = plt.figure(figsize=(9, 5))

	# create histogram with current threshold
	histogram_ax = plt.subplot2grid((2, 3), (0, 2), rowspan=2)
	title = "threshold = "+str(f'{threshold:1.5f}')
	histogram_ax.set_title(title)
	histogram_ax.hist(array_ndwi.ravel(), bins=200, range=(min_R, max_R), fc='k', ec='k', orientation='horizontal')
	histogram_ax.barh(threshold, max_y, 0.01, fc='r')
	histogram_ax.set_ylim([max_R, min_R])
	histogram_ax.set_xlim([0, max_y])

	# create plot with rgb image
	rgb_ax = plt.subplot2grid((2, 3), (0, 0), colspan=2)
	rgb_ax.imshow(array_rgb)
	rgb_ax.set_xlim([0 - figure_border, columns + figure_border])
	rgb_ax.set_ylim([rows + figure_border, 0 - figure_border])
	
	# create plot with ratio band with threshold
	threshold_ax = plt.subplot2grid((2, 3), (1, 0), colspan=2)
	threshold_array_ndwi = array_ndwi > threshold
	threshold_ax.imshow(threshold_array_ndwi, cmap="gray")
	threshold_ax.set_xlim([0 - figure_border, columns + figure_border])
	threshold_ax.set_ylim([rows + figure_border, 0 - figure_border])
	plt.tight_layout()

	output_fig.savefig(filename_in_animation+str(step).zfill(6)+".png", format='png', dpi=200)
	step = step + 1
	plt.close()

filename_in_results = "results/tn"+str(threshold_for_ndwi).zfill(3)+"_ts"+str(threshold_for_ship).zfill(2)+"_"

# create plot with ndwi band with threshold
threshold_ndwi = array_ndwi > threshold_for_ndwi
output_fig = plt.figure()
threshold_ndwi_ax = output_fig.add_subplot(111)
threshold_ndwi_img = plt.imshow(threshold_ndwi, cmap="gray")
threshold_ndwi_ax.set_xlim([0 - figure_border, columns + figure_border])
threshold_ndwi_ax.set_ylim([rows + figure_border, 0 - figure_border])
output_fig.savefig(filename_in_results+"threshold_ndwi.png", format='png', dpi=200)

# apply 3x3 mode filter to remove noise and save plot
mode_threshold_ndwi = np.copy(threshold_ndwi)
for i in range(1,rows):
	for j in range(1,columns):
		values = np.array(threshold_ndwi[i-1:i+2, j-1:j+2])
		mode_threshold_ndwi[i, j] = stats.mode(values.ravel())[0][0]
output_fig = plt.figure()
mode_threshold_ndwi_ax = output_fig.add_subplot(111)
mode_threshold_ndwi_img = plt.imshow(mode_threshold_ndwi, cmap="gray")
mode_threshold_ndwi_ax.set_xlim([0 - figure_border, columns + figure_border])
mode_threshold_ndwi_ax.set_ylim([rows + figure_border, 0 - figure_border])
output_fig.savefig(filename_in_results+"mode_threshold_ndwi.png", format='png', dpi=200)

# apply 3x3 filter to find points related to ships (highpass filter set)
ships_in_ndwi = np.zeros_like(array_ndwi)
line_detection_mask_horizontal = np.array((-1, -1, -1, 2, 2, 2, -1, -1, -1))
line_detection_mask_plus45 = np.array((-1, -1, 2, -1, 2, -1, 2, -1, -1))
line_detection_mask_vertical = np.array((-1, 2, -1, -1, 2, -1, -1, 2, -1))
line_detection_mask_minus45 = np.array((2, -1, -1, -1, 2, -1, -1, -1, 2))
for i in range(1,rows):
	for j in range(1,columns):
		values = np.array(array_ndwi[i-1:i+2, j-1:j+2])
		ships_in_ndwi[i, j] = False

		if mode_threshold_ndwi[i, j]:
			if values.ravel().shape == line_detection_mask_horizontal.shape:
				horizontal = np.abs((values.ravel() * line_detection_mask_horizontal).sum())
				plus45 = np.abs((values.ravel() * line_detection_mask_plus45).sum())
				vertical = np.abs((values.ravel() * line_detection_mask_vertical).sum())
				minus45 = np.abs((values.ravel() * line_detection_mask_minus45).sum())
				line_detection = np.array((horizontal, plus45, vertical, minus45))
				ships_in_ndwi[i, j] = line_detection.max() >= threshold_for_ship

output_fig = plt.figure()
ships_in_ndwi_ax = output_fig.add_subplot(111)
ships_in_ndwi_img = plt.imshow(ships_in_ndwi, cmap="gray")
ships_in_ndwi_ax.set_xlim([0 - figure_border, columns + figure_border])
ships_in_ndwi_ax.set_ylim([rows + figure_border, 0 - figure_border])
output_fig.savefig(filename_in_results+"ships_in_ndwi.png", format='png', dpi=200)

# create plot with rgb image with ships highlighted
output_fig = plt.figure(figsize=(9, 5))

rgb_ax = output_fig.add_subplot(111)
rgb_img = plt.imshow(array_rgb)
rectangles = np.zeros_like(ships_in_ndwi)
for row in range(1, rows):
	for column in range(1, columns):
		if ships_in_ndwi[row, column]:
			column_start = int(column-square_side/2)
			column_end = int(column+square_side/2)
			row_start = int(row-square_side/2)
			row_end = int(row+square_side/2)
			if rectangles[row_start:row_end, column_start:column_end].sum() == 0:
				ship_square = patches.Rectangle((column_start,row_start),square_side,square_side,linewidth=1,edgecolor='r',facecolor='none')
				rgb_ax.add_patch(ship_square) 
				rectangles[row_start:row_end, column_start:column_end] = 1.0
rgb_ax.set_xlim([0 - figure_border, columns + figure_border])
rgb_ax.set_ylim([rows + figure_border, 0 - figure_border])
output_fig.savefig(filename_in_results+"ships_in_rgb.png", format='png', dpi=500)

# loop over points to draw squares when ship is detected
filename_in_animation = "animation/ships_in_rgb_step_"
step = 0
bar_rows = np.linspace(0, rows, max_steps)
bar_columns = np.linspace(0, columns, max_steps)
for bar_row, bar_column in zip(bar_rows, bar_columns):
	print (step)
	output_fig = plt.figure(figsize=(9, 5))

	rgb_ax = output_fig.add_subplot(111)
	rgb_img = plt.imshow(array_rgb)
	rgb_ax.barh(bar_row, columns, 3, fc='r')
	rgb_ax.bar(bar_column, rows, 3, fc='r')
	rectangles = np.zeros_like(ships_in_ndwi)
	for row in range(1, int(bar_row)):
		for column in range(1, int(bar_column)):
			if ships_in_ndwi[row, column]:
				column_start = int(column-square_side/2)
				column_end = int(column+square_side/2)
				row_start = int(row-square_side/2)
				row_end = int(row+square_side/2)
				if rectangles[row_start:row_end, column_start:column_end].sum() == 0:
					ship_square = patches.Rectangle((column_start,row_start),square_side,square_side,linewidth=1,edgecolor='r',facecolor='none')
					rgb_ax.add_patch(ship_square) 
					rectangles[row_start:row_end, column_start:column_end] = 1.0
			
	rgb_ax.set_xlim([0 - figure_border, columns + figure_border])
	rgb_ax.set_ylim([rows + figure_border, 0 - figure_border])
	output_fig.savefig(filename_in_animation+str(step).zfill(6)+".png", format='png', dpi=200)
	step = step + 1

# close all datasets
dataset_rgb = None
dataset_green = None
dataset_nir = None
