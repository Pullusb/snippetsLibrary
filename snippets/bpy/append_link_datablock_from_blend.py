## generic load datablock from blend
def load_datablocks(self, src, names, type, link=True):
    with bpy.data.libraries.load(str(src), link=link) as (data_from, data_to):
        setattr(data_to, type, names)

        return getattr(data_to, type)
