import json

import bpy
from bpy.props import StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper

bl_info = {
    'name': 'Export Linked Objects to JSON',
    'author': 'Oleg Postoev',
    'version': (0, 0, 1),
    'blender': (2, 80, 0),
    'location': 'File > Export',
    'description': '',
    'warning': '',
    'wiki_url': '',
    'support': 'COMMUNITY',
    'category': 'Import-Export',
}


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def save_liked_data_to_json(context, filepath):
    """
    Function save data about linked objects into JSON as array of object with fields:
        name
        position
        quaternion
        scale
        filename
        parent
        visible

    :param context:
    :param filepath:
    :return:
    """

    print('running save_liked_data_to_json...')

    # Collect data into data_json
    json_data = []
    for item in bpy.data.objects:
        if item.type == 'EMPTY' and item.instance_type == 'COLLECTION':
            asset_name = bpy.data.objects[item.name].instance_collection.name
            asset_file_name = bpy.data.collections[asset_name].library.name_full

            data = {
                'name': item.name,
                'position': {
                    'x': truncate(item.location[0], 1),
                    'y': truncate(item.location[1], 1),
                    'z': truncate(item.location[2], 1),
                },
                'quaternion': {
                    'w': truncate(item.rotation_quaternion[0], 2),
                    'x': truncate(item.rotation_quaternion[1], 2),
                    'y': truncate(item.rotation_quaternion[2], 2),
                    'z': truncate(item.rotation_quaternion[3], 2),
                },
                'rotation_axis_angle': {
                    'w': truncate(item.rotation_axis_angle[0], 2),
                    'x': truncate(item.rotation_axis_angle[1], 2),
                    'y': truncate(item.rotation_axis_angle[2], 2),
                    'z': truncate(item.rotation_axis_angle[3], 2),
                },
                'rotation_euler': {
                    'x': truncate(item.rotation_euler[0], 2),
                    'y': truncate(item.rotation_euler[1], 2),
                    'z': truncate(item.rotation_euler[2], 2),
                },
                'rotation_mode': item.rotation_mode,
                'scale': {
                    'x': truncate(item.scale[0], 2),
                    'y': truncate(item.scale[1], 2),
                    'z': truncate(item.scale[2], 2),
                },
                'parent': asset_name,
                'filename': asset_file_name.replace('.blend', ''),
                'visible': not (item.hide_viewport or item.hide_render),
            }
            json_data.append(data)

    print('json_data')
    print(json_data)

    # Save data
    f = open(filepath, 'w', encoding='utf-8')
    json.dump(json_data, f, ensure_ascii=False, indent=2)
    f.close()

    print('Saved file: ' + filepath)
    return {'FINISHED'}


class ExportLinkedObjects(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = 'export_linked_objects.data'
    bl_label = 'Export to JSON'

    # ExportHelper mixin class uses this
    filename_ext = '.json'

    filter_glob: StringProperty(
        default='*.json',
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        return save_liked_data_to_json(context, self.filepath)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportLinkedObjects.bl_idname, text='Export Linked Objects to JSON')


def register():
    print('register 8')
    bpy.utils.register_class(ExportLinkedObjects)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportLinkedObjects)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == '__main__':
    register()
