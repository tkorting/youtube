# Subscribe to my channel, share and like my videos at
# http://youtube.com/tkorting
#
# This source code is used to create a step-by-step
# animation about image pan-sharpening using RGB and 
# HSV color transforms. Feel free to use and share this 
# code.
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
# needed to resize raster and apply HSV <-> RGB color transforms
from skimage.transform import resize
from skimage.color import rgb2hsv, hsv2rgb

# define the file names for RGB and panchromatic (pan) images
filename_rgb = "/vsicurl/https://raw.githubusercontent.com/tkorting/remote-sensing-images/master/wv2_RGB_clip_contrast_low_spatial_resolution.tif"
filename_pan = "/vsicurl/https://raw.githubusercontent.com/tkorting/remote-sensing-images/master/wv2_pan_clip_contrast_high_spatial_resolution.tif"

# define constants
figure_border = 5
max_steps = 500

# load the datasets
try:
  dataset_rgb = gdal.Open(filename_rgb, GA_ReadOnly)
  dataset_pan = gdal.Open(filename_pan, GA_ReadOnly) 
except:
  print('error loading files')

# retrieve metadata
columns = dataset_rgb.RasterXSize
rows = dataset_rgb.RasterYSize
max_pixel = 65535 # in this case we used 16-bit images
# get the arrays for Red, Green, Blue and pan images
array_rgb = np.zeros((rows, columns, 3))
array_rgb[:,:,0] = dataset_rgb.GetRasterBand(1).ReadAsArray().astype(float)
array_rgb[:,:,1] = dataset_rgb.GetRasterBand(2).ReadAsArray().astype(float)
array_rgb[:,:,2] = dataset_rgb.GetRasterBand(3).ReadAsArray().astype(float)
array_pan = dataset_pan.GetRasterBand(1).ReadAsArray().astype(float)
# normalize RGB and pan to 0..1 interval
array_rgb = array_rgb / max_pixel
array_pan = array_pan / max_pixel

# resize all low spatial resolution images
columns = dataset_pan.RasterXSize
rows = dataset_pan.RasterYSize
array_rgb = resize(array_rgb, (rows, columns))

# create figure to display RGB Vs R, G and B components
output_fig = plt.figure(figsize=(8, 8))
rgb_ax = plt.subplot2grid((2, 2), (0, 0))
rgb_ax.imshow(array_rgb)
rgb_ax.set_title("Color image")
rgb_ax.set_xlim([0 - figure_border, columns + figure_border])
rgb_ax.set_ylim([rows + figure_border, 0 - figure_border])
r_ax = plt.subplot2grid((2, 2), (0, 1))
r_ax.imshow(array_rgb[:, :, 0], cmap="gray")
r_ax.set_title("Red")
r_ax.set_xlim([0 - figure_border, columns + figure_border])
r_ax.set_ylim([rows + figure_border, 0 - figure_border])
g_ax = plt.subplot2grid((2, 2), (1, 0))
g_ax.imshow(array_rgb[:, :, 1], cmap="gray")
g_ax.set_title("Green")
g_ax.set_xlim([0 - figure_border, columns + figure_border])
g_ax.set_ylim([rows + figure_border, 0 - figure_border])
b_ax = plt.subplot2grid((2, 2), (1, 1))
b_ax.imshow(array_rgb[:, :, 2], cmap="gray")
b_ax.set_title("Blue")
b_ax.set_xlim([0 - figure_border, columns + figure_border])
b_ax.set_ylim([rows + figure_border, 0 - figure_border])
plt.tight_layout()
output_fig.savefig("color_vs_rgb.png", format='png', dpi=200)
plt.close()

# make RGB -> HSV transform
array_hsv = rgb2hsv(array_rgb)

# create figure to display RGB Vs H, S and V components
output_fig = plt.figure(figsize=(8, 8))
rgb_ax = plt.subplot2grid((2, 2), (0, 0))
rgb_ax.imshow(array_rgb)
rgb_ax.set_title("Color image")
rgb_ax.set_xlim([0 - figure_border, columns + figure_border])
rgb_ax.set_ylim([rows + figure_border, 0 - figure_border])
h_ax = plt.subplot2grid((2, 2), (0, 1))
h_ax.imshow(array_hsv[:, :, 0], cmap="gray")
h_ax.set_title("Hue")
h_ax.set_xlim([0 - figure_border, columns + figure_border])
h_ax.set_ylim([rows + figure_border, 0 - figure_border])
s_ax = plt.subplot2grid((2, 2), (1, 0))
s_ax.imshow(array_hsv[:, :, 1], cmap="gray")
s_ax.set_title("Saturation")
s_ax.set_xlim([0 - figure_border, columns + figure_border])
s_ax.set_ylim([rows + figure_border, 0 - figure_border])
v_ax = plt.subplot2grid((2, 2), (1, 1))
v_ax.imshow(array_hsv[:, :, 2], cmap="gray")
v_ax.set_title("Value")
v_ax.set_xlim([0 - figure_border, columns + figure_border])
v_ax.set_ylim([rows + figure_border, 0 - figure_border])
plt.tight_layout()
output_fig.savefig("color_vs_hsv.png", format='png', dpi=200)
plt.close()

