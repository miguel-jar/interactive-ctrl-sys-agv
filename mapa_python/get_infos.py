import ezdxf

doc = ezdxf.readfile('tratamento_mapa_python\mapas\mapa.DXF')
msp = doc.modelspace()

textos = msp.query("MTEXT")

folhas = ['A0', 'A1', 'A2', 'A3', 'A4']  # Padrão ISO

for c in textos:
    texto = c.text

    if texto in folhas:
        tamanhoFolha = texto

    if 'ESCALA:' in texto:
        escala = texto[7:].split(':')

print(tamanhoFolha)
print(escala)

    