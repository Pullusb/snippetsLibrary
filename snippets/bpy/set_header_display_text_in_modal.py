## set header text during modal
# in modal loop
display_text = f"Modal engaged | tweak level: {self.value}"
context.area.header_text_set(display_text)

# at exit
context.area.header_text_set(None)