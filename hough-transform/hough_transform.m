# Subscribe to my channel, share and like my videos at
# http://youtube.com/tkorting
#
# Feel free to use and share this code.
#
# Thales Sehn Körting

function [matrix_A, rhos_thetas_rankings] = hough_transform(edge_image, theta_step = 1, resampling = 1, n_maximuns = 10, display_debug = false, make_animation = false)

  # metadata
  if (display_debug == true)
    disp('* loading metadata');
  endif
  image_size = size(edge_image);
  n_rows = image_size(1);
  n_cols = image_size(2);
  n_bands = 1;
  band = 1;
  if (display_debug == true)
    disp('* edge metadata:');
    disp(['n_rows: ', num2str(n_rows)]);
    disp(['n_cols: ', num2str(n_cols)]);
  endif;

  # definitions of theta limits
  theta_min = -90;
  theta_max = +90;

  # create struct with theta possible indices
  if (display_debug == true)
    disp('* creating possible theta indices')
  endif

  counter = 1;
  theta_indices = struct();
  theta_indices_inverted = struct();
  for theta = theta_min:theta_step:theta_max
    theta_indices = setfield(theta_indices, num2str(theta), counter);
    theta_indices_inverted = setfield(theta_indices_inverted, num2str(counter), theta);
    counter = counter + 1;
  endfor

  # definitions of rho limits
  rho_min = -ceil(sqrt(n_rows^2 + n_cols^2));
  rho_max = -rho_min;
  theta_size = length(theta_min:theta_step:theta_max);
  rho_step = ceil((rho_max - rho_min) / theta_size);
  if (rho_step < 1.0)
    rho_step = 1;
  endif

  # create struct with rho possible indices
  if (display_debug == true)
    disp('* creating possible rho indices')
  endif
  counter = 1;
  rho_indices = struct();
  rho_indices_inverted = struct();
  for rho = rho_min:rho_step:rho_max
    rho_indices = setfield(rho_indices, num2str(rho), counter);
    rho_indices_inverted = setfield(rho_indices_inverted, num2str(counter), rho);
    counter = counter + 1;
  endfor

  # create cummulative matrix_A
  rows_in_A = numfields(rho_indices);
  columns_in_A = numfields(theta_indices);
  matrix_A = zeros(rows_in_A, columns_in_A);

  # creating cache of cos_theta and sin_theta
  cossines_theta = zeros(numfields(theta_indices), 1);
  sines_theta = zeros(numfields(theta_indices), 1);
  for theta = theta_min:theta_step:theta_max
    theta_index = getfield(theta_indices, num2str(theta));
    cossines_theta(theta_index) = cos(theta * pi / 180);
    sines_theta(theta_index) = sin(theta * pi / 180);
  endfor

  if (display_debug == true)
    figure(4);
    max_pixel = max(max(edge_image));
    imshow(edge_image * 255 / max_pixel, gray);
  endif

  # populate matrix_A
  if (display_debug == true)
    disp('* populating cummulative matrix_A')
  endif
  animation_id = 0;
  colormap(gray);
  for row = 1:resampling:n_rows
    for column = 1:resampling:n_cols
      if (edge_image(row, column, band) > 0)
        for theta = theta_min:theta_step:theta_max
          theta_index = getfield(theta_indices, num2str(theta));
          cos_theta = cossines_theta(theta_index);
          sin_theta = sines_theta(theta_index);
          rho = row * cos_theta + column * sin_theta;
          rho = ceil(rho);
          while (isfield(rho_indices, num2str(rho)) == false)
            if (rho < rho_min)
              rho = rho + 1;
            else
              rho = rho - 1;
            endif
          endwhile
          rho_index = getfield(rho_indices, num2str(rho));
          matrix_A(rho_index, theta_index) = matrix_A(rho_index, theta_index) + 1;

          if (make_animation)
            # print when edge is found
            figure(10, 'visible', 'off');
            clf;
            subplot(1, 2, 2);
            imagesc(edge_image*255);
            axis([0 n_cols + 1 0 n_rows + 1]);
            hold on;

            x1 = 1;
            y1 = ceil((rho - x1 * cos(theta * pi / 180)) / sin(theta * pi / 180));
            x2 = n_cols;
            y2 = ceil((rho - x2 * cos(theta * pi / 180)) / sin(theta * pi / 180));
            drawEdge(y1, x1, y2, x2, 'color', 'g', 'linewidth', 2);
            plot(column, row, 'yo', 'linewidth', 2);
            axis off;
            #refresh();

            subplot(1, 2, 1);
            max_matrix_A = max(max(matrix_A));
            if (max_matrix_A < 1)
              max_matrix_A = 1;
            endif
            imagesc(floor(matrix_A * 255 / max_matrix_A));
            colormap(gray);
            hold on;
            axis off;
            plot(theta_index, rho_index, 'rx');
            refresh();

            output_filename = sprintf('animation/animation-%09d.png', animation_id);
            print(output_filename, '-dpng', '-S900,300');
            animation_id = animation_id + 1;
          endif

        endfor
      endif

      if (make_animation)
        # print when no edge is found
        figure(10, 'visible', 'off');
        clf;
        subplot(1, 2, 2);
        imagesc(edge_image*255);
        axis([0 n_cols + 1 0 n_rows + 1]);
        axis off;
        hold on;

        plot(column, row, 'ro', 'linewidth', 2);

        subplot(1, 2, 1);
        max_matrix_A = max(max(matrix_A));
        if (max_matrix_A < 1)
          max_matrix_A = 1;
        endif
        imagesc(floor(matrix_A * 255 / max_matrix_A));
        colormap(gray);
        axis off;
        refresh();

        output_filename = sprintf('animation/animation-%09d.png', animation_id);
        print(output_filename, '-dpng', '-S900,300');
        animation_id = animation_id + 1;
      endif
    endfor
    if (display_debug == true)
      disp([num2str(row), '.']);

      figure(5);
      max_matrix_A = max(max(matrix_A));
      if (max_matrix_A < 1)
        max_matrix_A = 1;
      endif
      imshow(floor(matrix_A * 255 / max_matrix_A), gray);
      refresh();
      fflush(stdout);
    endif
  endfor

  # create output values for rhos, thetas and rhos_thetas_rankings
  rhos_thetas_rankings = [];
  tmp_matrix_A = matrix_A;
  for n=1:n_maximuns
    max_matrix_A = max(max(tmp_matrix_A));
    only_max_matrix_A = tmp_matrix_A == max_matrix_A;
    [max_rho, max_theta] = find(only_max_matrix_A);
    for counter=1:length(max_rho)
      rho = getfield(rho_indices_inverted, num2str(max_rho(counter)));
      theta = getfield(theta_indices_inverted, num2str(max_theta(counter)));
      rhos_thetas_rankings = [rhos_thetas_rankings; rho, theta, n];
    endfor
    tmp_matrix_A = tmp_matrix_A .* not(only_max_matrix_A);
  endfor

endfunction
