## Overlay an image on a video with ffmpeg (Watermak)
## command : ffmpeg -i video_source.mp4 -i watermark_image.png -filter_complex "overlay=x=(main_w-overlay_w)/2:y=(main_h-overlay_h)/2" output.mp4
import subprocess

watermark_image = r"E:\travaux_perso\PERSO\Logo - Signature\Icon\icon_SB_256blanc.png"
video_source = r"G:\WORKS\PRO\ARCHIVE\J_colin\Video_Drone_AW\render\gl_render_L.mp4"
output = r"G:\WORKS\PRO\ARCHIVE\J_colin\Video_Drone_AW\render\WM.mp4"

cmd = ['ffmpeg', '-i', video_source, '-i', watermark_image, '-filter_complex', 'overlay=x=(main_w-overlay_w)/2:y=(main_h-overlay_h)/2', output]

subprocess.call(cmd)
print('Done')