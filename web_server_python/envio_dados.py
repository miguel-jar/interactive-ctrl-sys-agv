import serial, time, os
import matplotlib.pyplot as plt
import pandas as pd

def __organiza_coordenadas(header, x, y):
    msbX, lsbX = (x >> 8), (x & 255)
    msbY, lsbY = (y >> 8), (y & 255)

    return header + [msbX, lsbX, msbY, lsbY]

def save_fig(x_target, y_target, x_real, y_real, sv_path : str, sv_path_all : str):
    plt.plot(x_target, y_target)
    plt.plot(x_real, y_real)
    plt.legend(["Pontos desejados", "Trajetória percorrida"])
    plt.xlabel("X [CM]")
    plt.ylabel("Y [CM]")
    plt.grid()

    counter = 1
    path_img = sv_path_all.replace('*', f'{counter}.svg')
    while os.path.exists(path_img):
        counter += 1
        path_img = sv_path_all.replace('*', f'{counter}.svg')
        path_dados = sv_path_all.replace('*', f'{counter}_paradas.csv')
    
    plt.savefig(path_img)  # salva na pasta de histórico
    plt.savefig(sv_path)  # salva na pasta pra ver grafico no HTML
    plt.close()
    
    return path_dados

def envia_pontos(portaUSB : str, baudrate : int, origin, data, header, start, stop, stop_flag, sv_path : str, sv_path_all : str) -> None:
    try:
        with serial.Serial(port=portaUSB, baudrate=baudrate) as cereal:
            time.sleep(6)

            dados_paradas = {x_target: [], y_target: [], x_real:[], y_real:[]}
            
            # Envio das coordenadas iniciais
            baites = __organiza_coordenadas(header, origin[0], origin[1])
            print("\nEnviando coordenadas iniciais...")
            cereal.write(baites)
            cereal.write(start)

            # Envio das coordenadas desejadas
            x_target, y_target = [], []
            x_real, y_real = [], []

            for x, y in data:
                baites = __organiza_coordenadas(header, x, y)
                print("\nEnviando dados!")
                cereal.write(baites)

                x_target.append(x)
                y_target.append(y)

                while True:
                    if cereal.in_waiting > 0:
                        xx = int.from_bytes(cereal.read(size=2))
                        yy = int.from_bytes(cereal.read(size=2))

                        if xx == 32760 and yy == 32760:
                            # salvando dados assim que o robô chega no marco pra calcular EQM dps
                            dados_paradas['x_target'].append(x)
                            dados_paradas['y_target'].append(y)
                            dados_paradas['x_real'].append(xx[-1])
                            dados_paradas['y_real'].append(xx[-1])
                            break

                        xx = (xx - 0x10000) if xx > 0x7FFF else xx
                        yy = (yy - 0x10000) if yy > 0x7FFF else yy
                        print(xx, yy)

                        x_real.append(xx)
                        y_real.append(yy)

                    if stop_flag.is_set():
                        break

                if stop_flag.is_set():
                    print('Execucao interrompida.')
                    break
            
            if not stop_flag.is_set():
                print('Trajeto completo!')

            cereal.write(stop)  # de qualquer forma tem que printar stop, pro carrinho parar

            path_dados = save_fig(x_target, y_target, x_real, y_real, sv_path, sv_path_all)
            df = pd.DataFrame(data=dados_paradas)
            df.to_csv(path_or_buf=path_dados, header=False)
                
    except serial.SerialException:
        print("\nNão foi possível comunicar com arduino. Confira a porta serial e tente novamente.")