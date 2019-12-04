def sizeof_fmt(num, suffix='B'):
    '''
    return human readable size from bytes amount
    ex: sizeof_fmt(os.stat(filename).st_size)
    '''
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)