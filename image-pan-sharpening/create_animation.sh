# this script allows to create a .flv file after crating png steps (can be loaded in prezi)
rm -f animation/*.png

# run python with main file and create animation
python main.py
rm -f pan_sharpening.flv
ffmpeg -f image2 -pattern_type glob -i "animation/value_to_pan_*.png" -r 25 -b 50000000 -filter:v "setpts=0.5*PTS" -an pan_sharpening.flv
