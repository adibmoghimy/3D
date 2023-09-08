import ezdxf
from sklearn.cluster import DBSCAN
import numpy as np


def extract_coordinates_from_entities(dxf_file):
    doc = ezdxf.readfile(dxf_file)
    mspace = doc.modelspace()
    coords = []
    map_coords_entity = []

    for entity in mspace:
        coords_entity = {"entity": entity, "coords_index": []}
        if entity.dxftype() == 'LINE':
            coords.append(list(entity.dxf.start))
            coords_entity["coords_index"].append(len(coords) - 1)
            coords.append(list(entity.dxf.end))
            coords_entity["coords_index"].append(len(coords) - 1)
            map_coords_entity.append(coords_entity)
        elif entity.dxftype() == 'CIRCLE':
            coords.append(list(entity.dxf.center))
            coords_entity["coords_index"].append(len(coords) - 1)
            map_coords_entity.append(coords_entity)
        elif entity.dxftype() == 'ARC':
            coords.append(list(entity.dxf.center))
            coords_entity["coords_index"].append(len(coords) - 1)
            coords.append(list(entity.start_point))
            coords_entity["coords_index"].append(len(coords) - 1)
            coords.append(list(entity.end_point))
            coords_entity["coords_index"].append(len(coords) - 1)
            map_coords_entity.append(coords_entity)
        elif entity.dxftype() == 'ELLIPSE':
            coords.append(list(entity.dxf.center))
            coords_entity["coords_index"].append(len(coords) - 1)
        # elif entity.dxftype() == 'DIMENSION':
        #     coords.append(list(entity.dxf.def_point))
        #     coords_entity["coords_index"].append(len(coords) - 1)
        elif entity.dxftype() == 'SPLINE':
            for point in entity.control_points:
                coords.append(list(point))
                coords_entity["coords_index"].append(len(coords) - 1)
        elif entity.dxftype() == 'LWPOLYLINE':
            for point in entity.lwpoints:
                coords.append(list(point[0:3]))
                coords_entity["coords_index"].append(len(coords) - 1)
        elif entity.dxftype() == 'HATCH':
            # Extracting boundary points for HATCH might be complex, so we'll skip it for now
            pass
        elif entity.dxftype() == 'MTEXT':
            coords.append(list(entity.dxf.insert))
            coords_entity["coords_index"].append(len(coords) - 1)
        elif entity.dxftype() == 'INSERT':
            coords.append(list(entity.dxf.insert))
            coords_entity["coords_index"].append(len(coords) - 1)
        # else:
        #     print(entity.dxftype())

    coords_array = np.array(coords)
    return {"coords_array": coords_array, "map_coords_entity": map_coords_entity}


def cluster_coordinates(coords):
    clustering = DBSCAN(eps=400, min_samples=2).fit(coords)
    return clustering.labels_


def map_entity_label(map_coords_entity, labels):
    for coord_entity in map_coords_entity:
        index = coord_entity["coords_index"][0]
        coord_entity["label"] = labels[index]

    return map_coords_entity


def save_entities_to_dxf(entities, filename):
    # Create a new DXF document
    doc = ezdxf.new()
    mspace = doc.modelspace()

    # Add entities to the modelspace
    for entity_data in entities:
        entity = entity_data["entity"]
        if entity.dxftype() == 'LINE':
            mspace.add_line(start=entity.dxf.start, end=entity.dxf.end)
        elif entity.dxftype() == 'CIRCLE':
            mspace.add_circle(center=entity.dxf.center, radius=entity.dxf.radius)
        elif entity.dxftype() == 'ARC':
            mspace.add_arc(center=entity.dxf.center, radius=entity.dxf.radius,
                           start_angle=entity.dxf.start_angle, end_angle=entity.dxf.end_angle)
        elif entity.dxftype() == 'ELLIPSE':
            mspace.add_ellipse(center=entity.dxf.center, major_axis=entity.dxf.major_axis, ratio=entity.dxf.ratio)
        elif entity.dxftype() == 'SPLINE':
            mspace.add_spline(control_points=entity.control_points)
        # Uncomment below if you decide to handle LWPOLYLINE in the future
        elif entity.dxftype() == 'LWPOLYLINE':
            points = [(point.x, point.y) for point in entity.lwpoints]
            mspace.add_lwpolyline(points)
        elif entity.dxftype() == 'MTEXT':
            mspace.add_mtext(text=entity.dxf.text, insert=entity.dxf.insert)
        elif entity.dxftype() == 'INSERT':
            mspace.add_blockref(name=entity.dxf.name, insert=entity.dxf.insert)

    # Save the DXF document
    doc.saveas(filename)


def group_and_save_by_label(map_coords_entity_test):
    # Group entities by label
    grouped_entities = {}
    for entity in map_coords_entity_test:
        label = entity["label"]
        if label not in grouped_entities:
            grouped_entities[label] = []
        grouped_entities[label].append(entity)

    # Save each group to a new DXF file
    for label, entities in grouped_entities.items():
        filename = f"label_{label}.dxf"
        save_entities_to_dxf(entities, filename)


if __name__ == '__main__':
    file_path = "1.dxf"
    coords = extract_coordinates_from_entities(file_path)
    labels = cluster_coordinates(coords["coords_array"])

    map_coords_entity_test = map_entity_label(coords["map_coords_entity"], labels)
    group_and_save_by_label(map_coords_entity_test)
