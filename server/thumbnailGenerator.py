from moviepy.editor import VideoFileClip
from checktype import *


def generate_thumbnail(name):
    if checkType(name) == 'video':
        path = "/app/media/"+name
        clip = VideoFileClip(path, audio=False)
        # getting only first 3 seconds
        clip = clip.subclip(0, 3)
        nameWithoutExtension = name.split('.')[0]
        thumbnail_output = "/app/media/thumbnails/" + nameWithoutExtension + ".png"
        clip.save_frame(thumbnail_output, t = clip.duration/2)

