import json

from ezdxf.addons.drawing import layout, svg
from ezdxf.addons.drawing.frontend import Frontend
from ezdxf.addons.drawing.properties import RenderContext
from ezdxf.document import Drawing
from ezdxf.filemanagement import new, readfile

# Path definitions
CONFIG_JSON_PATH = "static/config.json"
MAP_SVG_PATH = "static/map.svg"
SOLIDWORKS_TEMPLATES_PATH = "map_processing/sw_templates/"


def _get_lines(doc: Drawing):
    msp = doc.modelspace()
    lines_query = msp.query("LINE")
    line_set = set()

    for entity in lines_query:
        x_coords = (entity.dxf.start[0], entity.dxf.end[0])
        y_coords = (entity.dxf.start[1], entity.dxf.end[1])
        line_set.add((x_coords, y_coords))

    return line_set


def _get_solidworks_info(doc: Drawing):
    sheet_types = ["A0", "A1", "A2", "A3", "A4"]
    msp = doc.modelspace()

    scale_parts, sheet_type = None, None

    for text_entity in msp.query("MTEXT"):
        if text_entity.text in sheet_types:
            sheet_type = text_entity.text.lower()
        elif "ESCALA:" in text_entity.text:
            # Extracts scale (e.g., "1:50")
            scale_parts = text_entity.text[7:].split(":")

    if scale_parts is None or sheet_type is None:
        print("scale_parts or sheet_type not defined.")
        raise (ValueError)

    real_scale = int(scale_parts[1]) / int(scale_parts[0])

    units_map = {4: "MM", 5: "CM", 6: "M"}
    drawing_unit = units_map[doc.header.get("$INSUNITS")]

    return sheet_type, drawing_unit, real_scale


def _normalize_data(data, unit: str, draw_scale):
    # Standardizes everything to CM
    scale_conv_to_cm = {"MM": 0.1, "CM": 1, "M": 100}

    # Normalizing based on the smallest start point (offset)
    min_point = min(data)
    offset_x, offset_y = min_point[0][0], min_point[1][0]

    normalized_rows = []
    for line in data:
        x_norm = [
            (val - offset_x) * draw_scale * scale_conv_to_cm[unit] for val in line[0]
        ]
        y_norm = [
            (val - offset_y) * draw_scale * scale_conv_to_cm[unit] for val in line[1]
        ]
        normalized_rows.append([x_norm, y_norm])

    return normalized_rows


def _export_to_svg(points):
    doc = new()
    msp = doc.modelspace()

    min_x, max_x = float("inf"), -float("inf")
    min_y, max_y = float("inf"), -float("inf")

    for p in points:
        min_x = min(min_x, min(p[0]))
        max_x = max(max_x, max(p[0]))
        min_y = min(min_y, min(p[1]))
        max_y = max(max_y, max(p[1]))
        # Add line using [start_x, start_y], [end_x, end_y]
        msp.add_line([p[0][0], p[1][0]], [p[0][1], p[1][1]])

    max_size_px = 1000
    width_cm, height_cm = max_x - min_x, max_y - min_y

    # Calculate aspect ratio for normalization
    max_dim = max(width_cm, height_cm)
    norm_scale_w, norm_scale_h = width_cm / max_dim, height_cm / max_dim
    norm_width_px, norm_height_px = (
        max_size_px * norm_scale_w,
        max_size_px * norm_scale_h,
    )

    metadata = {
        "max_size_px": max_size_px,
        "width_cm": round(width_cm, 2),
        "height_cm": round(height_cm, 2),
        "norm_width_px": int(norm_width_px),
        "norm_height_px": int(norm_height_px),
    }

    with open(CONFIG_JSON_PATH, "w") as config_file:
        json.dump(metadata, config_file, indent=4)

    # Render context for SVG generation
    context = RenderContext(doc)
    backend = svg.SVGBackend()
    frontend = Frontend(context, backend)
    frontend.draw_layout(msp)

    page = layout.Page(
        width=norm_width_px, height=norm_height_px, units=layout.Units.px
    )
    svg_string = backend.get_string(page)

    with open(MAP_SVG_PATH, "wt", encoding="utf8") as svg_file:
        svg_file.write(svg_string)


def generate_map(filename: str, is_solidworks: bool = True):
    doc = readfile(filename)
    file_lines = _get_lines(doc)

    if is_solidworks:
        try:
            sheet_type, unit, scale = _get_solidworks_info(doc)

            # Load template to remove borders and title blocks
            template_doc = readfile(SOLIDWORKS_TEMPLATES_PATH + sheet_type + ".DXF")
            template_lines = _get_lines(template_doc)

            # Map is the difference between file lines and template lines
            map_lines = file_lines - template_lines
            normalized_points = _normalize_data(map_lines, unit, scale)
            _export_to_svg(normalized_points)
            return normalized_points
        except ValueError:
            print("Not a Solidworks file. Trying other approach...")

    _export_to_svg(file_lines)
    return file_lines


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # Example usage
    map_coordinates = generate_map("map_processing/maps/corridor.DXF")
    for line in map_coordinates:
        plt.plot(line[0], line[1])
    plt.show()
