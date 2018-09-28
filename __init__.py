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
    reload(op_create_texts)
    reload(utils)
    reload(ui)

import bpy

from add_text_packed_meme.op_create_texts import OBJECT_OT_add_texts
from add_text_packed_meme.op_pack_meme import OBJECT_OT_pack_meme
from add_text_packed_meme.ui import VIEW3D_MT_meme_menu

from add_text_packed_meme import utils, ui

classes = (
    OBJECT_OT_add_texts,
    OBJECT_OT_pack_meme,
    VIEW3D_MT_meme_menu,
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
