import serial, time, yaml

if __name__ == "__main__":
    with open('configs.yaml', 'r') as arquivo:
        configs = yaml.load(arquivo, yaml.SafeLoader)

    data = [[0, 16], [512, 1024]]

    with serial.Serial(port=configs['PORTA_USB'], baudrate=configs['BAUDRATE']) as cereal:
        time.sleep(5)
        while True:
            for x, y in data:
                msbX, lsbX = (x >> 8), (x & 255)
                msbY, lsbY = (y >> 8), (y & 255)

                baites = configs['HEADER'] + [msbX, lsbX, msbY, lsbY]
                cereal.write(baites)

                xx = int.from_bytes(cereal.read(size=2))
                yy = int.from_bytes(cereal.read(size=2))
                print(xx, yy)

                time.sleep(2)