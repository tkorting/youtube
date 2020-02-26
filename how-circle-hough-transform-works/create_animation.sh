rm -f drawing_circle.flv
ffmpeg -f image2 -pattern_type glob -i "animation/drawing_circle*.png" -r 25 -b 50000000 -filter:v "setpts=0.5*PTS" -an drawing_circle.flv

rm -f accumulator.flv
ffmpeg -f image2 -pattern_type glob -i "animation/accumulator*.png" -r 25 -b 50000000 -filter:v "setpts=0.5*PTS" -an accumulator.flv
