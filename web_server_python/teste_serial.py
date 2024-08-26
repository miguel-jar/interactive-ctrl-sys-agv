import serial, time

def envia_pontos(portaUSB, baudrate, data, st_byte, sp_byte, header, stop_flag) -> None:
    try:
        with serial.Serial(port=portaUSB, baudrate=baudrate) as cereal:
            time.sleep(5)
            
            cereal.write(st_byte)

            for x, y in data:
                                
                if stop_flag: 
                    cereal.write(sp_byte)
                    break
                
                msbX, lsbX = (x >> 8), (x & 255)
                msbY, lsbY = (y >> 8), (y & 255)

                baites = header + [msbX, lsbX, msbY, lsbY]
                cereal.write(baites)

                retorno = cereal.read()  # aguarda Arduino solicitar outro ponto
                
    except serial.SerialException:
        print("\nNão foi possível comunicar com arduino. Confira a porta serial e tente novamente.")

if __name__ == "__main__":
    
    import yaml

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

                print(int.from_bytes(cereal.read()))
                print(int.from_bytes(cereal.read()))
                print(int.from_bytes(cereal.read()))
                print(int.from_bytes(cereal.read()))
                print()

                time.sleep(2)