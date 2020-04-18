## Context overrides with various methods
def get_3dview_override():
  for window in bpy.context.window_manager.windows:
      screen = window.screen
      for area in screen.areas:
          if area.type == 'VIEW_3D':
              for region in area.regions:
                  if region.type == 'WINDOW':
                      return {'window': window, 'screen': screen, 'area': area, 'region': region}
                      ## Can do operator here instead of return (to make if in all view instead of first found)
                      # bpy.ops. ...
                      # break# break go to next view if any

override = get_3dview_override()
if override:
    #bpy.ops.screen.screen_full_area(override)
    #bpy.ops.screen.back_to_previous(override)
    #bpy.ops.view3d.view_orbit(override)
    #bpy.ops.view3d.view_pan(override)
    bpy.ops.view3d.zoom(override, delta=-5, mx=0, my=0)
    #bpy.ops.mesh.loopcut(override, number_cuts=...,)#<<not working


## Find_3D_view_Pannel_options (2.7):
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        area.spaces[0].use_matcap = True
        area.spaces[0].show_only_render = True
        area.spaces[0].matcap_icon = '12'

## access BG images (2.7 ?)
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        space_data = area.spaces.active
        bg = space_data.background_images.new()
        bg.image = img
        break

## texteditor_override
def get_text_override():
    # for finding text area
    win      = bpy.context.window
    scr      = win.screen
    areastxt = [area for area in scr.areas if area.type == 'TEXT_EDITOR']
    region   = [region for region in areastxt[0].regions if region.type == 'WINDOW']

    override = {'window':win,
                'screen':scr,
                'area'  :areastxt[0],
                'region':region,
                "edit_text" : areastxt[0].spaces[0].text #find text datablock
                #'scene' :bpy.context.scene,
                }#
    return (override)

override = get_text_override()
if override:
    #untested example:
    bpy.ops.text.scroll(lines=1)


## point_cache_override
def get_cloth_override():
    for scene in bpy.data.scenes:
        for object in scene.objects:
            for modifier in object.modifiers:
                if modifier.type == 'CLOTH':
                    override = {'scene': scene, 'active_object': object, 'point_cache': modifier.point_cache}
                    return(override)
                    ## direct use:
                    # bpy.ops.ptcache.bake(override, bake=True)
                    # break

## Or shorter version:
# a = {}
# a['point_cache'] = bpy.data.objects['Cube'].particle_systems['ParticleSystem'].point_cache
# bpy.ops.ptcache.bake_from_cache(a)

## Cloth overrides
override = get_cloth_override()
if override:
    #free bake from previous cache
    bpy.ops.ptcache.free_bake(override)
    #change values ...
    mod = bpt.context.object.modifiers["Cloth"]
    set = mod.settings
    ptc = mod.point_cache
    #bake and render
    bpy.ops.ptcache.bake(override,bake=True)
