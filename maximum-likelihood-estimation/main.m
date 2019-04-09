clear all;

# defining class 1 parameters
class_1_axis_x = randn(100, 1);
class_1_axis_y = randn(100, 1);
class_1_axis_x = class_1_axis_x * 3;
class_1_axis_y = class_1_axis_y + 5;
mu_1_x = mean(class_1_axis_x);
mu_1_y = mean(class_1_axis_y);
sigma_1_x = std(class_1_axis_x);
sigma_1_y = std(class_1_axis_y);

# defining class 2 parameters
class_2_axis_x = randn(100, 1);
class_2_axis_y = randn(100, 1);
class_2_axis_x = class_2_axis_x - 4;
class_2_axis_y = class_2_axis_y - 3;
mu_2_x = mean(class_2_axis_x);
mu_2_y = mean(class_2_axis_y);
sigma_2_x = std(class_2_axis_x);
sigma_2_y = std(class_2_axis_y);

# defining class 3 parameters
class_3_axis_x = randn(100, 1);
class_3_axis_y = randn(100, 1);
class_3_axis_x = class_3_axis_x + 5;
class_3_axis_y = class_3_axis_y - 2;
class_3_axis_y = class_3_axis_y * 2.5;
mu_3_x = mean(class_3_axis_x);
mu_3_y = mean(class_3_axis_y);
sigma_3_x = std(class_3_axis_x);
sigma_3_y = std(class_3_axis_y);

# defining constants
limit_min = -10;
limit_max = 10;
K = 5;
ki = 0;

# first plot
clf;
hold on;
plot(class_1_axis_x, class_1_axis_y, 'ro');
plot(class_2_axis_x, class_2_axis_y, 'bo');
plot(class_3_axis_x, class_3_axis_y, 'go');
axis([limit_min limit_max limit_min limit_max]);

t = 1000;
filename = 'animation/mle-t-';
extension = '.png';
print([filename, num2str(t), extension], '-dpng');

vector_x = [];
vector_y = [];
# creating vector of points
for x = limit_min:0.5:limit_max
	for y = limit_min:0.5:limit_max
		my_x = x + rand() / 5;
		my_y = y + rand() / 5;
		vector_x = [vector_x, my_x];
		vector_y = [vector_y, my_y];
	end;
end;

n = rand(length(vector_x), 1); 
[garbage index] = sort(n); 
x_randomized = vector_x(index); 
y_randomized = vector_y(index);

# classifying all points in interval [limit_min, limit_maxi]
for i = 1:length(x_randomized)
	my_x = x_randomized(i);
	my_y = y_randomized(i);

	ki = ki + 1;
	if (mod(ki, K) == 0)
		print([filename, num2str(t), extension], '-dpng');
		ki = 0;
		t = t + 1;
	end

	p_1_x = 1 / (sigma_1_x * sqrt(2*pi)) * exp(-1/2 * ((my_x - mu_1_x)/sigma_1_x)^2);
	p_1_y = 1 / (sigma_1_y * sqrt(2*pi)) * exp(-1/2 * ((my_y - mu_1_y)/sigma_1_y)^2);
	p_1 = p_1_x * p_1_y;

	p_2_x = 1 / (sigma_2_x * sqrt(2*pi)) * exp(-1/2 * ((my_x - mu_2_x)/sigma_2_x)^2);
	p_2_y = 1 / (sigma_2_y * sqrt(2*pi)) * exp(-1/2 * ((my_y - mu_2_y)/sigma_2_y)^2);
	p_2 = p_2_x * p_2_y;

	p_3_x = 1 / (sigma_3_x * sqrt(2*pi)) * exp(-1/2 * ((my_x - mu_3_x)/sigma_3_x)^2);
	p_3_y = 1 / (sigma_3_y * sqrt(2*pi)) * exp(-1/2 * ((my_y - mu_3_y)/sigma_3_y)^2);
	p_3 = p_3_x * p_3_y;

	if (p_1 > p_2) && (p_1 > p_3)
		plot(my_x, my_y, 'r.');
	elseif (p_2 > p_1) && (p_2 > p_3)
		plot(my_x, my_y, 'b.');
	else
		plot(my_x, my_y, 'g.');
	end;
	axis([limit_min limit_max limit_min limit_max]);
end
