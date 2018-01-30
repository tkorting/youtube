# this is a very basic example of a convolutional neural network - CNN
# parameters:
# input_image_path: the path to the file with input image
# cnn_metadata_file: the path to the file containing all variables for configuring CNN, which are:
#   N_filters_L1: number of filters at the first layer
#   S_filters_L1: size of filters at the first layer
#   f1: the actual weights of filters at the first layer
#   N_filters_L2: number of filters at the second layer
#   S_filters_L2: size of filters at the second layer
#   f2: the actual weights of filters at the second layer
#   N_filters_L3: will be the same as N_filters_L3 since the third layer is max pooling
#   scale_factor: the scale factor of the third (max pooling) layer
#   N_neurons_L4: number of filters at the fourth layer (fully connected)
#   w4: the actual weights of the fourth layer (fully connected)
#   N_classes: the number of classes to be the output of fifth layer (softmax)
#   w5: the actual weights of the fifth layer (softmax)
# debug: a flag to show/not show intermediate results
#
# fwd: the output will be the predicted class (e.g. N_classes = 4 and predicted class is 2, fwd = [0 1 0 0])
function fwd = forward_cnn(input_image_path, cnn_metadata_file, debug = false)

  if (debug)
    disp(['predicting class for ', input_image_path]);
    disp(['loading metadata at ', cnn_metadata_file]);
  endif
  
  # load input image
  input_image = imread(input_image_path);
  # limits = [min(min(min(input_image))) max(max(max(input_image)))];

  # compute input metadata
  image_size = size(input_image);
  Height = image_size(1);
  Width = image_size(2);
  N_bands = image_size(3);

  debug_figure = 10;
  if (debug)
    # showing the input data
    figure(debug_figure);
    debug_figure = debug_figure + 1;
    colormap(gray)
    for i = 1:N_bands
      subplot(1, N_bands, i)
      imagesc(input_image(:, :, i))
    endfor
  endif

  # load metadata of CNN
  load cnn_metadata_file;

  #################
  # the first layer
  delta_L1 = floor(S_filters_L1 / 2);
  # creating tensors for the first layer
  t1 = zeros(Height, Width, N_filters_L1);

  animation_figure = 1;
  # graphics_toolkit gnuplot
  # figure(animation_figure, 'visible', 'off');
  step_animation_L1 = 1;
  animation_size = "-S1024,768";

  # apply the filters to the input image, followed by an activation function (ReLU)
  disp('L1');
  for r = delta_L1+1:Height-delta_L1-1
    disp(['  row ', num2str(r)]);
    fflush(stdout);
    for c = delta_L1+1:Width-delta_L1-1
      clf;
      for i = 1:N_bands
        subplot(max(N_bands, N_filters_L1), 2, (i*2)-1);
        graph_title = ['convolution in band ', num2str(i), ' at position ', num2str(r), ',', num2str(c)];
        draw_current_state(animation_figure, input_image(:, :, i), r, c, S_filters_L1, 'c', graph_title);
      endfor
      for f = 1:N_filters_L1
        f1_results = [];
        # apply f1 (filters of first layer) to all input bands
        for b = 1:N_bands
          partial_result = artificial_neuron(
            input_image(r-delta_L1:r+delta_L1, c-delta_L1:c+delta_L1, b), 
            f1(:, :, b, f));
          f1_results = [f1_results, partial_result];
        endfor
        t1(r, c, f) = relu(f1_results); 

        # plot tensors under construction
        colormap(gray);
        subplot(max(N_bands, N_filters_L1), 2, (f*2));
        limits = [0, 1866.563; 0, 872.331]; # t1
        imagesc(t1(:, :, f), limits(f, :));
        grid off; axis off;
      endfor
      output_filename = ['animation/animation_L1_', num2str(step_animation_L1), '.png'];
      step_animation_L1 = step_animation_L1 + 1;
      print(output_filename, animation_size);
    endfor
  endfor
  for f = 1:N_filters_L1
    disp(['limits for t1: ', num2str(max(max(max(t1(:, :, f)))))]);
  endfor
  
  if (debug)
    # showing output of the first layer
    figure(debug_figure);
    debug_figure = debug_figure + 1;
    colormap(gray)
    for i = 1:N_filters_L1
      subplot(1, N_filters_L1, i)
      imagesc(t1(:, :, i))
    endfor
  endif
  # the output tensors will be the input data for the next layer

  ##################
  # the second layer
  delta_L2 = floor(S_filters_L2 / 2);
  # creating tensors for the second layer
  t2 = zeros(Height, Width, N_filters_L2);
  
  animation_figure = 2;
  step_animation_L2 = 1;

  # apply the filters to the tensors of the first layer, followed by an activation function (ReLU)
  disp('L2');
  for r = delta_L2+1:Height-delta_L2-1
    disp(['  row ', num2str(r)]);
    fflush(stdout);
    for c = delta_L2+1:Width-delta_L2-1
      clf;
      for i = 1:N_filters_L1
        subplot(max(N_filters_L2, N_filters_L1), 2, (i*2)-1);
        graph_title = ['convolution in tensor ', num2str(i), ' at position ', num2str(r), ',', num2str(c)];
        draw_current_state(animation_figure, t1(:, :, i), r, c, S_filters_L2, 'c', graph_title);
      endfor
      for f = 1:N_filters_L2
        f2_results = [];
        # apply f2 (filters of second layer) to all input tensors from first layer
        for b = 1:N_filters_L1
          partial_result = artificial_neuron(
            t1(r-delta_L2:r+delta_L2, c-delta_L2:c+delta_L2, b), 
            f2(:, :, b, f));
          f2_results = [f2_results, partial_result];
        endfor
        t2(r, c, f) = relu(f2_results);
        
        # plot tensors under construction
        colormap(gray)
        subplot(max(N_filters_L2, N_filters_L1), 2, (f*2));
        limits = [0, 322.776; 0, 962.384; 0, 2476.059]; # t2
        imagesc(t2(:, :, f), limits(f, :));
        grid off; axis off;
      endfor
      output_filename = ['animation/animation_L2_', num2str(step_animation_L2), '.png'];
      step_animation_L2 = step_animation_L2 + 1;
      print(output_filename, animation_size);
    endfor
  endfor
  for f = 1:N_filters_L2
    disp(['limits for t2: ', num2str(max(max(max(t2(:, :, f)))))]);
  endfor

  # showing output of the second layer
  if (debug)
    figure(debug_figure);
    debug_figure = debug_figure + 1;
    colormap(gray)
    for i = 1:N_filters_L2
      subplot(1, N_filters_L2, i)
      imagesc(t2(:, :, i))
    endfor
  endif
  # the output tensors will be the input data for the next layer

  #################
  # the third layer ->r -> fully connected layer max pooling (the same number of filters from previous layer)
  N_filters_L3 = N_filters_L2;
  # creating output from third layer: max pooling with scale factor
  t3 = zeros(Height/scale_factor, Width/scale_factor, N_filters_L3);

  animation_figure = 3;
  step_animation_L3 = 1;

  # apply pooling with max operation
  disp('L3');
  pooling_r = 1;
  for r = 1:scale_factor:size(t2)(1)-scale_factor
    pooling_c = 1;
    disp(['  row ', num2str(r)]);
    fflush(stdout);
    for c = 1:scale_factor:size(t2)(2)-scale_factor
      clf;
      for i = 1:N_filters_L2
        subplot(max(N_filters_L3, N_filters_L3), 2, (i*2)-1);
        graph_title = ['pooling in tensor ', num2str(i), ' at position ', num2str(r), ',', num2str(c)];
        draw_current_state(animation_figure, t2(:, :, i), r, c, scale_factor, 'p', graph_title);
      endfor
      for b = 1:N_filters_L3
        t3(pooling_r, pooling_c, b) = max(max(t2(r:r+scale_factor-1, c:c+scale_factor-1, b)));

        # plot tensors under construction
        colormap(gray)
        subplot(max(N_filters_L3, N_filters_L3), 2, (b*2));
        limits = [0, 322.776; 0, 962.384; 0, 2476.059]; # t3
        imagesc(t3(:, :, b), limits(b, :));
        grid off; axis off;
      endfor
      output_filename = ['animation/animation_L3_', num2str(step_animation_L3), '.png'];
      step_animation_L3 = step_animation_L3 + 1;
      print(output_filename, animation_size);
  
      pooling_c = pooling_c + 1;
    endfor
    pooling_r = pooling_r + 1;
  endfor
  for b = 1:N_filters_L3
    disp(['limits for t3: ', num2str(max(max(max(t3(:, :, b)))))]);
  endfor

  
  # showing output of the third layer
  if (debug)
    figure(debug_figure);
    debug_figure = debug_figure + 1;
    colormap(gray)
    for i = 1:N_filters_L3
      subplot(1, N_filters_L3, i)
      imagesc(t3(:, :, i))
    endfor
  endif
  
  ##################
  # the fourth layer -> fully connected layer
  x = reshape(t3(:, :, :), 1, prod(size(t3)));
  # create the neurons at the fourth layer
  neurons_L4 = zeros(1, N_neurons_L4);
  # compute values for neurons at the fourth layer, using hyperbolic tangent as activation function
  for i = 1:N_neurons_L4
    neurons_L4(i) = hyperbolic_tangent(artificial_neuron(x, w4(i, :)));
  endfor

  #################
  # the fifth layer -> the softmax to output class membership
  # create the neurons at the fifth layer
  softmax_output = zeros(1, N_classes);
  # compute values for neurons at layer 5
  for i = 1:N_classes
    softmax_output(i) = softmax(neurons_L4, i, w5);
  endfor
    
  if (debug)
    softmax_output
    
    disp(' ');
  endif
  
  fwd = softmax_output;
  return
endfunction
