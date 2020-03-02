def get_last_traceback(to_clipboad=False):
    '''Get last traceback error details summed in string'''
    import sys
    message = ''
    linum = ''

    if hasattr(sys, "last_traceback") and sys.last_traceback:
        i = 0
        last=sys.last_traceback.tb_next
        tbo = None
        while last:
            i+=1
            tbo = last
            last = last.tb_next
            if i>100:
                print("bad recursion")
                return False

        if not tbo: tbo = sys.last_traceback

        linum = sys.last_traceback.tb_lineno# first linum
        message += f'from line {str(linum)}\n'

        frame = str(tbo.tb_frame)
        if frame:
            if 'file ' in frame:
                # frame = 'file: ' + frame.split('file ')[1]
                frame = '\n'.join(frame.split(', ')[1:3])
            message += f'{frame}\n'

    else:
        print('No error traceback found by sys module')
        return

    if hasattr(sys, "last_type") and sys.last_type:
        error_type = str(sys.last_type)
        error_type = error_type.replace("<class '", "").replace("'>","")
        message =  f'type {error_type}\n{message}'

    if hasattr(sys, "last_value") and sys.last_value:
        message += f'error : {str(sys.last_value)}\n'

        if not linum and hasattr(sys.last_value, "lineno"):# maybe not usefull
            print('use "last_value" line num')
            message += f'line {str(sys.last_value.lineno)}\n'

    if not message :
        print('No message to display')
        return

    if message and to_clipboad:
        bpy.context.window_manager.clipboard = message

    return message

error = get_last_traceback()
# if error:# code markdown formatting to send over tchat
#     error = f'```\n{error}```'
print(error)