import serial, time

def envia_pontos(portaUSB : str, baudrate : int, data, start, stop, header, stop_flag) -> None:
    try:
        with serial.Serial(port=portaUSB, baudrate=baudrate) as cereal:
            time.sleep(5)
            cereal.write(start)
            toleranciaX, toleranciaY = 10, 10

            for x, y in data:
                msbX, lsbX = (x >> 8), (x & 255)
                msbY, lsbY = (y >> 8), (y & 255)

                baites = header + [msbX, lsbX, msbY, lsbY]
                print("Enviando dados!")
                cereal.write(baites)

                # Confirma o que foi enviado para o Arduino
                xx = int.from_bytes(cereal.read(size=2))
                yy = int.from_bytes(cereal.read(size=2))
                print(xx, yy)

                x_atual, y_atual = 0, 0
                while ((abs(x - x_atual) > toleranciaX) or (abs(y-y_atual) > toleranciaY)):

                    if cereal.in_waiting > 0:
                        x_atual = int.from_bytes(cereal.read(size=2))
                        y_atual = int.from_bytes(cereal.read(size=2))

                        x_atual = (x_atual - 0x10000) if x_atual > 0x7FFF else x_atual
                        y_atual = (y_atual - 0x10000) if y_atual > 0x7FFF else y_atual
                        print(x_atual, y_atual)
                    
                    if stop_flag.is_set():
                        break

                if stop_flag.is_set():
                    print('saiu')
                    cereal.write(stop)
                    break
                
    except serial.SerialException:
        print("\nNão foi possível comunicar com arduino. Confira a porta serial e tente novamente.")