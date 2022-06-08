## Import videos in video sequencer editor sorted (here sorted by length).
import bpy
import os
from pathlib import Path
import shlex
import subprocess

def get_frame_count(fp):
    '''
    Return number of frame of passed video as int
    cmd from : https://stackoverflow.com/questions/2017843/fetch-frame-count-with-ffmpeg
    (faster methods are available)
    '''
    cmd = 'ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1'
    cmd = shlex.split(cmd)
    cmd.append(fp)
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        frame_number = proc.stdout.read().decode('utf-8').strip()
        print('frame_number:', frame_number)
        return int(frame_number)

def get_duration(fp, timecode=False):
    '''
    Return duration of video in seconds (2.240000)
    ::timecode:: if True return time 0:00:02.240000  
    cmd from : https://superuser.com/questions/650291/how-to-get-video-duration-in-seconds
    '''
    
    import subprocess
    ## can also select specific stream : -select_streams v:0
    cmd = 'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1'
    if timecode:
        cmd = 'ffprobe -v error -show_entries format=duration -sexagesimal -of default=noprint_wrappers=1:nokey=1'
    cmd = shlex.split(cmd)
    cmd.append(fp)
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        duration = proc.stdout.read().decode('utf-8').strip()
        print('duration:', duration)
        return duration

vse = bpy.context.scene.sequence_editor
strips = vse.sequences

loc = r'path/to/video/files'

videos = [(i, float(get_duration(i.path)) ) for i in os.scandir(loc) if i.name.endswith('.mp4')]

# Sort videos, here organise by length
videos.sort(key=lambda x:x[1])

prev=None
channel = 2
frame_start = 1
for video_path, time in videos: 
    print("time:", time, video_path.name)
    if prev:
        frame_start = prev.frame_final_end
    
    name = video_path.name
    filepath = video_path.path
    #print(name, get_frame_count(video_path.path))

    prev = strips.new_movie(name, filepath, channel, frame_start, fit_method='ORIGINAL')
    sd = strips.new_sound(name + '_sound', filepath, channel-1, frame_start)
    sd.frame_final_end = prev.frame_final_end
    sd.show_waveform = True