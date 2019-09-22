# Subscribe to my channel, share and like my videos at
# http://youtube.com/tkorting
#
# Feel free to use and share this code.
#
# Thales Sehn Körting

function hy = hyperbolic_tangent(input_matrix)

  # create 1D vector with all points in input_matrix
  vector_from_input_matrix = reshape(input_matrix, 1, prod(size(input_matrix)));
   
  # apply hyperbolic tangent function as activation function
  hy = tanh(vector_from_input_matrix);
  return

endfunction
