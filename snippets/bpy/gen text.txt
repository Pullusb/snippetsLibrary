#Create text through with some options
def gen_text(text=None, position=(0,0,0), select=False, active=False, center=False, up=False):
    '''
    create text object with some argument:
        text : str, prefilled text
        position: vector3, position
        select: boolean, select the text object
        active : boolean, make the text object active
        center : boolean, align CENTER text, else align LEFT
        up : make the text Z axis oriented instead of Y
    '''

    ### create text object and link it to active collection
    text_data = bpy.data.curves.new(name="text", type='FONT')
    if text:text_data.body = text
    if center:text_data.align_x = 'CENTER'

    text_obj = bpy.data.objects.new(name="text", object_data=text_data)
    bpy.context.collection.objects.link(text_obj)
    
    ### Place to a specified location
    text_obj.location = position
    
    ### select state
    text_obj.select_set(select)

    ### make it active
    if active:
        bpy.context.view_layer.objects.active = text_obj

    if up:
        import math
        text_obj.rotation_euler.x = math.radians(90)

    return(text_obj)


def gen_text_ops():
    '''method to create text via ops'''
    bpy.ops.object.text_add(radius=1, align="WORLD", enter_editmode=False, location=(0, 0, 0))
    ob_text = bpy.context.active_object
    print(ob_text.data.body)
    return(ob_text)

def hello_text():
    ob_text = gen_text('Hello World !', position=(0,0,2))
    
    ## to modify text after:
    #ob_text.data.body = 'Hello there'
    
    import math
    ob_text.rotation_euler.x = math.radians(90)
    ob_text.data.align_x = 'CENTER'
    print("ob_text.data.align_x", ob_text.data.align_x)#Dbg


gen_text(select=True, active=True, up=True)#center=True
hello_text()