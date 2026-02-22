import os
import time

import matplotlib.pyplot as plt
import pandas as pd
import serial


def _format_coordinates(header, x, y):
    # Logic for splitting 16-bit integers into MSB and LSB
    msb_x, lsb_x = (x >> 8), (x & 255)
    msb_y, lsb_y = (y >> 8), (y & 255)

    return header + [msb_x, lsb_x, msb_y, lsb_y]


def save_fig(target_x, target_y, real_x, real_y, save_path: str, save_path_all: str):
    plt.plot(target_x, target_y)
    plt.plot(real_x, real_y)
    plt.legend(["Target points", "Traveled path"])
    plt.xlabel("X [CM]")
    plt.ylabel("Y [CM]")
    plt.grid()

    counter = 1
    # Formatting the filename for the history folder
    img_path = save_path_all.replace("*", f"{counter}.svg")
    data_path = save_path_all.replace("*", f"{counter}_stops.csv")

    while os.path.exists(img_path):
        counter += 1
        img_path = save_path_all.replace("*", f"{counter}.svg")
        data_path = save_path_all.replace("*", f"{counter}_stops.csv")

    plt.savefig(img_path)  # Save to history folder
    plt.savefig(save_path)  # Save to static folder for HTML viewing
    plt.close()

    return data_path


def send_points(
    usb_port: str,
    baudrate: int,
    origin,
    data,
    header,
    start_cmd,
    stop_cmd,
    stop_flag,
    save_path: str,
    save_path_all: str,
) -> None:
    try:
        # 'cereal' renamed to 'ser' (standard for serial objects)
        with serial.Serial(port=usb_port, baudrate=baudrate) as ser:
            time.sleep(6)  # Wait for Arduino reboot

            stops_data = {"target_x": [], "target_y": [], "real_x": [], "real_y": []}

            # Send initial origin coordinates
            payload = _format_coordinates(header, origin[0], origin[1])
            print("\nSending initial coordinates...")
            ser.write(payload)
            ser.write(start_cmd)

            target_x_list, target_y_list = [], []
            real_x_list, real_y_list = [], []

            for x, y in data:
                payload = _format_coordinates(header, x, y)
                print("\nSending data!")
                ser.write(payload)

                target_x_list.append(x)
                target_y_list.append(y)

                while True:
                    if ser.in_waiting > 0:
                        # Reading 2 bytes for X and 2 bytes for Y
                        rx_x = int.from_bytes(ser.read(size=2), byteorder="big")
                        rx_y = int.from_bytes(ser.read(size=2), byteorder="big")

                        # 32760 (0x7FF8) is the 'Target Reached' flag from Arduino
                        if rx_x == 32760 and rx_y == 32760:
                            stops_data["target_x"].append(x)
                            stops_data["target_y"].append(y)
                            # Using the last valid real position received
                            stops_data["real_x"].append(
                                real_x_list[-1] if real_x_list else x
                            )
                            stops_data["real_y"].append(
                                real_y_list[-1] if real_y_list else y
                            )
                            break

                        # Two's complement conversion for negative coordinates
                        rx_x = (rx_x - 0x10000) if rx_x > 0x7FFF else rx_x
                        rx_y = (rx_y - 0x10000) if rx_y > 0x7FFF else rx_y
                        print(rx_x, rx_y)

                        real_x_list.append(rx_x)
                        real_y_list.append(rx_y)

                    if stop_flag.is_set():
                        break

                if stop_flag.is_set():
                    print("Execution interrupted.")
                    break

            if not stop_flag.is_set():
                print("Path completed!")

            ser.write(stop_cmd)  # Safety stop command

            # Save visuals and numerical data
            final_data_path = save_fig(
                target_x_list,
                target_y_list,
                real_x_list,
                real_y_list,
                save_path,
                save_path_all,
            )
            df = pd.DataFrame(data=stops_data)
            df.to_csv(path_or_buf=final_data_path, index=False)

    except serial.SerialException:
        print(
            "\nCould not communicate with Arduino. Check the serial port and try again."
        )
