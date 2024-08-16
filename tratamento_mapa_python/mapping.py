import ezdxf

compFolhas = {'A0':1189, 'A1':841, 'A2':594, 'A3':420, 'A4':290}  # Padrão ISO

def get_map(filename : str):
    doc = ezdxf.readfile(filename)
    msp = doc.modelspace()

    linhas = msp.query("LINE")

    maxDistancia = 0
    retasMain = set()
    for e in linhas:
        x1, x2 = e.dxf.start[0], e.dxf.end[0]
        y1, y2 = e.dxf.start[1], e.dxf.end[1]

        if x1 == x2:
            maxDistancia = max(maxDistancia, abs(y1 - y2))
        elif y1 == y2:
            maxDistancia = max(maxDistancia, abs(x1 - x2))
        
        retasMain.add((x1, y1, x2, y2))

    # print(maxDistancia)

    if compFolhas['A1'] < maxDistancia <= compFolhas['A0']:
        pathArquivo = 'tratamento_mapa_python/solid_templates/a0.DXF'
    elif compFolhas['A2'] < maxDistancia <= compFolhas['A1']:
        pathArquivo = 'tratamento_mapa_python/solid_templates/a1.DXF'
    elif compFolhas['A3'] < maxDistancia <= compFolhas['A2']:
        pathArquivo = 'tratamento_mapa_python/solid_templates/a2.DXF'
    elif compFolhas['A4'] < maxDistancia <= compFolhas['A3']:
        pathArquivo = 'tratamento_mapa_python/solid_templates/a3.DXF'
    elif maxDistancia <= compFolhas['A4']:
        pathArquivo = 'tratamento_mapa_python/solid_templates/a4.DXF'

    # print(pathArquivo)

    doc2 = ezdxf.readfile(pathArquivo)
    msp2 = doc2.modelspace()

    cabecalhoTemplate = msp2.query("LINE")

    retasTemplate = set()
    for e in cabecalhoTemplate:
        x1, x2 = e.dxf.start[0], e.dxf.end[0]
        y1, y2 = e.dxf.start[1], e.dxf.end[1]
        
        retasTemplate.add((x1, y1, x2, y2))

    mapa = retasMain - retasTemplate
    offset = min(mapa)

    linhas = []
    rr = set()

    for c in mapa:
        x = [c[0] - offset[0], c[2] - offset[0]]
        y = [c[1]- offset[1], c[3]- offset[1]]

        rr.add('{x:' + str(x[0]) + ', y:' + str(y[0]) + '},')
        rr.add('{x:' + str(x[1]) + ', y:' + str(y[1]) + '},')

        linhas.append([x, y])
    
    for c in rr:
        print(c)

    return linhas

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    coordenadas = get_map('tratamento_mapa_python/mapas/mapa.DXF')
    for linhas in coordenadas:
        x, y = linhas[0], linhas[1]
        plt.plot(x , y)
    plt.show()