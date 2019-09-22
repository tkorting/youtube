# Subscribe to my channel, share and like my videos at
# http://youtube.com/tkorting
#
# This source code is used to create a step-by-step
# animation about image enhancement. Feel free to 
# use and share this code.
#
# Thales Sehn Körting

# run python with main file and create animation
python main.py

# run ffmpeg to create animation from steps
ffmpeg -f image2 -pattern_type glob -i "animation/gain_*.png" -r 25 -b 50000000 -filter:v "setpts=1.25*PTS" -an gain_animation.flv
ffmpeg -f image2 -pattern_type glob -i "animation/offset_*.png" -r 25 -b 50000000 -filter:v "setpts=1.25*PTS" -an offset_animation.flv
ffmpeg -f image2 -pattern_type glob -i "animation/log_*.png" -r 25 -b 50000000 -filter:v "setpts=1.25*PTS" -an log_animation.flv
ffmpeg -f image2 -pattern_type glob -i "animation/nth root_*.png" -r 25 -b 50000000 -filter:v "setpts=1.25*PTS" -an nth_root_animation.flv
ffmpeg -f image2 -pattern_type glob -i "animation/negative_*.png" -r 25 -b 50000000 -filter:v "setpts=1.25*PTS" -an negative_animation.flv
ffmpeg -f image2 -pattern_type glob -i "animation/nth power_*.png" -r 25 -b 50000000 -filter:v "setpts=1.25*PTS" -an nth_power_animation.flv
ffmpeg -f image2 -pattern_type glob -i "animation/inverse log_*.png" -r 25 -b 50000000 -filter:v "setpts=1.25*PTS" -an inverse_log_animation.flv
# 