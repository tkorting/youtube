# this algorithm trains a convolutional neural network with 2 classes, composed
# by 10 images 25x25x3 for each class
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
# inserting weights manually
f1(:, :, 1, 1) = [[-0.02368285  0.02538801 -0.01932165  0.25477728  0.20033413];
 [ 0.17023836  0.23319542  0.17084651  0.18203516  0.19656181];
 [ 0.10934857  0.14219394  0.21891357  0.20877141  0.33948281];
 [-0.09320439  0.01150889 -0.12876688  0.02094664  0.27527612];
 [-0.27320921 -0.34534562 -0.20150925 -0.09823161  0.02205109]];
 
f1(:, :, 1, 2) = [[-0.31706592  0.04795819 -0.07556906  0.16986656  0.26975524];
 [-0.10761818  0.00715791  0.07745448  0.2200532   0.26664451];
 [-0.08029876  0.10013724  0.2967321   0.39399466  0.17620243];
 [-0.10950112  0.23780781  0.23171085  0.09772879  0.07413235];
 [ 0.05228718  0.26159331  0.17723559  0.14940436  0.00057207]];

# for L2
N_filters_L2 = 3;
S_filters_L2 = 3;
f2 = stdnormal_rnd(S_filters_L2, S_filters_L2, N_filters_L1, N_filters_L2);
f2(:, :, 1, 1) = [[ 0.02460317 -0.13784343 -0.03827504];
 [-0.06958239  0.13236864 -0.27199936];
 [ 0.02728009  0.10636655 -0.11625343]];
f2(:, :, 2, 1) = [[ 0.12448616  0.07813687  0.18678382];
 [ 0.07477919  0.00665949 -0.03663819];
 [ 0.06285388 -0.17171675 -0.30839694]];
f2(:, :, 1, 2) = [[ 0.15481368  0.15831989  0.08463945];
 [ 0.05412359  0.07236765  0.03234851];
 [-0.16967589 -0.14269011 -0.17531261]];
f2(:, :, 2, 2) = [[ 0.12448616  0.07813687  0.18678382];
 [ 0.07477919  0.00665949 -0.03663819];
 [ 0.06285388 -0.17171675 -0.30839694]];
f2(:, :, 1, 3) = [[ 0.11697991  0.18117943  0.17169274];
 [ 0.28143591  0.2586731   0.05783887];
 [-0.07365174  0.11839788  0.30618799]];
f2(:, :, 2, 3) = [[ 0.18836974  0.07069078  0.13196954];
 [-0.11153162 -0.04575561  0.02877112];
 [-0.07397725 -0.1582658   0.04497239]];

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

image_paths = cellstr(['training-set/one-1.png';   'training-set/one-2.png';   'training-set/one-3.png'; 
                       'training-set/two-1.png'; 'training-set/two-2.png'; 'training-set/two-3.png']);
expected_classes = [1, 1, 1, 2, 2, 2];


debug = false;
for i = 5:5#size(image_paths)
  # training_cnn(char(image_paths(i, :)), cnn_metadata_file, expected_classes(i), debug);
  forward_cnn(char(image_paths(i, :)), cnn_metadata_file, debug);
endfor
