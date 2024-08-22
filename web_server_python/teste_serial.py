import serial, time

portaUSB = 'COM5'
baudrate = 115200
header = [16, 23]

def envia_pontos(data):
    try:
        with serial.Serial(port=portaUSB, baudrate=baudrate) as cereal:
            time.sleep(5)

            for x, y in data:
                msbX, lsbX = (x >> 8), (x & 255)
                msbY, lsbY = (y >> 8), (y & 255)

                baites = header + [msbX, lsbX, msbY, lsbY]
                cereal.write(baites)

                retorno = cereal.read()  # aguarda Arduino solicitar outro ponto
    except serial.SerialException:
        print("\nNão foi possível comunicar com arduino. Confira a porta serial e tente novamente.")

if __name__ == "__main__":
    data = [[0, 16], [512, 1024]]

    with serial.Serial(port=portaUSB, baudrate=baudrate) as cereal:
        time.sleep(5)
        while True:
            for x, y in data:
                msbX, lsbX = (x >> 8), (x & 255)
                msbY, lsbY = (y >> 8), (y & 255)

                baites = header + [msbX, lsbX, msbY, lsbY]
                cereal.write(baites)

                print(int.from_bytes(cereal.read()))
                print(int.from_bytes(cereal.read()))
                print(int.from_bytes(cereal.read()))
                print(int.from_bytes(cereal.read()))
                print()

                time.sleep(2)