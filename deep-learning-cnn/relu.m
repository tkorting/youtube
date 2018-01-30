function re = relu(input_matrix)

  # create 1D vector with all points in input_matrix
  vector_from_input_matrix = reshape(input_matrix, 1, prod(size(input_matrix)));
   
  # apply ReLU formula f(z) = max(0, z)
  re = max(0, max(vector_from_input_matrix));
  return

endfunction
