clear all;

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
