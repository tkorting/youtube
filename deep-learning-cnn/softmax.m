# Subscribe to my channel, share and like my videos at
# http://youtube.com/tkorting
#
# Feel free to use and share this code.
#
# Thales Sehn Körting

# this function assumes that input_vector and weights_matrix(:, class_number) are of the same size
function sm = softmax(input_vector, class_number, weights_matrix, bias = 0.0)

  # compute weighted sum at numerator
  numerator = exp(input_vector * weights_matrix(:, class_number) + bias);
  # compute weights sum at denominator
  denominator = 0.0;
  for i = 1:size(weights_matrix)(2)
    denominator += exp(input_vector * weights_matrix(:, i) + bias);
  endfor
  sm = numerator / denominator;
  return

endfunction
