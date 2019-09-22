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
# needed to create plots
import matplotlib.pyplot as plt
import matplotlib.colors as colors
# needed to manipulate arrays
import numpy as np

# define constants
figure_border = 25
power = 2
filename_in_animation = "animation/"
filename_in_results = "results/"
L = 256
normalization_0_L = colors.Normalize(vmin=0, vmax=L)

# load the dataset
filename = "pan5_sjcampos_original.tif"
dataset = gdal.Open(filename, GA_ReadOnly)

# retrieve metadata from raster
rows = dataset.RasterYSize
columns = dataset.RasterXSize
N = rows * columns
bands = 1
higher_frequency = 25000
(min_pixel, max_pixel) = dataset.GetRasterBand(1).ComputeRasterMinMax()

# get arrays to compute enhancements
array_pixels = dataset.GetRasterBand(1).ReadAsArray().astype(float)
# normalize original raster to min/max
array_pixels = (L - 1) * (array_pixels - min_pixel) / (max_pixel - min_pixel)
min_pixel = array_pixels.min()
max_pixel = array_pixels.max()

# create animation for gain and offset
# 0 - gain
# 1 - offset
enhancement_names = ('gain', 'offset')
array_enhanced_pixels = np.zeros((5, array_pixels.shape[0], array_pixels.shape[1]))
array_x_axis = np.arange(L)

# print basic metadata
print ("image metadata:")
print (rows, "rows x", columns, "columns x", bands, "bands")
print ("minimum pixel", min_pixel, "max pixel", max_pixel)
print ("total of", N, "pixels and L is", L)

# save original image
output_fig = plt.figure()
normalization_0_L = colors.Normalize(vmin=0, vmax=L)
enhanced_raster_ax = output_fig.add_subplot(111)
title = "original image"
enhanced_raster_ax.set_title(title)
enhanced_raster_img = plt.imshow(array_pixels, cmap="gray", norm=normalization_0_L)
enhanced_raster_ax.set_xlim([0 - figure_border, columns + figure_border])
enhanced_raster_ax.set_ylim([rows + figure_border, 0 - figure_border])
output_fig.savefig(filename_in_results+"original_raster.png", format='png', dpi=200)

# save original histogram
output_fig = plt.figure()
# create histogram with original image
histogram_ax = output_fig.add_subplot(111)
title = "histogram of original image"
histogram_ax.set_title(title)
histogram_ax.hist(np.ravel(array_pixels), bins=L)
histogram_ax.set_xlim([0, L])
histogram_ax.set_ylim([0, higher_frequency])
output_fig.savefig(filename_in_results+"histogram_original_raster.png", format='png', dpi=200)

