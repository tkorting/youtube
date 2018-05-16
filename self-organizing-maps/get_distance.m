function d = get_distance(a, b)
    c = a - b;
    r = c * c';
    d = sqrt(r);