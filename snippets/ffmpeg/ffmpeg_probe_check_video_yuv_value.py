def check_yuv_full(fp):
    cmd = ['ffprobe', fp]
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        if 'yuv444p' in str(proc.stderr.read()):
            return True