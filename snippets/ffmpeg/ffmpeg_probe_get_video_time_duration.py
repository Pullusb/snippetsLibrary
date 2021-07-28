def get_duration(fp, timecode=False):
    '''
    Return duration of video in seconds (2.240000)
    ::timecode:: if True return time 0:00:02.240000  
    cmd from : https://superuser.com/questions/650291/how-to-get-video-duration-in-seconds
    '''

    import subprocess
    # can also select specific stream : -select_streams v:0
    cmd = 'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1'
    if timecode:
        cmd = 'ffprobe -v error -show_entries format=duration -sexagesimal -of default=noprint_wrappers=1:nokey=1'
    cmd = cmd.split(' ')
    cmd.append(fp)
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        # out = str(proc.stdout.read()).decode('utf-8')
        duration = proc.stdout.read().decode('utf-8').strip()
        print('duration:', duration)
        return duration
