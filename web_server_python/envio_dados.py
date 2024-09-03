import serial, time

__toleranciaX, __toleranciaY = 10, 10

def __organiza_coordenadas(header, x, y):
    msbX, lsbX = (x >> 8), (x & 255)
    msbY, lsbY = (y >> 8), (y & 255)

    return header + [msbX, lsbX, msbY, lsbY]

def envia_pontos(portaUSB : str, baudrate : int, data, start, stop, header, stop_flag) -> None:
    try:
        with serial.Serial(port=portaUSB, baudrate=baudrate) as cereal:
            time.sleep(6)

            # Envio das coordenadas iniciais
            x_atual, y_atual = 0, 0
            baites = __organiza_coordenadas(header, x_atual, y_atual)
            print("\nEnviando coordenadas iniciais!")
            cereal.write(baites)

            # Confirma o que foi enviado para o Arduino
            xx = int.from_bytes(cereal.read(size=2))
            yy = int.from_bytes(cereal.read(size=2))
            print(xx, yy)

            cereal.write(start)

            # Envio das coordenadas desejadas
            for x, y in data:
                baites = __organiza_coordenadas(header, x, y)
                print("\nEnviando dados!")
                cereal.write(baites)

                # Confirma o que foi enviado para o Arduino
                xx = int.from_bytes(cereal.read(size=2))
                yy = int.from_bytes(cereal.read(size=2))
                print(xx, yy)

                while ((abs(x - x_atual) > __toleranciaX) or (abs(y - y_atual) > __toleranciaY)):

                    if cereal.in_waiting > 0:
                        x_atual = int.from_bytes(cereal.read(size=2))
                        y_atual = int.from_bytes(cereal.read(size=2))

                        x_atual = (x_atual - 0x10000) if x_atual > 0x7FFF else x_atual
                        y_atual = (y_atual - 0x10000) if y_atual > 0x7FFF else y_atual
                        print(x_atual, y_atual)
                    
                    if stop_flag.is_set():
                        break

                if stop_flag.is_set():
                    print('Execucao interrompida.')
                    break

            if not stop_flag.is_set():
                print('Trajeto completo!')

            cereal.write(stop)  # de qualquer forma tem que printar stop, pro carrinho parar
                
    except serial.SerialException:
        print("\nNão foi possível comunicar com arduino. Confira a porta serial e tente novamente.")