# Subscribe to my channel, share and like my videos at
# http://youtube.com/tkorting
#
# Feel free to use and share this code.
#
# Thales Sehn Körting

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
# expected_class: the expected class number for the input image
# debug: a flag to show/not show intermediate results

function train = training_cnn(input_image_path, cnn_metadata_file, expected_class, debug = false)

  if (debug)
    disp(['training with ', input_image_path]);
    disp(['loading metadata at ', cnn_metadata_file]);
    disp(['expected class: ', num2str(expected_class)]);
  endif
  
  # load input image
  input_image = imread(input_image_path);

  # compute input metadata
  image_size = size(input_image);
  Height = image_size(1);
  Width = image_size(2);
  N_bands = image_size(3);

  if (debug)
    # showing the input data
    figure(1)
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
  # apply the filters to the input image, followed by an activation function (ReLU)
  for r = delta_L1+1:Height-delta_L1-1
    for c = delta_L1+1:Width-delta_L1-1
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
      endfor   
    endfor
  endfor

  if (debug)
    # showing output of the first layer
    figure(2)
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
  # apply the filters to the tensors of the first layer, followed by an activation function (ReLU)
  for r = delta_L2+1:Height-delta_L2-1
    for c = delta_L2+1:Width-delta_L2-1
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
      endfor
    endfor
  endfor

  # showing output of the second layer
  if (debug)
    figure(3)
    colormap(gray)
    for i = 1:N_filters_L2
      subplot(1, N_filters_L2, i)
      imagesc(t2(:, :, i))
    endfor
  endif
  # the output tensors will be the input data for the next layer

  #################
  # the third layer -> max pooling (the same number of filters from previous layer)
  N_filters_L3 = N_filters_L2;
  # creating output from third layer: max pooling with scale factor
  t3 = zeros(Height/scale_factor, Width/scale_factor, N_filters_L3);
  # apply max pooling operation
  for b = 1:N_filters_L3
    t3(:, :, b) = max_pooling(t2(:, :, b), scale_factor);
  endfor

  # showing output of the third layer
  if (debug)
    figure(4)
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
  
  # create vector of expected output
  expected_output = zeros(1, N_classes);
  expected_output(expected_class) = 1;

  # compute loss function for the fifth layer
  loss = loss_function(expected_output, softmax_output);
disp('w5 before update');
w5
  # update weights at the fifth layer
  Neta = 0.95;
  corrected_softmax_output = zeros(1, N_classes);
  new_w5 = w5 - (expected_output - softmax_output) * Neta;
  for i = 1:N_classes
    corrected_softmax_output(i) = softmax(neurons_L4, i, new_w5);
  endfor
  w5 = new_w5;
disp('w5 after update');
w5
expected_output
softmax_output
corrected_softmax_output
  if (debug)
    expected_output
    softmax_output
    corrected_softmax_output
    
    disp(' ');
  endif
  
  save cnn_metadata_file N_filters_L1 S_filters_L1 f1 N_filters_L2 S_filters_L2 f2 N_filters_L3 scale_factor N_neurons_L4 w4 N_classes w5;
endfunction
