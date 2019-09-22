# Subscribe to my channel, share and like my videos at
# http://youtube.com/tkorting
#
# Feel free to use and share this code.
#
# Thales Sehn Körting

function re = relu(input_matrix)

  # create 1D vector with all points in input_matrix
  vector_from_input_matrix = reshape(input_matrix, 1, prod(size(input_matrix)));
   
  # apply ReLU formula f(z) = max(0, z)
  re = max(0, max(vector_from_input_matrix));
  return

endfunction
