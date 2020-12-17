# import libraries
from osgeo import gdal
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.mplot3d import Axes3D

# gdal constants
from gdalconst import *

# inform to use GDAL exceptions
gdal.UseExceptions()

# open dataset
filename = "CBERS_4_MUX_20170810_152_123_L4_BANDS765_crop_contrast.tif"
dataset = gdal.Open(filename, GA_ReadOnly)

# retrieve metadata from raster
rows = dataset.RasterYSize
columns = dataset.RasterXSize
N = rows * columns
bands = dataset.RasterCount

# print basic metadata
print ("image metadata:")
print (rows, "rows x", columns, "columns x", bands, "bands")

# variables to control graph rotation and zoom in animation
figure_border = 25
figure_steps = 0
jumps = columns / 2
j = 0
angle = 20
angle_delta = 0.125
max_angle = 60
min_angle = 10
dist_delta = -0.01
max_dist = 8.5
min_dist = 4
dist = max_dist
animation_steps = 2000

# parameters for kNN algorithm
k = 3
max_distance = 100
min_distance = 1
actual_max_distance = min_distance
step_distance = max_distance / animation_steps

# parameters for colormap used by classification
default_colormap = 'tab20'
colormap_vmax = 20
offset = 50

# retrieve arrays from input image, 3 channels in this case
array_R = dataset.GetRasterBand(1).ReadAsArray().astype(float)
array_G = dataset.GetRasterBand(2).ReadAsArray().astype(float)
array_B = dataset.GetRasterBand(3).ReadAsArray().astype(float)
array_RGB = np.zeros((rows, columns, bands), dtype=np.uint8)
array_RGB[:,:,0] = array_R
array_RGB[:,:,1] = array_G
array_RGB[:,:,2] = array_B
array_RGB_copy = array_RGB.copy()

array_RGB[array_RGB > offset] -= offset
array_RGB[array_RGB < offset] = 0

# slightly change position of RGB for better 
# visualization of scatterplot
array_R += np.random.uniform(low=-0.5, high=0.5, size=array_R.shape)
array_G += np.random.uniform(low=-0.5, high=0.5, size=array_G.shape)
array_B += np.random.uniform(low=-0.5, high=0.5, size=array_B.shape)

# samples for classification
# basic format (column, row, class number)
samples = []
samples.append((100, 233, 8))
samples.append((500, 400, 4))
samples.append((650, 100, 2))
samples.append((30, 500, 8))
samples.append((550, 400, 4))
samples.append((620, 100, 2))
samples.append((80, 250, 8))
samples.append((450, 450, 4))
samples.append((650, 50, 2))

all_classes = (0, 8, 4, 2)
colors = {}
cmap = matplotlib.cm.get_cmap(default_colormap)
for one_class in all_classes:
    colors[one_class] = cmap(one_class)

array_R_flatten = array_R.flatten()
array_G_flatten = array_G.flatten()
array_B_flatten = array_B.flatten()

# create scatterplot with animation
if True:
    for r in range(rows):
        print(r, '', end='', flush=True)

        for c in range(columns):
            # update pixels in animation with offset
            array_RGB[r, c, :] = array_RGB[r, c, :] + offset

            if j > jumps:
                j = 0
            else:
                j = j + 1
                continue

            # display partial result in png animation
            output_figure_path = 'animation/scatterplot_' + str(figure_steps).zfill(6) + '.png'

            # create figure with 2 columns
            output_fig = plt.figure(figsize=(10, 4))
            input_ax = output_fig.add_subplot(121)
            scatterplot_ax = output_fig.add_subplot(122, projection='3d')
            
            # draw input image with actual pixel
            input_ax.imshow(array_RGB)
            # input_ax.set_title('Input image')
            # input_ax.plot(c, r, '.')
            input_ax.set_xlim([0 - figure_border, columns + figure_border])
            input_ax.set_ylim([rows + figure_border, 0 - figure_border])
            input_ax.xaxis.set_tick_params(labelsize=5)
            input_ax.yaxis.set_tick_params(labelsize=5)

            # draw partial histogram
            reds = array_R_flatten[0:(r * columns + c)]
            greens = array_G_flatten[0:(r * columns + c)]
            blues = array_B_flatten[0:(r * columns + c)]

            scatterplot_ax.scatter(reds, greens, blues, s=0.3, c=np.array(colors[0]).reshape(1, -1))
            scatterplot_ax.set_xlabel('red', fontsize=5)
            scatterplot_ax.xaxis.label.set_color('red')
            scatterplot_ax.xaxis.set_tick_params(labelsize=5)
            scatterplot_ax.set_ylabel('green', fontsize=5)
            scatterplot_ax.yaxis.label.set_color('green')
            scatterplot_ax.yaxis.set_tick_params(labelsize=5)
            scatterplot_ax.set_zlabel('blue', fontsize=5)
            scatterplot_ax.zaxis.label.set_color('blue')
            scatterplot_ax.zaxis.set_tick_params(labelsize=5)

            scatterplot_ax.set_xlim([0, 255])
            scatterplot_ax.set_ylim([0, 255])
            scatterplot_ax.set_zlim([0, 255])
            scatterplot_ax.view_init(30, angle)
            scatterplot_ax.dist = dist
            # update rotation angle of plot
            angle = angle + angle_delta
            if (angle > max_angle) or (angle < min_angle):
                angle_delta = angle_delta * -1

            # save partial results in animation        
            output_fig.savefig(output_figure_path, format='png', dpi=200)
            plt.tight_layout()
            plt.close()

            # clean up
            scatterplot_ax = None
            input_ax = None
            output_fig = None

            reds = None
            greens = None
            blues = None

            figure_steps = figure_steps + 1


