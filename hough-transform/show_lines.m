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

#  x1 = 1;
#  y1 = 1;
#  x2 = 1;
#  y2 = 1;
#  flag_can_stop_1 = false;
#  flag_can_stop_2 = false;
#  for x = 1:n_cols
#    if (flag_can_stop_1 && flag_can_stop_2)
#      continue;
#    endif
#    if (x1 == 1 && y1 == 1)
#      y = ceil((rho - x * cos(theta * pi / 180)) / sin(theta * pi / 180));
#      if (y > 0 && y <= n_rows)
#        if (edge_image(y, x) > 0)
#          x1 = x;
#          y1 = y;
#          flag_can_stop_1 = true;
#        endif
#      endif
#    endif
#    if (x2 == 1 && y2 == 1)
#      x_end = n_cols - x;
#      y_end = ceil((rho - x_end * cos(theta * pi / 180)) / sin(theta * pi / 180));
#      if (y_end > 0 && y_end <= n_rows)
#        if (edge_image(y_end, x_end) > 0)
#          x2 = x_end;
#          y2 = y_end;
#          flag_can_stop_2 = true;
#        endif
#      endif
#    endif
#  endfor
#
#  drawEdge(y1, x1, y2, x2, 'color', colorstr(line_id), 'linewidth', 2);
#endfor 
#print('lines.png', '-dpng');