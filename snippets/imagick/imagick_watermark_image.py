## Watermak image with image magick
## imagick command : composite -dissolve 15 -tile watermark_image image_to_modify output_image
import subprocess

watermark_image = r""
image_to_modify = r""
output_image = r""

## 0-100%, (100-200 fade source image with opaque watermark on top)
opacity = 80


## f-string with quoting command (works with subprocess.call and os.system)
# cmd = f'composite -dissolve {str(opacity)} -tile "{watermark_image}" "{image_to_modify}" "{output_image}"'
# cmd = f'composite -compose multiply -tile "{watermark_image}" "{image_to_modify}" "{output_image}"'

## list format (safer)
## opacity
cmd = ['composite', '-dissolve', str(opacity), '-tile', watermark_image, image_to_modify, output_image]


## multiply fusion mode instead of opacity
#cmd = ['composite', '-compose', 'multiply', '-tile', watermark_image, image_to_modify, output_image]

# launch
subprocess.call(cmd)