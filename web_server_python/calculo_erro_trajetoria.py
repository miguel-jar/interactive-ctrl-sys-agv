import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np

def __obter_paths_do_grupo(svg_file, grupo_id):
    # Carregar o arquivo SVG
    tree = ET.parse(svg_file)
    root = tree.getroot()

    # Espaço de nomes (namespace) padrão para SVG
    ns = {'svg': 'http://www.w3.org/2000/svg'}

    # Encontrar o grupo pelo ID
    grupo = root.find(f".//svg:g[@id='{grupo_id}']", ns)

    # Obter todos os paths dentro do grupo
    if grupo is not None:
        paths = grupo.findall('.//svg:path', ns)
        return paths
    else:
        return None
    
def obter_coordenadas_paths(svg_file, ids):

    xxx, yyy = [], []

    for id in ids:
        paths = __obter_paths_do_grupo(svg_file, id)
        
        xx, yy = [], []
        if paths is not None:
            for path in paths:
                dados = path.attrib['d'].split()
                            
                x = dados[1::3]
                y = dados[2::3]

                x = list(map(lambda z: float(z), x))
                y = list(map(lambda z: -float(z), y))
                
                #plt.plot(x, y)
                
                xx.append(x)
                yy.append(y)
                
        else:
            print("Grupo não encontrado ou não contém caminhos.")
                
        xxx.append(xx)
        yyy.append(yy)
        
    return xxx, yyy

if __name__ == "__main__":
    svg_file = "trajetos/06_10/55.svg"  # Substitua pelo caminho do seu arquivo SVG
    ids = ["line2d_25", "line2d_26"]   # Substitua pelo ID do grupo que você deseja obter

    # plt.plot(xxx[0][0], yyy[0][0])
    
    xxx, yyy = obter_coordenadas_paths(svg_file, ids)
    
    xt, yt = xxx[0][0], yyy[0][0]
    xr, yr = xxx[1][0], yyy[1][0]
    
    distancias_x, distancias_y = [], []
    for d in range(1, len(xt)):
        dx = abs(xt[d-1] - xt[d])
        dy = abs(yt[d-1] - yt[d])
        # ddd = (dx ** 2 + dy ** 2) ** (1/2)
        distancias_x.append(dx)
        distancias_y.append(dy)

    escala_x = 1000 / max(distancias_x)
    escala_y = 1000 / (distancias_y[0] + distancias_y[1])  # soma pq tem 2 trechos que dão a maior distância
    offset_x = min(xxx[0][0])
    offset_y = min(yyy[0][0])

    xt = [(j - offset_x) * escala_x for j in xt] 
    yt = [(j - offset_y) * escala_y for j in yt]
    plt.plot(xt, yt)
    
    xr = [(j - offset_x) * escala_x for j in xr] 
    yr = [(j - offset_y) * escala_y for j in yr]
    plt.plot(xr, yr)

    o = 0
    erros, error = [], [0] * len(xt)
    
    for f, g in zip(xr, yr):
        dx, dy = f - xt[o], g - yt[o]
        e = (dx ** 2 + dy ** 2) ** (1 / 2)
        if e < 18:
            error[o] = e ** 2 # eleva ao quadrado pra calcular o EQM
            o = o + 1 if o < len(xt) - 1 else len(xt) - 1
            
        erros.append(e)
    
    eqm = sum(error) / len(error)
    reqm = eqm ** (1 / 2)
    e_medio = sum([ee ** (1 / 2) for ee in error]) / len(error)
    
    print("\nEQM =", eqm)
    print("REQM =", reqm)
    print("Erro médio absoluto =", e_medio)
        
    plt.figure()
    plt.plot(erros)
    plt.show()