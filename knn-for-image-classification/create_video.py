# import libraries
import os
import moviepy.video.io.ImageSequenceClip

# define constants
image_folder='animation'
fps=30

# create image sequence
image_files = [image_folder+'/'+img for img in os.listdir(image_folder) if img.endswith(".png")]
image_files.sort()

# create video
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
clip.write_videofile('my_video.mp4')
