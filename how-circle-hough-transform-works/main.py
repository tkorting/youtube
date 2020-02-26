# Subscribe to my channel, share and like my videos at
# http://youtube.com/tkorting
#
# This source code is used to create two step-by-step
# animations about circle creation/detection using the 
# hough transform.
# Feel free to use and share this code.
#
# Thales Sehn Körting

# define constants
figure_border = 5
max_steps = 300

# importing libraries
# needed to open GeoTIFF files
from osgeo import gdal
from gdalconst import *
# needed to create plots
import matplotlib.pyplot as plt
# needed to manipulate arrays
import numpy as np
import math
import sys
import cv2

# animation for showing how to draw a circle
# basic circle equation
# (x - a)^2 + (y - b)^2 = r^2
# define constants (a, b) for center, and r for radius
# a = 12
# b = 24
# r = 10

# define set of valid x values
x = np.linspace(a - r, a + r, max_steps)
# compute y values based on x
y = np.sqrt(r * r - (x - a) * (x - a)) + b
y2 = -np.sqrt(r * r - (x - a) * (x - a)) + b

# concatenate y with y2 for the animation, and close circle
x = np.append(x, np.flip(x))
y = np.append(y, np.flip(y2))
x = np.append(x, x[0])
y = np.append(y, y[0])

# make animation
filename_in_animation = "animation/drawing_circle_"
columns = 40
rows = 40
step = 0
for i in range(0, x.shape[0]):
  output_fig = plt.figure(figsize=(5, 5))
  animation_ax = output_fig.add_subplot(111)
  animation_img = plt.plot(x[0:i], y[0:i], 'b-')
  plt.plot([a, x[i]], [b, y[i]], 'r-')
  plt.plot(a, b, 'g.')
  plt.legend(["circle",
             r"radius $r$", 
             r"center $(a,b)$"])
  plt.xlabel(r"$x$")
  plt.ylabel("$y$")
  # plot dashed lines of support, plus grid
  plt.plot([x[i], x[i]], [0.0, y[i]], color='black', linestyle='--', linewidth=0.5)
  plt.plot([0.0, x[i]], [y[i], y[i]], color='black', linestyle='--', linewidth=0.5)
  plt.grid(b=True, color='gray', linestyle='--', linewidth=0.5);
  # plot x, y values
  plt.plot(x[i], 0.0, 'k.')
  plt.text(x[i], -1.5, "{:.2f}".format(x[i]), fontsize=6)
  plt.plot(0.0, y[i], 'k.')
  plt.text(-3.5, y[i], "{:.2f}".format(y[i]), fontsize=6)
  # format and save graph
  animation_ax.set_xlim([0 - figure_border, columns + figure_border])
  animation_ax.set_ylim([0 - figure_border, rows + figure_border])
  plt.tight_layout()
  output_fig.savefig(filename_in_animation+str(step).zfill(6)+".png", format='png', dpi=200)
  plt.close()
  step = step + 1
  print(step)

# make animation of the detection using hough transform
filename = "example_image_2circles_notext.tif"

# load the dataset
try:
  dataset = gdal.Open(filename, GA_ReadOnly) 
except:
  print('error loading files')

# retrieve metadata
columns = dataset.RasterXSize
rows = dataset.RasterYSize

# get numpy array from raster, only first band
pixels_array = dataset.GetRasterBand(1).ReadAsArray().astype(float)
pixels_array_8bits = (255 * pixels_array / pixels_array.max()).astype(np.uint8)

# apply threshold
threshold = 200
binary_array = pixels_array_8bits.copy()
binary_array[binary_array > threshold] = 255
binary_array[binary_array <= threshold] = 0

# apply canny edge detector
edges_array = cv2.Canny(binary_array, 0, 100, 10)

# start animation, defining parameters
fixed_r = 155
velocity = 2
start_y = 158
start_x = 240
filename_in_animation = "animation/accumulator_"
accumulator_array = np.zeros((rows, columns))

# algorithm for accumulator, based on Wikipedia
# For each pixel(x,y)
#     For each radius r = 10 to r = 60 // the possible radius
#       For each theta t = 0 to 360  // the possible  theta 0 to 360 
#          a = x – r * cos(t * PI / 180); //polar coordinate for center
#          b = y – r * sin(t * PI / 180);  //polar coordinate for center 
#          A[a,b,r] +=1; //voting
#       end
#     end
#  end

# first part, without borders
v = 0
step = 0
first_y = np.linspace(0, start_y, max_steps)
first_x = np.linspace(0, start_x, max_steps)
for y, x in zip(first_y, first_x):
    # velocity of the video
    v = v + 1
    if v > velocity:
      v = 0

      output_fig = plt.figure(figsize=(8, 4))
      edges_ax = output_fig.add_subplot(121)
      # draw input image with actual position of x,y without border
      edges_ax.imshow(edges_array, cmap='gray')
      plt.title('Image edges')
      edges_ax.plot(x, y, 'r.')
      edges_ax.set_xlim([0 - figure_border, columns + figure_border])
      edges_ax.set_ylim([rows + figure_border, 0 - figure_border])
      # draw ancillary lines
      edges_ax.plot([x, x], [0.0, y], color='gray', linestyle='--', linewidth=0.5)
      edges_ax.plot([0.0, x], [y, y], color='gray', linestyle='--', linewidth=0.5)

      # draw partial accumulator
      accumulator_ax = output_fig.add_subplot(122)
      accumulator_ax.imshow(accumulator_array, cmap='gray')
      plt.title('Accumulator')
      accumulator_ax.set_xlim([0 - figure_border, columns + figure_border])
      accumulator_ax.set_ylim([rows + figure_border, 0 - figure_border])
      # save current image
      plt.tight_layout()
      output_fig.savefig(filename_in_animation+str(step).zfill(6)+".png", format='png', dpi=200)
      plt.close()
      step = step + 1
      print(step)

