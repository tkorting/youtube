# import libraries
from osgeo import gdal
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# gdal constants
from gdalconst import *

# inform to use GDAL exceptions
gdal.UseExceptions()

from matplotlib.colors import ListedColormap, BoundaryNorm

# compute the distance in the SLIC space given:
# - two pixels as 5-tuple (R, G, B, x, y)
# - the expected compactness, m [1, 20]
# - the size S (grid interval expected)
def distance_slic(pixel_k, pixel_i, m, S):
    # compute the euclidian distance in RGB space between pixels k and i
    # in the original algorithm, the CIE-L*a*b color space is used
    d_rgb = math.sqrt( (pixel_k[0] - pixel_i[0]) ** 2 + 
                       (pixel_k[1] - pixel_i[1]) ** 2 + 
                       (pixel_k[2] - pixel_i[2]) ** 2)
    # compute the euclidian distance in the row/column space between pixels k and i
    d_xy = math.sqrt( (pixel_k[3] - pixel_i[3]) ** 2 + 
                      (pixel_k[4] - pixel_i[4]) ** 2)
    final_distance = d_rgb + m * d_xy / S
    # print ('d_rgb:', d_rgb, 'd_xy:', d_xy, 'final distance:', final_distance)
    return final_distance

# return a default color in range 0-1000
def get_color(k, K):
    color_vector = matplotlib.cm.get_cmap('Spectral')
    return color_vector(k / K)

# print centers of clusters
def plot_clusters(array, clusters, K, S, output_figure = ''):
    fig = plt.figure(figsize = (8, 6))
    plt.imshow(array, vmin=0, vmax=255)
    for k in range(K):
        # plot bounding box
        center_x = clusters[k, 3]
        center_y = clusters[k, 4]
        x = [center_x - S, center_x + S, center_x + S, center_x - S, center_x - S]
        y = [center_y - S, center_y - S, center_y + S, center_y + S, center_y - S]
        ax = fig.add_subplot(111)
        cluster_color = get_color(k, K)
        # cluster_color = (clusters[k, 0], clusters[k, 1], clusters[k, 2], 1.0)
        ax.fill(x, y, color=cluster_color, fill = None, linewidth=1, alpha = 0.5)
        # plot center
        # plt.plot(center_x, center_y, color=cluster_color, marker='.')
        plt.scatter(center_x, center_y, s = 35, facecolors=cluster_color, edgecolors='white', linewidth=1, alpha = 0.75)
        # adjust image
        (rows, columns, bands) = array.shape
        plt.xlim([0 - S, columns + S])
        plt.ylim([0 - S, rows + S])

    if output_figure != '':
        plt.savefig(output_figure, format='png', dpi=1000)
    else:
        plt.show()

def plot_slic(array, clusters, K, S, output_figure = ''):
    fig = plt.figure(figsize=(8, 6))
    # create colormap based on cluster RGB centers
    slic_colormap = []
    for c in clusters:
        slic_colormap.append((c[0], c[1], c[2], 1.0))
    slic_listed_colormap = ListedColormap(slic_colormap)
    slic_norm = BoundaryNorm(range(K), K)
    plt.imshow(array, norm=slic_norm, cmap=slic_listed_colormap)
    # adjust image
    (rows, columns) = array.shape
    plt.xlim([0 - S, columns + S])
    plt.ylim([0 - S, rows + S])

    if output_figure != '':
        plt.savefig(output_figure, format='png', dpi=1000)
    else:
        plt.show()

# open dataset
filename = "slic_test.tif"
dataset = gdal.Open(filename, GA_ReadOnly)

# retrieve metadata from raster
rows = dataset.RasterYSize
columns = dataset.RasterXSize
N = rows * columns
bands = dataset.RasterCount

# define the number of regions to split the image into
set_of_K = (400, 1200)
# define compactness constant
m = 10

