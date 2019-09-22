# Subscribe to my channel, share and like my videos at
# http://youtube.com/tkorting
#
# Feel free to use and share this code.
#
# Thales Sehn Körting

# import libraries
from osgeo import gdal
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.axes_grid1 import make_axes_locatable

# gdal constants
from gdalconst import *

# inform to use GDAL exceptions
gdal.UseExceptions()

# open dataset
filename = "integral-image-test.tif"
dataset = gdal.Open(filename, GA_ReadOnly)

# retrieve metadata from raster
rows = min(dataset.RasterXSize, dataset.RasterYSize)
columns = min(dataset.RasterXSize, dataset.RasterYSize)
N = rows * columns
bands = dataset.RasterCount

# print basic metadata
print ("image metadata:")
print (rows, "rows x", columns, "columns x", bands, "bands")

# retrieve arrays from input image
array_R = dataset.GetRasterBand(1).ReadAsArray()[0:rows,0:columns]
array_G = dataset.GetRasterBand(2).ReadAsArray()[0:rows,0:columns]
array_B = dataset.GetRasterBand(3).ReadAsArray()[0:rows,0:columns]
# we will the intensity image (the average of RGB channels) for computing the integral image 
array_intensity = (array_R.astype(float) + array_G.astype(float) + array_B.astype(float)) / 3
array_intensity *= 255 / array_intensity.max()

# create the array of integral image
array_integral = np.zeros_like(array_intensity)

# compute values for integral image
figure_steps = 0
for r in range(rows):
    print(r)
    for c in range(columns):

        # compute the integral image (fast way)
        B = 0
        C = 0
        D = 0
        if r > 0:
            B = array_integral[r - 1, c]
        if c > 0:
            C = array_integral[r, c - 1]
        if r > 0 and c > 0:
            D = array_integral[r - 1, c - 1]

        array_integral[r, c] = array_intensity[r, c] + B + C - D

        # compute the integral image (slow way)
        # for i in range(r):
        #     for j in range(c):
        #         array_integral[r, c] = array_integral[r, c] + array_intensity[i, j]

        # remove the following comment to make only integral image computing
        # make the following comment to make the images for step-by-step animation
        # continue
        if r != c:
            continue

        # display partial result in png animation
        output_figure_path = 'animation/integral_' + str(figure_steps).zfill(6) + '.png'
        figure_border = 25

        # create figure with 2 columns
        output_fig, (input_ax, integral_ax) = plt.subplots(figsize=(8, 4), ncols=2)

        # draw input image with rectangle
        divider_input = make_axes_locatable(input_ax)
        ax_input = divider_input.new_horizontal(size="5%", pad=0.05)
        fig0 = integral_ax.get_figure()
        # fig0.add_axes(ax_input)
        input_ax.imshow(array_intensity, cmap='gray', vmin=0, vmax=255)
        # define rectangle of integral: (0,0) -> (r, c)
        x = [0, c, c, 0, 0]
        y = [0, 0, r, r, 0]
        input_ax.fill(x, y, fill = None, linewidth=1, alpha=0.5, color='red')
        input_ax.set_xlim([0 - figure_border, columns + figure_border])
        input_ax.set_ylim([rows + figure_border, 0 - figure_border])

        # draw integral image with scale
        divider = make_axes_locatable(integral_ax)
        ax_cb = divider.new_horizontal(size="5%", pad=0.05)
        fig1 = integral_ax.get_figure()
        fig1.add_axes(ax_cb)
        im = integral_ax.imshow(array_integral, vmin=0, vmax=131439465.33333834)

        plt.colorbar(im, cax=ax_cb)
        ax_cb.yaxis.tick_right()
        ax_cb.yaxis.set_tick_params(labelright=False)

        integral_ax.set_xlim([0 - figure_border, columns + figure_border])
        integral_ax.set_ylim([rows + figure_border, 0 - figure_border])
        
        output_fig.savefig(output_figure_path, format='png', dpi=200)
        plt.close()

        figure_steps = figure_steps + 1
        
print (array_integral.max())
np.save(filename + '.array_integral_image.npy', array_integral)

# close dataset
dataset = None
