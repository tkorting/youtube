function d = h_gauss(i, j, m, n)
	r = 0.05;
	a = i - m;
    b = j - n;
	
	d = exp(-0.5 * sqrt((a * a + b * b) / r));

