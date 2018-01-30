# this source code shows how a CNN is applied in a set of images
# composed by 10 images 25x25x3 for each class, representing digits
# from 0 to 9, the provided images here are only variations of
# 1's and 2's. the structure of the network is described above
# and contains weights defined randomly

clf;

# defining initial metadata for training function
# set example image to obtain metadata of input images
input_image = imread('training-set/one-1.png');
image_size = size(input_image);
Height = image_size(1);
Width = image_size(2);
N_bands = image_size(3);
# for L1
N_filters_L1 = 2;
S_filters_L1 = 5;
f1 = stdnormal_rnd(S_filters_L1, S_filters_L1, N_bands, N_filters_L1);

# for L2
N_filters_L2 = 3;
S_filters_L2 = 3;
f2 = stdnormal_rnd(S_filters_L2, S_filters_L2, N_filters_L1, N_filters_L2);

# for L3
N_filters_L3 = N_filters_L2;
scale_factor = 4;

# for L4
N_neurons_L4 = 4;
size_L4 = floor(Height/scale_factor) * floor(Width/scale_factor) * N_filters_L3;
w4 = stdnormal_rnd(N_neurons_L4, size_L4);

# for L5
N_classes = 10;
w5 = stdnormal_rnd(N_neurons_L4, N_classes);

# saving all parameters
cnn_metadata_file = 'metadata-cnn-one-x-two.mat';
save cnn_metadata_file N_filters_L1 S_filters_L1 f1 N_filters_L2 S_filters_L2 f2 N_filters_L3 scale_factor N_neurons_L4 w4 N_classes w5;

# defining training data
image_paths = cellstr(['training-set/one-1.png';  'training-set/one-2.png'; 'training-set/one-3.png'; 
                       'training-set/one-4.png';  'training-set/one-5.png'; 'training-set/one-6.png'; 
                       'training-set/one-7.png';  'training-set/one-8.png'; 'training-set/one-9.png'; 
                       'training-set/one-10.png'; 'training-set/two-1.png'; 'training-set/two-2.png'; 
                       'training-set/two-3.png';  'training-set/two-4.png'; 'training-set/two-5.png'; 
                       'training-set/two-6.png';  'training-set/two-7.png'; 'training-set/two-8.png'; 
                       'training-set/two-9.png';  'training-set/two-10.png']);
expected_classes = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2];

debug = true;
for i = 5:size(image_paths)
  forward_cnn(char(image_paths(i, :)), cnn_metadata_file, debug);
endfor