# this function assumes that input matrix is 2D
function mp = max_pooling(input_matrix, scale_factor)

  mp = zeros(size(input_matrix)(1)/scale_factor, 
             size(input_matrix)(2)/scale_factor);
   
  # apply max pooling operation
  for i = 1:size(mp)(1)
    for j = 1:size(mp)(2)
      submatrix = input_matrix((i-1)*scale_factor+1:(i*scale_factor), (j-1)*scale_factor+1:(j*scale_factor));
      mp(i, j) = max(max(submatrix));
    endfor
  endfor
  return

endfunction
