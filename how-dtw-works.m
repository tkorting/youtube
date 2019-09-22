# Subscribe to my channel, share and like my videos at
# http://youtube.com/tkorting
#
# This source code is used to create a step-by-step
# animation about image enhancement. Feel free to 
# use and share this code.
#
# Thales Sehn Körting

A = [1, 3, 4, 9, 8, 2, 1, 5, 7, 3];
B = [1, 6, 2, 3, 0, 9, 4, 3, 6, 3];
dtw_axis = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
figure(1), clf, hold on
plot(dtw_axis, A, 'r-', 'linewidth', 2.0)
plot(dtw_axis, B, 'b-', 'linewidth', 2.0), legend('time series A', 'time series B')
axis([0, 9])
