def get_frame_count(fp):
    '''
    Return number of frame of passed video as int
    cmd from : https://stackoverflow.com/questions/2017843/fetch-frame-count-with-ffmpeg
    (faster methods are available)
    '''
    cmd = 'ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1'
    cmd = cmd.split(' ')#to list
    cmd.append(fp)
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        # out = str(proc.stdout.read()).decode('utf-8')
        frame_number = proc.stdout.read().decode('utf-8').strip()
        print('frame_number:', frame_number)
        return int(frame_number)