# create figure to display pan Vs Value
output_fig, (value_ax, pan_ax) = plt.subplots(figsize=(8, 4), ncols=2)
value_ax.imshow(array_hsv[:, :, 2], cmap="gray")
value_ax.set_title("Value")
value_ax.set_xlim([0 - figure_border, columns + figure_border])
value_ax.set_ylim([rows + figure_border, 0 - figure_border])
pan_ax.imshow(array_pan, cmap="gray")
pan_ax.set_title("Panchromatic")
pan_ax.set_xlim([0 - figure_border, columns + figure_border])
pan_ax.set_ylim([rows + figure_border, 0 - figure_border])
plt.tight_layout()
output_fig.savefig("value_vs_pan.png", format='png', dpi=200)
plt.close()

# create animation for changing Value component with pan
filename_in_animation = "animation/value_to_pan_"
step = 0
all_rows = np.linspace(0, rows, max_steps)
all_columns = np.linspace(0, columns, max_steps)
for row, column in zip(all_rows, all_columns):
 	array_hsv[0:int(row), 0:int(column), 2] = array_pan[0:int(row), 0:int(column)]
 	output_fig = plt.figure(figsize=(9, 5))
 	animation_ax = output_fig.add_subplot(111)
 	animation_img = plt.imshow(array_hsv[:, :, 2], cmap='gray')
 	animation_ax.set_xlim([0 - figure_border, columns + figure_border])
 	animation_ax.set_ylim([rows + figure_border, 0 - figure_border])
 	plt.tight_layout()
 	output_fig.savefig(filename_in_animation+str(step).zfill(6)+".png", format='png', dpi=200)
 	plt.close()
 	step = step + 1

# make HSV -> RGB transform, replacing Value component by pan
array_hsv[:, :, 2] = array_pan
new_array_rgb = hsv2rgb(array_hsv)

# create figure to display RGB Vs H, S components and panchromatic
output_fig = plt.figure(figsize=(8, 8))
new_rgb_ax = plt.subplot2grid((2, 2), (0, 0))
new_rgb_ax.imshow(new_array_rgb)
new_rgb_ax.set_title("pan-sharpened image")
new_rgb_ax.set_xlim([0 - figure_border, columns + figure_border])
new_rgb_ax.set_ylim([rows + figure_border, 0 - figure_border])
pan_ax = plt.subplot2grid((2, 2), (1, 0))
pan_ax.imshow(array_pan, cmap="gray")
pan_ax.set_title("Panchromatic")
pan_ax.set_xlim([0 - figure_border, columns + figure_border])
pan_ax.set_ylim([rows + figure_border, 0 - figure_border])
h_ax = plt.subplot2grid((2, 2), (0, 1))
h_ax.imshow(array_hsv[:, :, 0], cmap="gray")
h_ax.set_title("Hue")
h_ax.set_xlim([0 - figure_border, columns + figure_border])
h_ax.set_ylim([rows + figure_border, 0 - figure_border])
s_ax = plt.subplot2grid((2, 2), (1, 1))
s_ax.imshow(array_hsv[:, :, 1], cmap="gray")
s_ax.set_title("Saturation")
s_ax.set_xlim([0 - figure_border, columns + figure_border])
s_ax.set_ylim([rows + figure_border, 0 - figure_border])
plt.tight_layout()
output_fig.savefig("pan_sharpened_vs_hspan.png", format='png', dpi=200)
plt.close()

# create figure to display original RGB Vs new RGB
output_fig, (pan_ax, value_ax) = plt.subplots(figsize=(8, 4), ncols=2)
pan_ax.imshow(array_rgb)
pan_ax.set_title("Original Color image")
pan_ax.set_xlim([0 - figure_border, columns + figure_border])
pan_ax.set_ylim([rows + figure_border, 0 - figure_border])
value_ax.imshow(new_array_rgb)
value_ax.set_title("pan-sharpened image")
value_ax.set_xlim([0 - figure_border, columns + figure_border])
value_ax.set_ylim([rows + figure_border, 0 - figure_border])
plt.tight_layout()
output_fig.savefig("original_vs_pan_sharpened.png", format='png', dpi=200)

# close datasets
dataset_rgb = None
dataset_pan = None
