import xml.etree.ElementTree as ET

import matplotlib.pyplot as plt


def _get_paths_from_group(svg_file, group_id):
    # Load the SVG file
    tree = ET.parse(svg_file)
    root = tree.getroot()

    # Default SVG namespace
    ns = {"svg": "http://www.w3.org/2000/svg"}

    # Find the group by ID
    group = root.find(f".//svg:g[@id='{group_id}']", ns)

    # Get all paths within the group
    if group is not None:
        paths = group.findall(".//svg:path", ns)
        return paths
    else:
        return None


def get_path_coordinates(svg_file, ids):
    all_x, all_y = [], []

    for group_id in ids:
        paths = _get_paths_from_group(svg_file, group_id)

        group_x, group_y = [], []
        if paths is not None:
            for path in paths:
                # 'd' attribute contains path data
                data = path.attrib["d"].split()

                x_coords = data[1::3]
                y_coords = data[2::3]

                x_coords = list(map(lambda z: float(z), x_coords))
                y_coords = list(map(lambda z: -float(z), y_coords))

                group_x.append(x_coords)
                group_y.append(y_coords)

        else:
            print(f"Group '{group_id}' not found or contains no paths.")

        all_x.append(group_x)
        all_y.append(group_y)

    return all_x, all_y


def calculate_error(target_x, target_y, real_x, real_y, plot=False) -> list[list[int]]:
    idx = 0
    errors, squared_errors = [], [0] * len(target_x)
    matched_target_x, matched_target_y = [], []

    for rx, ry in zip(real_x, real_y):
        dx, dy = rx - target_x[idx], ry - target_y[idx]
        distance = (dx**2 + dy**2) ** (1 / 2)

        # Threshold to update target index (mimicking robot progress)
        if distance < 18:
            # Store squared error for MSE calculation
            squared_errors[idx] = distance**2
            idx = idx + 1 if idx < len(target_x) - 1 else len(target_x) - 1

        errors.append(distance)
        matched_target_x.append(target_x[idx])
        matched_target_y.append(target_y[idx])

    # Calculate Metrics
    mse = sum(squared_errors) / len(squared_errors)  # Mean Squared Error
    rmse = mse ** (1 / 2)  # Root Mean Squared Error
    mae = sum([e ** (1 / 2) for e in squared_errors]) / len(
        squared_errors
    )  # Mean Absolute Error

    print("\nMSE (EQM) =", mse)
    print("RMSE (REQM) =", rmse)
    print("Mean Absolute Error =", mae)

    if plot:
        plt.figure()
        plt.plot(errors)
        plt.title("Error over time")

    return [matched_target_x, matched_target_y]


if __name__ == "__main__":
    svg_file = "routes/06_10/55.svg"  # Update path as needed
    ids = ["line2d_25", "line2d_26"]

    # Extract coordinates
    all_x, all_y = get_path_coordinates(svg_file, ids)

    # Target Trajectory (xt, yt) and Real Trajectory (xr, yr)
    target_x_raw, target_y_raw = all_x[0][0], all_y[0][0]
    real_x_raw, real_y_raw = all_x[1][0], all_y[1][0]

    # Scaling logic
    x_distances, y_distances = [], []
    for i in range(1, len(target_x_raw)):
        dx = abs(target_x_raw[i - 1] - target_x_raw[i])
        dy = abs(target_y_raw[i - 1] - target_y_raw[i])
        x_distances.append(dx)
        y_distances.append(dy)

    x_scale = 1000 / max(x_distances)
    # Scale Y based on the sum of segments
    y_scale = 1000 / (y_distances[0] + y_distances[1])

    x_offset = min(all_x[0][0])
    y_offset = min(all_y[0][0])

    # Apply Offset and Scale
    target_x = [(val - x_offset) * x_scale for val in target_x_raw]
