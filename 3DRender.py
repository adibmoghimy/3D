import bpy


def creat3D():
    # Step 1: Import the DXF file
    bpy.ops.import_scene.dxf(filepath="1.dxf")

    # Step 2: Access the imported objects (assuming they are imported as curves)
    imported_objects = bpy.context.selected_objects

    # Step 3: Convert curves to mesh (if they are imported as curves)
    for obj in imported_objects:
        if obj.type == 'CURVE':
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.convert(target='MESH')

    # Step 4: Now you can manipulate the mesh objects further to create a 3D shape
    # For example, you might extrude the meshes to give them volume
    for obj in imported_objects:
        if obj.type == 'MESH':
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, 1)})
            bpy.ops.object.mode_set(mode='OBJECT')

    # Step 5: Save the resulting 3D shape as a new file (if desired)
    bpy.ops.wm.save_as_mainfile(filepath="path/to/save/your/3dmodel.blend")


if __name__ == '__main__':
    creat3D()
