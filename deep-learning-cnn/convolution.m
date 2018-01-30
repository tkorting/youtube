# this function assumes that input_matrix and weights_matrix are of the same size, and 2D
function conv = convolution(input_matrix, weights_matrix)

  # create 1D vectors with input and weights matrices
  input_vector = double(reshape(input_matrix, 1, prod(size(input_matrix))));
  weights_vector = double(reshape(weights_matrix, prod(size(weights_matrix)), 1));
  
  # make convolution
  conv = input_vector * weights_vector;
  return;

endfunction