def compute_euclidean_distance(a, b):
    c = b - a
    d = c * c
    e = d.sum()
    
    return np.sqrt(e)

def knn(samples, r, g, b):

    # computing distances of input (r, g, b) to all samples
    distances = {}
    for sample in samples:
        row_sample = sample[1]
        column_sample = sample[0]
        r_sample = array_RGB_copy[row_sample, column_sample, 0]
        g_sample = array_RGB_copy[row_sample, column_sample, 1]
        b_sample = array_RGB_copy[row_sample, column_sample, 2]
        euclidean_distance = compute_euclidean_distance(np.array((r, g, b)).astype(float), np.array((r_sample, g_sample, b_sample)).astype(float))
        # print('sample', sample, r_sample, g_sample, b_sample, 'euclidean_distance', euclidean_distance)
        distances[euclidean_distance] = sample[2]
    # print('inside knn', distances)
    i_knn = 1
    classification = None
    knn_classifications = []
    for distance in sorted(distances.keys()):
        if i_knn > k:
            break
        i_knn = i_knn + 1
        if distance < actual_max_distance:
            knn_classifications.append(distances[distance])
    # print('set(knn_classifications)', set(knn_classifications))
    classification = 0
    if len(knn_classifications) > 0:
        classification = max(set(knn_classifications), key=knn_classifications.count)
        # print('actual_max_distance', actual_max_distance, 'some elements classified')        
    # else:
        # print('actual_max_distance', actual_max_distance, 'no elements classified')
    # print('knn_classifications', knn_classifications, 'and classification', classification)

    return classification

# create animation for k-nn classification
actual_samples = samples
# classify several times, using part of
# the samples, to visualized knn effect
# for sample in (samples):
#     actual_samples.append(sample)
#     actual_max_distance = min_distance
#     print('actual_samples', actual_samples, 'actual_max_distance', actual_max_distance)
    
