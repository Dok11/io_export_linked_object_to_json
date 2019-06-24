import json

import bpy
from bpy.props import StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper

bl_info = {
    "name": "Export Linked Objects to JSON",
    "author": "Oleg Postoev",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "File > Export",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "support": "COMMUNITY",
    "category": "Import-Export",
}


def save_liked_data_to_json(context, filepath):
    # Collect data into data_json
    json_data = []
    for item in bpy.data.objects:
        if item.type == 'EMPTY' and item.instance_type == 'COLLECTION':
            data = {
                'name': item.name,
                'location': {
                    'x': item.location[0],
                    'y': item.location[1],
                    'z': item.location[2],
                },
                'rotation_quaternion': {
                    'w': item.rotation_quaternion[0],
                    'x': item.rotation_quaternion[1],
                    'y': item.rotation_quaternion[2],
                    'z': item.rotation_quaternion[3],
                },
                'rotation_axis_angle': {
                    'w': item.rotation_axis_angle[0],
                    'x': item.rotation_axis_angle[1],
                    'y': item.rotation_axis_angle[2],
                    'z': item.rotation_axis_angle[3],
                },
                'rotation_euler': {
                    'x': item.rotation_euler[0],
                    'y': item.rotation_euler[1],
                    'z': item.rotation_euler[2],
                },
                'rotation_mode': item.rotation_mode,
                'scale': {
                    'x': item.scale[0],
                    'y': item.scale[1],
                    'z': item.scale[2],
                },
                'asset_name': bpy.data.objects[item.name].instance_collection.name,
            }
            json_data.append(data)

    # Save data
    print("running save_liked_data_to_json...")
    f = open(filepath, 'w', encoding='utf-8')
    json.dump(json_data, f, ensure_ascii=False, indent=2)
    f.close()

    return {'FINISHED'}


class ExportLinkedObjects(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export_linked_objects.data"
    bl_label = "Export to JSON"

    # ExportHelper mixin class uses this
    filename_ext = ".json"

    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        return save_liked_data_to_json(context, self.filepath)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportLinkedObjects.bl_idname, text="Export Linked Objects to JSON")


def register():
    print('register 8')
    bpy.utils.register_class(ExportLinkedObjects)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportLinkedObjects)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()
