import ezdxf

from ezdxf.addons.drawing import Frontend, RenderContext
from ezdxf.addons.drawing import layout, svg

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
    folhas = {'A0':'mapa_python/sw_temp/a0.DXF', 
              'A1':'mapa_python/sw_temp/a1.DXF',
              'A2':'mapa_python/sw_temp/a2.DXF',
              'A3':'mapa_python/sw_temp/a3.DXF', 
              'A4':'mapa_python/sw_temp/a4.DXF'}

    msp = doc.modelspace()

    for c in msp.query("MTEXT"):
        if c.text in folhas.keys(): caminhoModeloBase = folhas[c.text]
        elif 'ESCALA:' in c.text: escala = c.text[7:].split(':')
    escalaReal = int(escala[1]) / int(escala[0])

    unidades = {4:'MM', 5:'CM', 6:'M'}
    unidadeDesenho = unidades[doc.header.get('$INSUNITS')]

    return caminhoModeloBase, unidadeDesenho, escalaReal

def __norm_data(data, unit : str = 'CM', scale = 1):

    scale_conv_2_cm = {'MM': 0.1, 'CM':1, 'M': 100}

    offset = min(data)  # normalizando em funçao do menor ponto de start
    offset_x, offset_y = offset[0][0], offset[1][0]

    rows = []
    for c in data:
        x = [(l - offset_x) * scale * scale_conv_2_cm[unit] for l in c[0]]
        y = [(l - offset_y) * scale * scale_conv_2_cm[unit] for l in c[1]]
        rows.append([x, y])

    return rows

def export(points):
    doc = ezdxf.new()
    msp = doc.modelspace()
    for c in points:
        msp.add_line([c[0][0], c[1][0]], [c[0][1], c[1][1]])  # start point e end point

    context = RenderContext(doc)
    backend = svg.SVGBackend()
    frontend = Frontend(context, backend)
    frontend.draw_layout(msp)
    page = layout.Page(0, 0, layout.Units.cm)

    svg_string = backend.get_string(page)
    with open("web_server_python\static\output.svg", "wt", encoding="utf8") as fp:
        fp.write(svg_string)

def get_map(filename : str, solidwork : bool = True):
    doc = ezdxf.readfile(filename)
    retasArquivo = __get_lines(doc)

    if solidwork:
        caminho, unidade, escala = __get_infos_solid(doc)

        doc2 = ezdxf.readfile(caminho)
        retasTemplate = __get_lines(doc2)

        mapa = retasArquivo - retasTemplate  # remove margens e legendas
        pontos = __norm_data(mapa, unidade, escala)
        export(pontos)
        return pontos

    export(retasArquivo)
    return retasArquivo

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    coordenadas = get_map('mapa_python/mapas/mapa.DXF')
    for linhas in coordenadas:
        x, y = linhas[0], linhas[1]
        plt.plot(x , y)
    plt.show()