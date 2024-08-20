import hashlib

from wand.image import Image as wandImage


def save_stripped_file(file_contents, output_path):
    with wandImage(blob=file_contents) as img:
        img.strip()
        img.save(filename=output_path)


def inverse_geojson(geojson):
    if geojson is None:
        return None
    geom_type = geojson["type"]

    def transform_coord(coord):
        return [coord[0], -coord[1]]

    if geom_type == "Point":
        geojson["coordinates"] = transform_coord(geojson["coordinates"])
    elif geom_type in ["LineString", "MultiPoint"]:
        geojson["coordinates"] = [transform_coord(coord) for coord in geojson["coordinates"]]
    elif geom_type in ["Polygon", "MultiLineString"]:
        geojson["coordinates"] = [[transform_coord(coord) for coord in ring] for ring in geojson["coordinates"]]
    elif geom_type == "MultiPolygon":
        geojson["coordinates"] = [
            [[transform_coord(coord) for coord in ring] for ring in polygon] for polygon in geojson["coordinates"]
        ]
    elif geom_type == "GeometryCollection":
        for geometry in geojson["geometries"]:
            inverse_geojson(geometry)
    else:
        raise ValueError(f"Unsupported geometry type: {geom_type}")
    return geojson


def get_projection_id(feature):
    if feature.get("projected_feature"):
        if len(feature.get("projected_feature", [])) > 0:
            proj_id = feature.get("projected_feature", [])[0].get("cdr_projection_id")
            return proj_id
    return ""


def return_line_properties(feature):
    return {"dash_pattern": feature.get("dash_pattern", ""), "symbol": feature.get("symbol", "")}


def return_point_properties(feature):
    return {"dip": feature.get("dip", ""), "dip_direction": feature.get("dip_direction", "")}


def return_properties(legend_features, feature):
    line_properties = {}
    if legend_features.get("category") == "line":
        line_properties = return_line_properties(feature)

    point_properties = {}
    if legend_features.get("category") == "point":
        point_properties = return_point_properties(feature)

    return {
        **line_properties,
        **point_properties,
        "px_bbox": feature.get("px_bbox", []),
        "legend_id": legend_features.get("legend_id", []),
        "label": legend_features.get("label"),
        "abbreviation": legend_features.get("abbreviation"),
        "description": legend_features.get("description", ""),
        "system": legend_features.get("system"),
        "system_version": legend_features.get("system_version"),
        "model_id": feature.get("model_id"),
        "confidence": feature.get("confidence"),
        "map_unit_age_text": legend_features.get("map_unit_age_text"),
        "map_unit_lithology": legend_features.get("map_unit_lithology"),
        "map_unit_b_age": legend_features.get("map_unit_b_age"),
        "map_unit_t_age": legend_features.get("map_unit_t_age"),
        "projection_id": get_projection_id(feature),
        "color": legend_features.get("color", ""),
        "pattern": legend_features.get("pattern", ""),
        "validated": feature.get("validated"),
    }


def hash_string(input_string, algorithm="sha256"):
    hash_object = hashlib.new(algorithm)
    encoded_string = input_string.encode("utf-8")
    hash_object.update(encoded_string)
    return hash_object.hexdigest()
