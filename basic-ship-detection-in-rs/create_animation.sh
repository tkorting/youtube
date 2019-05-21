# run ffmpeg to create animatino from steps
ffmpeg -f image2 -pattern_type glob -i "animation/threshold_ndwi_step_*.png" -r 25 -b 50000000 -filter:v "setpts=0.5*PTS" -an threshold_ndwi_animation.flv
ffmpeg -f image2 -pattern_type glob -i "animation/ships_in_rgb_step_*.png" -r 25 -b 50000000 -filter:v "setpts=0.5*PTS" -an ships_in_rgb_animation.flv