# create animations for gain and offset
constants = np.zeros((2, L))
# gains between 0.1 and 3
constants[0] = np.linspace(0.1, 3, L)
# offsets between 1 and 100
constants[1] = np.linspace(1, 100, L)
for enhancement in range(len(enhancement_names)):
	step = 1
	for constant in constants[enhancement]:
		print("current", enhancement_names[enhancement], '{:06.3f}'.format(constant))
		if enhancement_names[enhancement] == 'gain':
			# gain
			array_enhanced_pixels = constant * array_pixels
			array_y_axis = constant * array_x_axis
		elif enhancement_names[enhancement] == 'offset':
			# offset
			array_enhanced_pixels = array_pixels + constant
			array_y_axis = array_x_axis + constant

		output_fig = plt.figure(figsize=(8, 8))
		# create histogram with original image
		histogram_ax = plt.subplot2grid((2, 2), (0, 0))
		right_ax = histogram_ax.twinx()
		title = "histogram of original image"
		histogram_ax.set_title(title)
		histogram_ax.hist(np.ravel(array_pixels), bins=L)
		histogram_ax.set_xlim([0, L])
		histogram_ax.set_ylim([0, higher_frequency])

		# create visualization of original image
		original_raster_ax = plt.subplot2grid((2, 2), (0, 1))
		title = "original image"
		original_raster_ax.set_title(title)
		normalization_0_L = colors.Normalize(vmin=0, vmax=L)
		plt.imshow(array_pixels, cmap="gray", norm=normalization_0_L)
		original_raster_ax.set_xlim([0 - figure_border, columns + figure_border])
		original_raster_ax.set_ylim([rows + figure_border, 0 - figure_border])

		# plot functions
		right_ax.plot(array_x_axis, array_y_axis, "r-")
		right_ax.set_ylim([0, L])

		# create histogram of current enhancement
		histogram_out_ax = plt.subplot2grid((2, 2), (1, 0))
		title = "histogram of image with " + enhancement_names[enhancement] + " " + '{:06.3f}'.format(constant)
		histogram_out_ax.set_title(title)
		histogram_out_ax.hist(np.ravel(array_enhanced_pixels), bins=L) 
		histogram_out_ax.set_xlim([0, L])
		histogram_out_ax.set_ylim([0, higher_frequency])

		# create partial visualization of enhanced image
		enhanced_raster_ax = plt.subplot2grid((2, 2), (1, 1))
		title = "image with " + enhancement_names[enhancement] + " " + '{:06.3f}'.format(constant)
		enhanced_raster_ax.set_title(title)
		normalization_0_L = colors.Normalize(vmin=0, vmax=L)
		plt.imshow(array_enhanced_pixels, cmap="gray", norm=normalization_0_L)
		enhanced_raster_ax.set_xlim([0 - figure_border, columns + figure_border])
		enhanced_raster_ax.set_ylim([rows + figure_border, 0 - figure_border])

		# save image enhanced with log
		plt.tight_layout()
		output_fig.savefig(filename_in_animation + enhancement_names[enhancement] + "_" + str(step).zfill(6) + ".png", format='png', dpi=200)
		step = step + 1
		plt.close()

# close input dataset
dataset = None

# load the dataset
filename = "pan5_sjcampos_contrast.tif"
dataset = gdal.Open(filename, GA_ReadOnly)

# retrieve metadata from raster
rows = dataset.RasterYSize
columns = dataset.RasterXSize
N = rows * columns
bands = 1
L = 256
higher_frequency = 25000
(min_pixel, max_pixel) = dataset.GetRasterBand(1).ComputeRasterMinMax()

# get arrays to compute enhancements
array_pixels = dataset.GetRasterBand(1).ReadAsArray().astype(float)
# normalize original raster to min/max
array_pixels = (L - 1) * (array_pixels - min_pixel) / (max_pixel - min_pixel)
min_pixel = array_pixels.min()
max_pixel = array_pixels.max()

# create arrays with all enhanced images
# 0 - log
# 1 - nth root
# 2 - negative
# 3 - nth power
# 4 - inverse log
enhancement_names = ('log', 'nth root', 'negative', 'nth power', 'inverse log')
array_enhanced_pixels = np.zeros((5, array_pixels.shape[0], array_pixels.shape[1]))
array_x_axis = np.arange(L)
array_y_axis = np.zeros((5, np.arange(L).shape[0]))

# create enhanced rasters and axis to plot histograms, based on [0, L-1]
# log
array_enhanced_pixels[0] = L * np.log(1 + array_pixels) / np.log(L)
array_y_axis[0] = L * np.log(1 + array_x_axis) / np.log(L)
# nth root
array_enhanced_pixels[1] = np.power(L, 1 / power) * np.power(array_pixels, 1 / power)
array_y_axis[1] = np.power(L, 1 / power) * np.power(array_x_axis, 1 / power)
# negative
array_enhanced_pixels[2] = L - 1 - array_pixels
array_y_axis[2] = L - 1 - array_x_axis
# nth power
array_enhanced_pixels[3] = np.power(array_pixels, power) / L
array_y_axis[3] = np.power(array_x_axis, power) / L
# inverse log
array_enhanced_pixels[4] = np.power(np.exp(array_pixels), np.log(L) / L) - 1
array_y_axis[4] = np.power(np.exp(array_x_axis), np.log(L) / L) - 1

