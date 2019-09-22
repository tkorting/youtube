# Subscribe to my channel, share and like my videos at
# http://youtube.com/tkorting
#
# This source code is used to create a step-by-step
# animation about image enhancement. Feel free to 
# use and share this code.
#
# Thales Sehn Körting

# this function assumes that input_vector and weights_vector are of the same size, and 1D
function an = artificial_neuron(input_vector, weights_vector, bias = 0)

  # compute weighted sum
  an = convolution(input_vector, weights_vector) + bias;
  return
  
endfunction
