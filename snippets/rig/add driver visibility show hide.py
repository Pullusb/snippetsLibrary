# add a custom property to a rig (made for 279...)
def add_show_prop_driver(ob, rig, propertie_path):
    '''
    If driver expression start with 1
    add a new variable linked to specified property (arg 2 and 3 : rig object and datapath)
    replace 1 with 'show' in expression
    '''
    print('\n'+ob.name)
    print("drivers")
    for dr in ob.animation_data.drivers:
        print (dr.driver.expression)
        if dr.driver.expression.startswith('1 '):
            #create var
            v = dr.driver.variables.new()
            v.name = 'show'
            v.type = 'SINGLE_PROP'
            v.targets[0].id = rig#ex: bpy.data.objects['oscar_rig']
            v.targets[0].data_path = propertie_path#ex: 'pose.bones["prop"]["show"]'

            #set expression
            dr.driver.expression = 'show' + dr.driver.expression[1:]
            print('>',dr.driver.expression)

        #show for debug
        #for var in dr.driver.variables:
        #    print(var.type, var.name)


for ob in C.selected_objects:
    add_show_prop_driver(ob, bpy.data.objects['chapeau-chapeau-pirate_rig'], 'pose.bones["prop"]["show"]')