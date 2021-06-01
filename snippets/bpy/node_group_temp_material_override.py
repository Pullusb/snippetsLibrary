## create nodgroup for temporary material override
import bpy

def remove_nodegroup_override():
    '''Remove nodes named 'nodegroup_override_output' and connected nodegroup'''
    for mat in bpy.data.materials:
        if mat.use_nodes:
            for node in mat.node_tree.nodes :
                #can fin with node.color = (0.5,0.6,0.8)
                if 'nodegroup_override_output' in node.name:
                    output = node
                    group = output.inputs['Surface'].links[0].from_node
                    mat.node_tree.nodes.remove(output)
                    mat.node_tree.nodes.remove(group)

def create_nodegroup_override(mat, nodegroup) :
    '''
    Override given material with given nodegroup
    Add node_group connected to a new output node in nodetree
    (just activate out node 'nodegroup_override_output' if already exists)
    return a tupple with group node, output node and orignal output node
    '''
    if not mat.use_nodes:
        return
    node_tree = mat.node_tree
    if any('nodegroup_override_output' in n.name for n in node_tree.nodes):
        #if already exist just activate it
        print(mat.name, 'Already has override node')
        output = node_tree.nodes['nodegroup_override_output']
        try:
            group = output.inputs['Surface'].links[0].from_node
        except:
            print('!!! > no group connected to override material output node')
            group = None

    else:
        group = node_tree.nodes.new("ShaderNodeGroup")
        group.node_tree = nodegroup#bpy.data.node_groups['OldNodeGroupName']

        output = node_tree.nodes.new("ShaderNodeOutputMaterial")
        output.name = 'nodegroup_override_output'

        node_tree.links.new(group.outputs[0],output.inputs[0])

        # decoration
        rightest = max([node.location.x for node in node_tree.nodes])
        lowest = min([node.location.y for node in node_tree.nodes])
        output.location = (rightest, lowest - 50)
        group.location = (rightest-250, lowest - 50)
        output.use_custom_color = True
        output.color = (0.5,0.6,0.8)
        group.use_custom_color = True
        group.color = (0.5,0.6,0.8)

    for node in node_tree.nodes :
        if node.type == 'OUTPUT_MATERIAL' :
            node.is_active_output = False
            org_out = node
    output.is_active_output = True

    return (group,output,org_out)

def recusive_get_ob(ob):
    if ob.type == 'EMPTY' and ob.instance_collection is not None:
        for subob in ob.instance_collection.all_objects:
            recusive_get_ob(subob)
    else:
        if ob.type in ['MESH', 'CURVE']:
            for ms in ob.material_slots:
                if not ms.material:
                    continue
                if 'volumetric' in ms.material.name.lower():
                    continue
                create_nodegroup_override(ms.material, ng_override) # bpy.data.node_groups['override'])
                # if ms.material:
                #    ms.material = bpy.data.materials['HOLDOUT']
                # print(ms.material.name)

def create_nodegroup():
    ng = bpy.data.node_groups.new('override', 'ShaderNodeTree')
    gp_out = ng.nodes.new('NodeGroupOutput')
    gp_out.location.x = 250

    ## holdout
    # hold = ng.nodes.new('ShaderNodeHoldout')
    # ng.links.new(hold.outputs[0], gp_out.inputs[0])

    ## black emit
    emit = ng.nodes.new('ShaderNodeEmission')
    emit.inputs['Color'].default_value[:] = (0,0,0,1.0)
    ng.links.new(emit.outputs[0], gp_out.inputs[0])
    return ng


ng_override = bpy.data.node_groups.get('override')
if not ng_override:
    ng_override = create_nodegroup()

for o in bpy.context.scene.objects:
    recusive_get_ob(o)
