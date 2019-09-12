#import the bpy module to access blender API
import bpy

#WARNING: this is written and tested for blender 2.79
#blender 2.8 and newer will likely have a different python API

#create a property group, this is REALLY needed so that operators
#AND the UI can access, display and expose it to the user to change
#in here we will have all properties(variables) that is neccessary
class CustomPropertyGroup(bpy.types.PropertyGroup):
    #NOTE: read documentation about 'props' to see them and their keyword arguments
    #builtin float (variable)property that blender understands
    float_slider: bpy.props.FloatProperty(name='float value', soft_min=0, soft_max=10)
    #builtin integer (variable)property
    int_slider: bpy.props.IntProperty(name='int value', soft_min=0, soft_max=10)
    #builting boolean (variable)property
    bool_toggle: bpy.props.BoolProperty(name='bool toggle')
    #builting string (variable)property
    string_field: bpy.props.StringProperty(name='string field')


#create a panel (class) by deriving from the bpy Panel, this be the UI
class CustomToolShelf(bpy.types.Panel):
    #variable for determining which view this panel will be in
    bl_space_type = 'VIEW_3D'
    #this variable tells us where in that view it will be drawn
    bl_region_type = 'UI'
    #this variable is a label/name that is displayed to the user
    bl_label = 'Custom Tool Shelf'
    #this context variable tells when it will be displayed, edit mode, object mode etc
    bl_context = 'objectmode'
    #category is esentially the main UI element, the panels inside it are
    #collapsible dropdown menus drawn under a category
    #you can add your own name, or an existing one and it will be drawn accordingly
    bl_category = 'View'
    
    #now we define a draw method, in it we can tell what elements we want to draw
    #in this new space we created, buttons, toggles etc.
    def draw(self, context):
        #shorten the self.layout to just layout for convenience
        layout = self.layout
        #add a button to it, which is called an operator, its a little tricky to do it but...
        #first argument is a string with the operator name to be invoked
        #in example 'bpy.ops.mesh.primitive_cube_add()' is the function we want to invoke
        #so we invoke it by name 'mesh.primitive_cube_add'
        #then the rest are keyword arguments based on documentation
        #NOTE: for custom operations, you need to define and register an operator with
        #custom name, and then call it by that custom name as we did here
        layout.operator('mesh.primitive_cube_add', text = 'Add new cube')
        #the custom operator that we just made will go here as a new button
        layout.operator('custom.simple_op', text = 'Simple Op')
        #add multiple items on the same line, like a column layout, from left to right
        subrow = layout.row(align=True)
        #the complex operator will be draw on the left, as a button
        subrow.operator('custom.complex_op', text = 'Complex Op')
        #the property will be drawn next to it on the right, as an adjustible slider thing
        subrow.prop(context.scene.custom_props, 'float_slider')
        #add a label to the UI
        layout.label(text="v Testing layout, does nothing bellow this v")
        #add a new row with multiple elements in a column
        subrow = layout.row(align=True)
        #add a toggle
        subrow.prop(context.scene.custom_props, 'bool_toggle')
        #add an int slider
        subrow.prop(context.scene.custom_props, 'int_slider')
        #add a custom text field in the usual layout
        layout.prop(context.scene.custom_props, 'string_field')
        #NOTE: for more layout things see the types.UILayout in the documentation
        

#in order to make a button do custom behavior we need to register and make an operator, a basic
#custom operator that does not take any property and just runs is easily made like so        
class CustomSimpleOperator(bpy.types.Operator):
    #the id variable by which we can invoke the operator in blender
    #usually its good practice to have SOMETHING.other_thing as style so we can group
    #many id's together by SOMETHING and we have less chance of overriding existing op's
    bl_idname = 'custom.simple_op'
    #this is the label that essentially is the text displayed on the button
    bl_label = 'Simple Op'
    #these are the options for the operator, this one makes it not appear
    #in the search bar and only accessible by script, useful
    #NOTE: it's a list of strings in {} braces, see blender documentation on types.operator
    bl_options = {'INTERNAL'}

    #this is needed to check if the operator can be executed/invoked
    #in the current context, useful for some but not for this example    
    @classmethod
    def poll(cls, context):
        #check the context here
        return context.object is not None
    
    #this is the cream of the entire operator class, this one's the function that gets
    #executed when the button is pressed
    def execute(self, context):
        #just do the logic here
        
        #this is a report, it pops up in the area defined in the word
        #in curly braces {} which is the first argument, second is the actual displayed text
        self.report({'INFO'}, "The custom operator actually worked!")
        #return value tells blender wether the operation finished sueccessfully
        #needs to be in curly braces also {}
        return {'FINISHED'}

    
#this is a more complex operator, it will take a property value and
#then use it for computation of some kind
class CustomComplexOperator(bpy.types.Operator):
    #add an id to be able to access it
    bl_idname = 'custom.complex_op'
    #add label to show up on the button
    bl_label = 'Complex Op'
    #make it internal so we can't search for it
    bl_options={'INTERNAL'}
    
    #make it check if it can run in the context
    @classmethod
    def poll(cls, context):
        #check the context here
        return context.object is not None
    
    #here we can define how the operator itself is drawn to the screne
    #that means we can add toggles, sliders etc and be able to acess their
    #set values in the code execution
    #NOTE: this is automaticly done by default, if you have defined it
    #then it will be used, this gives more control over the layout
    #def draw(self, context):
    #TODO: could not get it working so far, would like to make it work on tools shelf

    #invoke runs before execute, it is useful to (run background tasts???)
    #run code that sets up or reads values neccessary for script execution
    #it is a little more involved then a simple operator
    #NOTE: look at types.operator documentation for more information
    #def invoke(self, context):
    
    #execute method for... executing... this... on call(button press) (after invoke)
    def execute(self, context):
        #shorthand to reach properties of self
        props = self.properties
        #shorthand to scene
        scene = context.scene
        #this sends a report showing the set value of the slider
        self.report({'INFO'}, "The value of the slider: " + str(scene.custom_props.float_slider))
        #return value that tells blender we finished without failure
        return {'FINISHED'}

#this is the addon info for when you choose to install it
#NOTE: for more information, see addon tutorial in the documentation
bl_info={
        "name":"Ui test addon",
        "category":"tests"
    }

#this function is called on plugin loading(installing), adding class definitions into blender
#to be used, drawed and called
def register():
    #register property group class
    bpy.utils.register_class(CustomPropertyGroup)
    #this one especially, it adds the property group class to the scene context (instantiates it)
    bpy.types.Scene.custom_props = bpy.props.PointerProperty(type=CustomPropertyGroup)
    #register the classes with the correct function
    bpy.utils.register_class(CustomSimpleOperator)
    bpy.utils.register_class(CustomComplexOperator)
    bpy.utils.register_class(CustomToolShelf)


#same as register but backwards, deleting references
def unregister():
    #delete the custom property pointer
    #NOTE: this is different from its accessor, as that is a read/write only
    #to delete this we have to delete its pointer, just like how we added it
    del bpy.types.Scene.custom_props 
    #now we can continue to unregister classes normally
    bpy.utils.unregister_class(CustomPropertyGroup)
    bpy.utils.unregister_class(CustomSimpleOperator)
    bpy.utils.unregister_class(CustomComplexOperator)
    bpy.utils.unregister_class(CustomToolShelf)     

#NOTE: during testing if this addon was installed from a file then that current version
#of that file will be copied over to the blender addons directory
#if you want to see what changes occour you HAVE TO REINSTALL from the new file for it to register
    
#a quick line to autorun the script from the text editor when we hit 'run script'
if __name__ == '__main__':
    register()