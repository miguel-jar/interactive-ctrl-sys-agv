import ezdxf
from ezdxf.addons.drawing import Frontend, RenderContext
from ezdxf.addons.drawing import layout, svg
import json

pathJSON = "static/config.json"
pathSVG = "static/mapa.svg"
pathTempsSolid = "proc_mapa/sw_temps/"

def __get_lines(doc : ezdxf.document.Drawing):    
    msp = doc.modelspace()
    linhas = msp.query('LINE')
    retas = set()

    for e in linhas:
        x = (e.dxf.start[0], e.dxf.end[0])
        y = (e.dxf.start[1], e.dxf.end[1])
        retas.add((x, y))
    
    return retas

def __get_infos_solid(doc : ezdxf.document.Drawing):
    folhas = ['A0', 'A1', 'A2', 'A3', 'A4']
    msp = doc.modelspace()

    for c in msp.query("MTEXT"):
        if c.text in folhas: tipoFolha = c.text.lower()
        elif 'ESCALA:' in c.text: escala = c.text[7:].split(':')
    escalaReal = int(escala[1]) / int(escala[0])

    unidades = {4:'MM', 5:'CM', 6:'M'}
    unidadeDesenho = unidades[doc.header.get('$INSUNITS')]

    return tipoFolha, unidadeDesenho, escalaReal

def __norm_data(data, unit : str, drawScale):

    scale_conv_2_cm = {'MM': 0.1, 'CM':1, 'M': 100}  # padroniza em CM

    offset = min(data)  # normalizando em funçao do menor ponto de start
    offset_x, offset_y = offset[0][0], offset[1][0]

    rows = []
    for c in data:
        x = [(l - offset_x) * drawScale * scale_conv_2_cm[unit] for l in c[0]]
        y = [(l - offset_y) * drawScale * scale_conv_2_cm[unit] for l in c[1]]
        rows.append([x, y])

    return rows

def __export(points):
    doc = ezdxf.new()
    msp = doc.modelspace()

    minX, maxX = float('inf'), -float('inf')
    minY, maxY = float('inf'), -float('inf')

    for c in points:
        minX = min(minX, min(c[0]))
        maxX = max(maxX, max(c[0]))
        minY = min(minY, min(c[1]))
        maxY = max(maxY, max(c[1]))
        msp.add_line([c[0][0], c[1][0]], [c[0][1], c[1][1]])  # start point e end point

    maxSzPx = 1000
    width, height = maxX - minX, maxY - minY
    normScaleW , normScaleH = width / max(width, height), height / max(width, height)
    normWidth, normHeight = maxSzPx * normScaleW, maxSzPx * normScaleH
    args = {'maxSzPx':maxSzPx, 'widthCm':width, 'heightCm':height,
            'normWidthPx':int(normWidth), 'normHeightPx':int(normHeight)}
    
    with open(pathJSON, "w") as configs:
        json.dump(args, configs, indent=4)

    context = RenderContext(doc)
    backend = svg.SVGBackend()
    frontend = Frontend(context, backend)
    frontend.draw_layout(msp)
    page = layout.Page(width=normWidth , height=normHeight, units=layout.Units.px)
    svg_string = backend.get_string(page)
    with open(pathSVG, "wt", encoding="utf8") as fp:
        fp.write(svg_string)

def get_mapa(filename : str, solidwork : bool = True):
    doc = ezdxf.readfile(filename)
    retasArquivo = __get_lines(doc)

    if solidwork:
        tipoFolha, unidade, escala = __get_infos_solid(doc)

        doc2 = ezdxf.readfile(pathTempsSolid + tipoFolha + '.DXF')
        retasTemplate = __get_lines(doc2)

        mapa = retasArquivo - retasTemplate  # remove margens e legendas
        pontos = __norm_data(mapa, unidade, escala)
        __export(pontos)
        return pontos

    __export(retasArquivo)
    return retasArquivo

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    coordenadas = get_mapa('proc_mapa/mapas/corredor_predio_2.DXF')
    for linhas in coordenadas:
        x, y = linhas[0], linhas[1]
        plt.plot(x , y)
    plt.show()