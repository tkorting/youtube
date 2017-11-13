clear all;

if (false)
  input_image_name = '/home/tkorting/Documentos/inpe/imagens/carolina/sjc-quickbird.png';
  original_image = imread(input_image_name);

  # create edge image
  [dx, dy] = gradient(mean(original_image, 3));
  edge_image = sqrt(double(dx .* dx + dy .* dy));

  # apply threshold to create binary edge image
  edge_image = (edge_image > 40);
endif

if (false)
  input_image_name = 'raster-49x49.tif';
  original_image = imread(input_image_name);
  edge_image = original_image;
endif

if (false)
  input_image_name = 'input_images/pan.tif';
  original_image = imread(input_image_name);
  #edge_image = edge(original_image, "Canny");
  load 'edges/edge_image_pan.mat';
endif

if (true)
  input_image_name = 'input_images/rectangle_rotacioned.png';
  original_image = imread(input_image_name);
  #edge_image = edge(original_image, "Canny");
  load 'edges/edge_image_rectangle.mat';
endif

theta_step = 1;
resampling = 1;
n_maximuns = 30;
display_debug = false;
make_animation = false;
[matrix_A, rhos_thetas_rankings] = hough_transform(edge_image, theta_step, resampling, n_maximuns, display_debug, make_animation);

save matrix_A.mat matrix_A;
save rhos_thetas_rankings.mat rhos_thetas_rankings;
save edge_image.mat edge_image;
save original_image.mat original_image;