for K in set_of_K:
    # compute other constants
    size = N / K
    S = math.sqrt(size)

    # get RGB numpy arrays
    array_R = dataset.GetRasterBand(1).ReadAsArray() / 255
    array_G = dataset.GetRasterBand(2).ReadAsArray() / 255
    array_B = dataset.GetRasterBand(3).ReadAsArray() / 255
    array_RGB = np.zeros([array_R.shape[0], array_R.shape[1], 3])
    array_RGB[:,:,0] = array_R
    array_RGB[:,:,1] = array_G
    array_RGB[:,:,2] = array_B

    # print some metadata
    print ("SLIC test")
    print ("image metadata:")
    print (rows, "rows x", columns, "columns x", bands, "bands")
    print (K, "expected divisions")
    print (S, "is the value of S")

    # compute initial clusters
    # the 5 positions are:
    # 1-R, 2-G, 3-B, 4-x, 5-y
    # in the original algorithm 1-L, 2-a, 3-b (the CIE-L*a*b color space)
    C = np.zeros((K, 5))

    # define center of K clusters (x, y)
    k = 0
    for y in range(math.floor(S / 2), rows, math.floor(rows / math.sqrt(K))):
        for x in range(math.floor(S / 2), columns, math.floor(columns / math.sqrt(K))):
            if k >= K:
                continue
            C[k, 0] = array_R[y, x]
            C[k, 1] = array_G[y, x]
            C[k, 2] = array_B[y, x]
            C[k, 3] = x
            C[k, 4] = y
            k = k + 1

    # set SLIC matrix
    array_SLIC = np.ones_like(array_R)

    t = 0
    plot_clusters(array_RGB, C, K, S, 'animation/K' + str(K) + '_cluster_limits_t' + str(t) + '.png')

    # compute superpixels matrix
    array_superpixels = np.zeros((N, 5))
    i = 0
    for y in range(0, rows):
        for x in range(0, columns):
            array_superpixels[i, 0] = array_R[y, x]
            array_superpixels[i, 1] = array_G[y, x]
            array_superpixels[i, 2] = array_B[y, x]
            array_superpixels[i, 3] = x
            array_superpixels[i, 4] = y
            i = i + 1


    # run SLIC k-means
    error_threshold = 5
    residual_error = error_threshold + 1
    i = 0
    max_i = 20
    while residual_error > error_threshold:
        # set SLIC matrix
        array_SLIC = np.ones_like(array_R)
        # define no data as K + 100 value
        array_SLIC *= (K * 100)

        print ("iteration", i)
        residual_error = 0.0
        # assign the best matching pixels from a 2S × 2S square neighborhood
        # around the cluster center according to the distance measure
        for k in range(K):
            center_x = C[k, 3]
            center_y = C[k, 4]
            left_y_limit = max(0, math.floor(center_y - S))
            right_y_limit = min(rows, math.floor(center_y + S))
            left_x_limit = max(0, math.floor(center_x - S))
            right_x_limit = min(columns, math.floor(center_x + S))
            print ("cluster", k, "limits y", left_y_limit, "to", right_y_limit, "and x", left_x_limit, "to", right_x_limit)
            for y in range(left_y_limit, right_y_limit):
                for x in range(left_x_limit, right_x_limit):
                    # print("checking around cluster", k, "y (row)", y, "x (column)", x)
                    distances_to_clusters = np.zeros(K)
                    for k1 in range(K):
                        pixel_k = np.array([C[k1, 0], C[k1, 1], C[k1, 2], C[k1, 3], C[k1, 4]])
                        pixel_i = np.array([array_R[y, x], array_G[y, x], array_B[y, x], x, y])
                        distances_to_clusters[k1] = distance_slic(pixel_k, pixel_i, m, S)
                    if np.argmin(distances_to_clusters) == k:
                        array_SLIC[y, x] = k
                    # print("  distances_to_clusters", distances_to_clusters)
                    # print("  array_SLIC", array_SLIC)
        # compute new cluster centers and residual error E
        for k in range(K):
            center_R = C[k, 0]
            center_G = C[k, 1]
            center_B = C[k, 2]
            center_x = C[k, 3]
            center_y = C[k, 4]
            new_center = np.zeros(5)
            total_in_k = 0
            for j in range(N):
                x = int(array_superpixels[j, 3])
                y = int(array_superpixels[j, 4])
                if array_SLIC[y, x] == k:
                    new_center = new_center + array_superpixels[j, :]
                    total_in_k = total_in_k + 1
            if total_in_k > 0:
                print("updating k", k, "old center", C[k, :], "new center", new_center / total_in_k, "total_in_k", total_in_k)
                new_center = new_center / total_in_k
                partial_error = C[k, :] - new_center
                residual_error = residual_error + math.sqrt(partial_error.dot(partial_error.transpose()))
                C[k, :] = new_center

        t = t + 1
        # plot intermediate clusters and slic
        plot_clusters(array_RGB, C, K, S, 'animation/K' + str(K) + '_cluster_limits_t' + str(t) + '.png')
        plot_slic(array_SLIC, C, K, S, 'animation/K' + str(K) + '_partial_slic_t' + str(t) + '.png')

        print ("residual error is", residual_error, "at iteration", i)
        i = i + 1
        # to avoid infinite loop
        if i > max_i:
            residual_error = error_threshold

    # make final segmentation
    # set SLIC matrix
    array_SLIC = np.ones_like(array_R)
    # define no data as K + 100 value
    array_SLIC *= (K * 100)
    # iterate again
    for j in range(N):
        x = int(array_superpixels[j, 3])
        y = int(array_superpixels[j, 4])
        distances_to_clusters = np.zeros(K)
        for k in range(K):
            pixel_k = np.array([C[k, 0], C[k, 1], C[k, 2], C[k, 3], C[k, 4]])
            pixel_i = array_superpixels[j, :]
            distances_to_clusters[k] = distance_slic(pixel_k, pixel_i, m, S)
        array_SLIC[y, x] = np.argmin(distances_to_clusters)

    # print("  array_SLIC", array_SLIC)
    plot_slic(array_SLIC, C, K, S, 'animation/K' + str(K) + '_final_slic_t.png')

# close dataset
dataset = None
