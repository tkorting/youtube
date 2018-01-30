# this function assumes that input_vector and weights_vector are of the same size, and 1D
function an = artificial_neuron(input_vector, weights_vector, bias = 0)

  # compute weighted sum
  an = convolution(input_vector, weights_vector) + bias;
  return
  
endfunction