for animation_step in range(animation_steps):

    # create array for classification
    array_classification = np.zeros((rows, columns)).flatten()

    # classify all pixels
    for i in range(len(array_R_flatten)):
        r = array_R_flatten[i]
        g = array_G_flatten[i]
        b = array_B_flatten[i]
        array_classification[i] = knn(actual_samples, r, g, b)
        # print('pixel', i, array_classification[i], 'with RGB', r, g, b)

    # display partial result in png animation
    output_figure_path = 'animation/scatterplot_' + str(figure_steps).zfill(6) + '.png'

    # create figure with 2 columns
    output_fig = plt.figure(figsize=(10, 4))
    input_ax = output_fig.add_subplot(121)
    scatterplot_ax = output_fig.add_subplot(122, projection='3d')
    
    n = len(actual_samples)
    input_ax.set_title(f'kNN (k$={k}$) result, {n} samples, max distance {int(actual_max_distance)}', fontsize=8)
    input_ax.set_xlim([0 - figure_border, columns + figure_border])
    input_ax.set_ylim([rows + figure_border, 0 - figure_border])
    input_ax.xaxis.set_tick_params(labelsize=5) 
    input_ax.yaxis.set_tick_params(labelsize=5)
    matplotlib.rc('xtick', labelsize=10) 
    matplotlib.rc('ytick', labelsize=20) 

    # draw input image with current classification
    image_classification = np.reshape(array_classification, (rows, columns))
    image_to_show = array_RGB_copy.copy()

    # get pixels for histogram and for classification
    for one_class in all_classes:

        if one_class != 0:
            image_to_show[:,:,0] = np.where(image_classification == one_class, 255 * colors[one_class][0], image_to_show[:,:,0])
            image_to_show[:,:,1] = np.where(image_classification == one_class, 255 * colors[one_class][1], image_to_show[:,:,1])
            image_to_show[:,:,2] = np.where(image_classification == one_class, 255 * colors[one_class][2], image_to_show[:,:,2])

        reds = array_R_flatten[array_classification == one_class].astype(float)
        greens = array_G_flatten[array_classification == one_class].astype(float)
        blues = array_B_flatten[array_classification == one_class].astype(float)

        scatterplot_ax.scatter(reds, greens, blues, marker='.', s=0.3, c=np.array(colors[one_class]).reshape(1,-1))
        scatterplot_ax.set_xlabel('red', fontsize=5)
        scatterplot_ax.xaxis.label.set_color('red')
        scatterplot_ax.xaxis.set_tick_params(labelsize=5)
        scatterplot_ax.set_ylabel('green', fontsize=5)
        scatterplot_ax.yaxis.label.set_color('green')
        scatterplot_ax.yaxis.set_tick_params(labelsize=5)
        scatterplot_ax.set_zlabel('blue', fontsize=5)
        scatterplot_ax.zaxis.label.set_color('blue')
        scatterplot_ax.zaxis.set_tick_params(labelsize=5)

        # clean up
        reds = None
        greens = None
        blues = None

    # input_ax.imshow(image_classification, cmap=default_colormap, vmin=0, vmax=colormap_vmax - 1) #, alpha=0.5)
    input_ax.imshow(image_to_show)

    # get samples position in the image
    for actual_sample in actual_samples:
        row_sample = actual_sample[1]
        column_sample = actual_sample[0]
        color_sample = colors[actual_sample[2]]
        input_ax.plot(column_sample, row_sample, marker='o', markersize=5, mew=1, mec='white', mfc=color_sample) # color=color_sample, 
    # output_fig.colorbar(im, ax=input_ax) #, orientation='horizontal', fraction=.1)

    scatterplot_ax.set_xlim([0, 255])
    scatterplot_ax.set_ylim([0, 255])
    scatterplot_ax.set_zlim([0, 255])
    scatterplot_ax.view_init(30, angle)
    scatterplot_ax.dist = dist
    # update distance of plot 
    dist = dist + dist_delta
    if (dist > max_dist) or (dist < min_dist):
        dist_delta = dist_delta * -1
    # update rotation angle of plot
    angle = angle + angle_delta
    if (angle > max_angle) or (angle < min_angle):
        angle_delta = angle_delta * -1
    # update knn max distance 
    actual_max_distance = actual_max_distance + step_distance
    if actual_max_distance > max_distance:
        actual_max_distance = max_distance

    # plot samples in scatterplot
    for marker_sample in actual_samples:
        row_sample = marker_sample[1]
        column_sample = marker_sample[0]
        r_sample = array_RGB_copy[row_sample, column_sample, 0]
        g_sample = array_RGB_copy[row_sample, column_sample, 1]
        b_sample = array_RGB_copy[row_sample, column_sample, 2]
        one_class = marker_sample[2]
        the_color = np.array(colors[one_class])
        scatterplot_ax.scatter(r_sample, g_sample, b_sample, marker='o', s=25, c=the_color.reshape(1,-1)) 
        scatterplot_ax.plot([r_sample, r_sample], [g_sample, g_sample], [0, b_sample], c=the_color, linewidth=0.5)
        scatterplot_ax.plot([r_sample, r_sample], [0, g_sample], [b_sample, b_sample], c=the_color, linewidth=0.5)
        scatterplot_ax.plot([0, r_sample], [g_sample, g_sample], [b_sample, b_sample], c=the_color, linewidth=0.5)

    # save partial results in animation        
    output_fig.savefig(output_figure_path, format='png', dpi=200)
    plt.tight_layout()
    plt.close()

    # clean up
    scatterplot_ax = None
    input_ax = None
    output_fig = None

    figure_steps = figure_steps + 1

# close dataset
dataset = None
