def date_from_timestamp(stamp, fmt=''):
    '''return date from epoch timestamp in second (int) and an optionnal format (str)
    fmt ex :
    %A, %B %d, %Y %I:%M:%S -> Sunday, January 29, 2017 08:30:00
    %Y-%m-%d_%H-%M-%S -> 2019-11-27_15-55-48 (default)
    '''
    from datetime import datetime
    if not fmt: fmt = "%Y-%m-%d_%H-%M-%S"
    return datetime.fromtimestamp(stamp).strftime(fmt)