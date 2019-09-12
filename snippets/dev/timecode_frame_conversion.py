#timecode <-> frame conversion
def timecode_to_frames(timecode,framerate):
    return sum(f * int(t) for f,t in zip((3600*framerate, 60*framerate, framerate, 1), timecode.split(':')))

def frames_to_timecode(frames,framerate):
    return '%02d:%02d:%02d:%02d'%(frames / (3600*framerate),
                                frames / (60*framerate) % 60,
                                frames / framerate % 60,
                                frames % framerate)