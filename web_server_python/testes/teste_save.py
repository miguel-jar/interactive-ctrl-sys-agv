import matplotlib.pyplot as plt
import os, yaml

def save_fig(x_target, y_target, x_real, y_real, sv_path : str, sv_path_all : str):
    plt.plot(x_target, y_target)
    plt.plot(x_real, y_real)
    plt.legend(["Pontos desejados", "Trajetória percorrida"])
    plt.xlabel("X [CM]")
    plt.ylabel("Y [CM]")
    plt.grid()

    counter = 1
    path = sv_path_all.replace('*', str(counter))

    while os.path.exists(path):
        counter += 1
        path = sv_path_all.replace('*', str(counter))
    
    plt.savefig(path)
    plt.savefig(sv_path)

with open('configs.yaml', 'r') as arquivo:
    configs = yaml.load(arquivo, yaml.SafeLoader)

x = [10, 20, 30, 40]
y = [10, 20, 30, 40]

save_fig(x, y, y, x, configs['SAVE_PATH'], configs['SAVE_PATH_ALL'])