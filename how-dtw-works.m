A = [1, 3, 4, 9, 8, 2, 1, 5, 7, 3];
B = [1, 6, 2, 3, 0, 9, 4, 3, 6, 3];
eixo = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
figure(1), clf, hold on
plot(eixo, A, 'r-', 'linewidth', 2.0)
plot(eixo, B, 'b-', 'linewidth', 2.0), legend('time series A', 'time series B')
axis([0, 9])
