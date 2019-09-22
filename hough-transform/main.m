# Subscribe to my channel, share and like my videos at
# http://youtube.com/tkorting
#
# Feel free to use and share this code.
#
# Thales Sehn Körting

clear all;

# need to download package from https://octave.sourceforge.io/image/
# and install by pkg install image-x.yy.0.tar.gz
pkg load image

# need to download package from https://octave.sourceforge.io/geometry/
# and install by pkg install geometry-x.yy.0.tar.gz
pkg load geometry

# load graphics toolkit to allow creating plots 
# and save to file without display
graphics_toolkit gnuplot

# defining input parameters for the algorithm
input_image_name = 'input.png';
original_image = imread(input_image_name);
edge_image = edge(original_image, 'Canny');
theta_step = 1;
resampling = 1;
n_maximuns = 30;
display_debug = true;
make_animation = true;
[matrix_A, rhos_thetas_rankings] = hough_transform(edge_image, theta_step, resampling, n_maximuns, display_debug, make_animation);

# saving data for future uses, if needed
save matrix_A.mat matrix_A;
save rhos_thetas_rankings.mat rhos_thetas_rankings;
save edge_image.mat edge_image;
save original_image.mat original_image;
