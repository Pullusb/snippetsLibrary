## set image output stamping exemnple
C = bpy.context
D = bpy.data
scn = scene = C.scene
rd = scn.render
ev = scn.eevee

def set_stamp(active_note=False):
    rd.use_stamp = True

    ## Enable
    rd.use_stamp_filename = True
    rd.use_stamp_frame = True
    rd.use_stamp_render_time = True
    rd.use_stamp_time = True
    rd.use_stamp_date = True

    ## Disable
    rd.use_stamp_sequencer_strip = False
    rd.use_stamp_marker = False
    rd.use_stamp_scene = False
    rd.use_stamp_lens = False
    rd.use_stamp_camera = False
    rd.use_stamp_hostname = False
    rd.use_stamp_memory = False
    rd.use_stamp_frame_range = False

    ## Notes
    rd.use_stamp_note = active_note

    if rd.use_stamp_note:
        info = D.texts.get('info')
        txt = ''
        if info:
            for l in info.lines[:2]:
                if 'Created from' in l.body:
                    txt = l.body
        if txt:
            rd.stamp_note_text = txt
        else:#disable notes
            rd.use_stamp_note = False


def setup_render_params(use_stamp=False):
    '''set dimensions, percentage, fps...'''
    if use_stamp:
        set_stamp(active_note=True)
    else:
        rd.use_stamp = False

    rd.resolution_x = 1920
    rd.resolution_y = 1080
    rd.resolution_percentage = 100
    rd.use_border = False
    rd.fps = 25
    rd.use_sequencer = False

    #sampling
    ev.taa_render_samples = 128#push up sample for shadow mainly

    #AO
    ev.use_gtao = True
    ev.gtao_distance = 0.7
    ev.gtao_factor = 0.7
    ev.gtao_quality = 0.2
    ev.use_gtao_bent_normals = False#bent normal makes it lighter than shadows !
    #not sure...
    ev.use_gtao_bounce = True#no bounce is darker... (less AO  on claer object)

    #setup color management
    scene.view_settings.look = 'Filmic - Medium High Contrast'

    #no disable auto folder opening after auto video making
    if hasattr(scene, 'MVopen'):
        scene.MVopen = False

def render_anim(GL=False):
    #openGl render
    if GL:
        bpy.ops.render.opengl(animation=True, view_context=False)#view_context False > look throughcam
    else:
        bpy.ops.render.render(animation=True)


def check_name(name, fp):
    filelist = [splitext(f)[0] for f in os.listdir(fp)]#raw names
    if not name in filelist:
        return name

    ct = 2
    new = name + '_' + str(ct).zfill(2)
    while new in filelist:
        new = name + '_' + str(ct).zfill(2)
        ct+=1
        if ct > 99:
            return None
    return new

def set_video_path():
    setup_render_params(use_stamp=info['stamp'])
    rd.image_settings.file_format = 'FFMPEG'
    rd.image_settings.color_mode = 'RGB'
    rd.ffmpeg.codec = 'H264'
    rd.ffmpeg.constant_rate_factor = 'HIGH'#default 'MEDIUM'
    rd.ffmpeg.format = 'MPEG4'#'MKV', 'QUICKTIME'
    rd.ffmpeg.ffmpeg_preset = 'GOOD'#default = 'GOOD'(compromise), BEST(light - slow), REALTIME(fat-fast)'

    ext = ''
    if rd.ffmpeg.format == 'MPEG4':
        ext = '.mp4'
    elif rd.ffmpeg.format == 'QUICKTIME':
        ext = '.mov'
    elif rd.ffmpeg.format == 'MKV':
        ext = '.mkv'

    filename = splitext(basename(D.filepath))[0]
    fp = join(dirname(D.filepath), 'images')

    if not exists(fp):
        print(f'not found : {fp} ')
        return

    filename = check_name(filename, fp)
    if not filename:
        print('name not available')
        return

    rd.filepath = join(dirname(D.filepath), 'images', filename + ext)

set_video_path()