import bpy, os

keep_alpha = True
custom_delay = True

delay_time = 4 #hundreds of a second : eg.>> 25 fPS > 100/25 = 4

note = bpy.context.scene.render.stamp_note_text
note = note.replace(" ", "_") #convert whitespace to underscore

outfolder = bpy.path.abspath(bpy.context.scene.render.filepath)
head, tail = os.path.split(outfolder)
files = [i for i in os.listdir(head)]

option = ""
delay = ""

if bpy.context.scene.render.film_transparent:
    if keep_alpha:
        option = "-dispose 2 "
    else:
        option = "-alpha off "

if custom_delay and delay_time:
    delay = '-delay ' + str(delay_time) + ' '

print ("generating gif")
print ("-"*14)

gifname = tail + "_" + note + ".gif"

if files:
    cmd = "convert " + option + delay + head + "\\*.png " + head + "\\..\\" + gifname
    print (cmd)
    os.system(cmd)
    print ("gif generated: " + gifname)

else:
    print ("NO FILES TO CONVERT IN RENDER OUTPUT LOCATION")