# print basic metadata
print ("image metadata:")
print (rows, "rows x", columns, "columns x", bands, "bands")
print ("minimum pixel", min_pixel, "max pixel", max_pixel)
print ("total of", N, "pixels and L is", L)

# create animations for all enhancements
for enhancement in range(len(enhancement_names)):
	for step in range(1, L):
		print (enhancement_names[enhancement], step)

		output_fig = plt.figure(figsize=(8, 8))
		# create histogram with original image
		histogram_ax = plt.subplot2grid((2, 2), (0, 0))
		right_ax = histogram_ax.twinx()
		title = "histogram of original image"
		histogram_ax.set_title(title)
		histogram_ax.hist(np.ravel(array_pixels), bins=L) 
		histogram_ax.set_xlim([0, L])
		histogram_ax.set_ylim([0, higher_frequency])

		# create partial visualization of original image
		original_raster_ax = plt.subplot2grid((2, 2), (0, 1))
		title = "original image"
		original_raster_ax.set_title(title)
		tmp_array_pixels = array_pixels.copy()
		tmp_array_pixels[array_pixels > step] = L
		plt.imshow(tmp_array_pixels, cmap="gray", norm=normalization_0_L)
		original_raster_ax.set_xlim([0 - figure_border, columns + figure_border])
		original_raster_ax.set_ylim([rows + figure_border, 0 - figure_border])

		# plot functions
		right_ax.bar(step, array_y_axis[enhancement][step], 2, fc='r')
		right_ax.plot(array_x_axis, array_y_axis[enhancement], "r-")
		right_ax.set_ylim([0, L])

		# create partial histogram with log
		histogram_out_ax = plt.subplot2grid((2, 2), (1, 0))
		title = "histogram of image enhanced with " + enhancement_names[enhancement]
		histogram_out_ax.set_title(title)
		tmp_array = array_enhanced_pixels[enhancement].copy()
		tmp_array[array_pixels > step] = L
		histogram_out_ax.hist(np.ravel(tmp_array), bins=L) 
		histogram_out_ax.set_xlim([0, L])
		histogram_out_ax.set_ylim([0, higher_frequency])

		# create partial visualization of enhanced image
		enhanced_raster_ax = plt.subplot2grid((2, 2), (1, 1))
		title = "image enhanced with " + enhancement_names[enhancement]
		enhanced_raster_ax.set_title(title)
		normalization_0_L = colors.Normalize(vmin=0, vmax=L)
		tmp_array_pixels = array_enhanced_pixels[enhancement].copy()
		tmp_array_pixels[array_pixels > step] = L
		plt.imshow(tmp_array_pixels, cmap="gray", norm=normalization_0_L)
		enhanced_raster_ax.set_xlim([0 - figure_border, columns + figure_border])
		enhanced_raster_ax.set_ylim([rows + figure_border, 0 - figure_border])

		# save image enhanced with log
		plt.tight_layout()
		output_fig.savefig(filename_in_animation + enhancement_names[enhancement] + "_" + str(step).zfill(6)+".png", format='png', dpi=200)
		plt.close()

	# save enhanced image
	output_fig = plt.figure()
	normalization = colors.Normalize(vmin=array_enhanced_pixels[enhancement].min(), vmax=array_enhanced_pixels[enhancement].max())
	enhanced_raster_ax = output_fig.add_subplot(111)
	title = "image enhanced with " + enhancement_names[enhancement]
	enhanced_raster_ax.set_title(title)
	enhanced_raster_img = plt.imshow(array_enhanced_pixels[enhancement], cmap="gray", norm=normalization)
	enhanced_raster_ax.set_xlim([0 - figure_border, columns + figure_border])
	enhanced_raster_ax.set_ylim([rows + figure_border, 0 - figure_border])
	output_fig.savefig(filename_in_results + "enhanced_raster_" + enhancement_names[enhancement] + ".png", format='png', dpi=200)

# close input dataset
dataset = None
