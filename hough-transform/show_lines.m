# this file can be used in case you produced all animation from octave, and want to display
# the main lines detected by the hough transform
# it will load matrices saved in main.m

load matrix_A.mat;
load rhos_thetas_rankings.mat;
load edge_image.mat;
load original_image.mat;

# display matrix_A as image
max_matrix_A = max(max(matrix_A));
min_matrix_A = min(min(matrix_A));
figure(1);
clf;
imshow(floor(matrix_A * 255 / max_matrix_A), gray);
print('matrix_A.png', '-dpng');

# display edge image
figure(2);
clf;
imshow(edge_image);
print('edges.png', '-dpng');

# display original image with lines
figure(3);
clf;
hold on;
imshow(edge_image)

colorstr = 'rgbmrgbmrgbmrgbmrgbmrgbmrgbmrgbmrgbmrgbmrgbmrgbmrgbmrgbmrgbmrgbmrgbmrgbmrgbm';
image_size = size(edge_image);
n_rows = image_size(1);
n_cols = image_size(2);

max_rhos = size(rhos_thetas_rankings)(1);
max_rhos = 10;
for line_id = 1:max_rhos
  rho = rhos_thetas_rankings(line_id, 1);
  theta = rhos_thetas_rankings(line_id, 2);

  x1 = 1;
  y1 = ceil((rho - x1 * cos(theta * pi / 180)) / sin(theta * pi / 180));
  x2 = n_cols;
  y2 = ceil((rho - x2 * cos(theta * pi / 180)) / sin(theta * pi / 180));
  drawEdge(y1, x1, y2, x2, 'color', colorstr(line_id), 'linewidth', 2);
endfor
