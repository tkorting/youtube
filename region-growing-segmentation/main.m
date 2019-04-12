clear all;
clf;
graphics_toolkit gnuplot

% constants
weight_mean = 1;
weight_new = 1;
T = 200;
w = 30;
h = 30;
c_start = 101;
r_start = 151;
filename = 'block.tif';
display_img = imread(filename);
display_img = display_img(c_start:c_start + w - 1, r_start:r_start + h - 1, :);
img = double(imread(filename));
img = img(c_start:c_start + w - 1, r_start:r_start + h - 1, :);

% create figure to save animation in files
graphics_toolkit gnuplot
figure(1, 'visible', 'off');
image(display_img)
axis([0 w + 1 0 h + 1]);
hold on;

% define seeds, except in the borders
r_seed = 3 + floor(rand(1) * (h - 3));
c_seed = 3 + floor(rand(1) * (w - 3));
r_seed = 4;
c_seed = 10;

r_region = [r_seed];
c_region = [c_seed];

r_plotted = [r_seed];
c_plotted = [c_seed];

plot(50, 50, 'k.');
plot(50, 51, 'r.');
plot(50, 52, 'rs');
legend('analyzed pixel', 'current pixel', 'pixel in region');

mean_pixels = [img(r_region, c_region, 1),  img(r_region, c_region, 2), img(r_region, c_region, 3)];
found_new_pixel = true;
plot_number = 10000;
while(found_new_pixel)
  found_new_pixel = false;
  for j = 1:length(r_region)
    r = r_region(j);
    c = c_region(j);
    
    min_distance = 255^3;
    r_new = r;
    c_new = c;
 
    % plotting central pixel
    plot(c, r, "k.");
    
    % testing homogeneity with neighbors in +
    for k = 1:4
      if (k == 1)
        neighbor_c = c + 1;
        neighbor_r = r;
      elseif (k == 2)
        neighbor_c = c - 1;
        neighbor_r = r;
      elseif (k == 3)
        neighbor_c = c;
        neighbor_r = r + 1;
      elseif (k == 4)
        neighbor_c = c;
        neighbor_r = r - 1;
        k = 1;
      end
      if (neighbor_c <= w && neighbor_c >= 1 &&
          neighbor_r <= h && neighbor_r >= 1 && 
          new_pixel(neighbor_c, neighbor_r, c_region, r_region))
        plot(neighbor_c, neighbor_r, "r.");

        repeated_frames = 1;
        if (new_pixel(neighbor_c, neighbor_r, c_plotted, r_plotted))
          for p = 1:repeated_frames
            plotname = ['animation/segmentation_t', num2str(plot_number), '.png'];
            print(plotname, '-dpng', '-r150');
            plot_number = plot_number + 1;
          end
          
          c_plotted = [c_plotted; neighbor_c];
          r_plotted = [r_plotted; neighbor_r];
        end
        
        pixel = [img(neighbor_r, neighbor_c, 1) img(neighbor_r, neighbor_c, 2) img(neighbor_r, neighbor_c, 3)];
        p1_minus_p2 = [mean_pixels(1) - img(neighbor_r, neighbor_c, 1), mean_pixels(2) - img(neighbor_r, neighbor_c, 2), mean_pixels(3) - img(neighbor_r, neighbor_c, 3)];
        distance = sqrt(sum(p1_minus_p2 .^ 2));
        title(['region mean of pixels (', num2str(floor(mean_pixels(1))), ';', num2str(floor(mean_pixels(2))), ';', num2str(floor(mean_pixels(3))), ') current pixel (', num2str(pixel(1)), ';', num2str(pixel(2)), ';', num2str(pixel(3)), ') and distance is ', num2str(distance)]);
        plot(neighbor_c, neighbor_r, "k.");

        if (distance < min_distance)
          r_new = neighbor_r;
          c_new = neighbor_c;
          min_distance = distance;
        end
      end;
    end;
  end

  % include all pixels with min_distance
  if (min_distance < T)

    for j = 1:length(r_region)
      r = r_region(j);
      c = c_region(j);
      
      % testing homogeneity with neighbors in +
      for k = 1:4
        if (k == 1)
          neighbor_c = c + 1;
          neighbor_r = r;
        elseif (k == 2)
          neighbor_c = c - 1;
          neighbor_r = r;
        elseif (k == 3)
          neighbor_c = c;
          neighbor_r = r + 1;
        elseif (k == 4)
          neighbor_c = c;
          neighbor_r = r - 1;
          k = 1;
        end
        if (neighbor_c <= w && neighbor_c >= 1 &&
            neighbor_r <= h && neighbor_r >= 1 && 
            new_pixel(neighbor_c, neighbor_r, c_region, r_region))
          p1_minus_p2 = [mean_pixels(1) - img(neighbor_r, neighbor_c, 1), mean_pixels(2) - img(neighbor_r, neighbor_c, 2), mean_pixels(3) - img(neighbor_r, neighbor_c, 3)];
          distance = sqrt(sum(p1_minus_p2 .^ 2));
          if (distance == min_distance)
            plot(neighbor_c, neighbor_r, "rs");
            c_region = [c_region; neighbor_c];
            r_region = [r_region; neighbor_r];
            found_new_pixel = true;

            mean_pixels(1) = (weight_mean * mean_pixels(1) + weight_new * img(neighbor_r, neighbor_c, 1)) / (weight_mean + weight_new);
            mean_pixels(2) = (weight_mean * mean_pixels(2) + weight_new * img(neighbor_r, neighbor_c, 2)) / (weight_mean + weight_new);
            mean_pixels(3) = (weight_mean * mean_pixels(3) + weight_new * img(neighbor_r, neighbor_c, 3)) / (weight_mean + weight_new);
          end
        end;
      end;
    end  
  
  end
  
  plot(c, r, "rs");
end
