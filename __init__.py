bl_info = {
    "name": "Packed Meme",
    "author": "florianfelix",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "",
    "description": "Add Packed Meme form text",
    "wiki_url": "",
    "category": "Add Text",
}


if 'bpy' in locals():
    from importlib import reload
    reload(op_pack_meme)

import bpy

from add_text_packed_meme import op_pack_meme





classes = (
    op_pack_meme.OBJECT_OT_pack_meme,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
