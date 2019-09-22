# Subscribe to my channel, share and like my videos at
# http://youtube.com/tkorting
#
# Feel free to use and share this code.
#
# Thales Sehn Körting

# run octave with main file
octave main.m

# call ffmpeg to create animation from set of files
ffmpeg -f image2 -pattern_type glob -i "animation/segmentation*.png" -r 25 -b 50000000 -filter:v "setpts=0.125*PTS" -an animation_regiongrowing.flv