# create a list of only edges in the image, following the circle
v = 0
r = fixed_r
list_y = [start_y]
list_x = [start_x]
nexts_y = [ 0, +1, +1, +1,  0, -1, -1, -1,  0, +1, +2, +2, +2, +2, +2, +1,  0, -1, -2, -2, -2, -2, -2, -1]
nexts_x = [+1, +1,  0, -1, -1, -1,  0, +1, +2, +2, +2, +1,  0, -1, -2, -2, -2, -2, -2, -1,  0, +1, +2, +2]
visited_array = np.zeros_like(edges_array)
found_edge = True
while found_edge:
  y = list_y[len(list_y) - 1]
  x = list_x[len(list_x) - 1]
  found_edge = False
  for delta_y, delta_x in zip(nexts_y, nexts_x):
    next_y = y + delta_y
    next_x = x + delta_x
    if edges_array[next_y, next_x] != 0 and visited_array[next_y, next_x] == 0:
      list_y.append(next_y)
      list_x.append(next_x)
      visited_array[next_y, next_x] = 1
      found_edge = True
      break

# second/third parts, some edges with full circle animation
# and then only edges without full circle animation
max_circles = 30
circle = 0
for y, x in zip(list_y, list_x):
  circle = circle + 1
  for theta in range(0, 360):
    a = int(x - r * math.cos(theta * math.pi / 180))
    b = int(y - r * math.sin(theta * math.pi / 180))
    if a > 0 and a < columns and b > 0 and b < rows:
      accumulator_array[b, a] = accumulator_array[b, a] + 1
      L = accumulator_array.max()
      log_accumulator_array = accumulator_array.copy()
      if np.log(L) != 0.0:
        log_accumulator_array = L * np.log(1 + accumulator_array) / np.log(L)

      # velocity of the video
      v = v + 1
      if v > velocity:
        v = 0

        if circle < max_circles:
          output_fig = plt.figure(figsize=(8, 4))
          edges_ax = output_fig.add_subplot(121)
          # draw input image with actual position and radius
          edges_ax.imshow(edges_array, cmap='gray')
          plt.title('Image edges')
          edges_ax.plot([x, a], [y, b], 'r-', linewidth=0.5)
          edges_ax.plot(a, b, 'r+', linewidth=0.5)
          edges_ax.set_xlim([0 - figure_border, columns + figure_border])
          edges_ax.set_ylim([rows + figure_border, 0 - figure_border])
          # draw ancillary lines
          edges_ax.plot([x, x], [0.0, y], color='gray', linestyle='--', linewidth=0.5)
          edges_ax.plot([0.0, x], [y, y], color='gray', linestyle='--', linewidth=0.5)

          # draw partial accumulator
          accumulator_ax = output_fig.add_subplot(122)
          accumulator_ax.imshow(log_accumulator_array, cmap='hot')
          plt.title('Accumulator')
          accumulator_ax.plot(a, b, 'r+', linewidth=0.5)
          accumulator_ax.set_xlim([0 - figure_border, columns + figure_border])
          accumulator_ax.set_ylim([rows + figure_border, 0 - figure_border])
          # save current image
          plt.tight_layout()
          output_fig.savefig(filename_in_animation+str(step).zfill(6)+".png", format='png', dpi=200)
          plt.close()
          step = step + 1
          print(step)

  # do not draw partial circles
  if circle >= max_circles:
    # velocity of the video
    v = v + 1
    if v > velocity:
      v = 0

      output_fig = plt.figure(figsize=(8, 4))
      edges_ax = output_fig.add_subplot(121)
      # draw input image with actual position and radius
      edges_ax.imshow(edges_array, cmap='gray')
      plt.title('Image edges')
      # edges_ax.plot([x, a], [y, b], 'r-', linewidth=0.5)
      edges_ax.plot(x, y, 'r+', linewidth=0.5)
      edges_ax.set_xlim([0 - figure_border, columns + figure_border])
      edges_ax.set_ylim([rows + figure_border, 0 - figure_border])
      # draw ancillary lines
      edges_ax.plot([x, x], [0.0, y], color='gray', linestyle='--', linewidth=0.5)
      edges_ax.plot([0.0, x], [y, y], color='gray', linestyle='--', linewidth=0.5)

      # draw partial accumulator
      accumulator_ax = output_fig.add_subplot(122)
      accumulator_ax.imshow(log_accumulator_array, cmap='hot')
      plt.title('Accumulator')
      # accumulator_ax.plot(a, b, 'r+', linewidth=0.5)
      accumulator_ax.set_xlim([0 - figure_border, columns + figure_border])
      accumulator_ax.set_ylim([rows + figure_border, 0 - figure_border])
      # save current image
      plt.tight_layout()
      output_fig.savefig(filename_in_animation+str(step).zfill(6)+".png", format='png', dpi=200)
      plt.close()
      step = step + 1
      print(step)

dataset = None
