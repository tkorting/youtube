# this script allows to create a .mov file after crating png steps
rm -f hough-animation.mov
ffmpeg -f image2 -pattern_type glob -i "animation/animation-*.png" -r 25 -b 50000000 -filter:v "setpts=0.5*PTS" -an hough-animation.mov
