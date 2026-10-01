"""Ícono del sitio y datos para instalarlo en el celular (manifest.webmanifest)."""
import json, re
from PIL import Image
from herramientas import REPO, servidor, nuevo_contexto

TITULO = 'Ícono del sitio e instalación en el celular'


def correr(nav, r):
    m = json.loads((REPO / 'manifest.webmanifest').read_text(encoding='utf-8'))
    r.caso('manifest: nombre completo "VTES Matchmaking" y corto "VTESMatch"', m.get('name') == 'VTES Matchmaking' and m.get('short_name') == 'VTESMatch', m)
    r.caso('manifest: abre en el navegador normal (el inicio de sesión de Google sigue funcionando)', m.get('display') == 'browser')
    r.caso('manifest: empieza y se queda en la carpeta del sitio', m.get('start_url') == './' and m.get('scope') == './')
    tam = {}
    for ic in m.get('icons', []):
        f = REPO / ic['src']
        ok = f.exists() and Image.open(f).size == tuple(int(x) for x in ic['sizes'].split('x'))
        tam[ic['src'] + ' ' + ic.get('purpose', '')] = ok
    r.caso('manifest: íconos 192, 512 y versión recortable, con su tamaño real', len(tam) == 3 and all(tam.values()), tam)
    for f, px in [('iconos/apple-touch-icon.png', 180), ('iconos/favicon-32.png', 32)]:
        r.caso(f'{f} existe y mide {px}×{px}', (REPO / f).exists() and Image.open(REPO / f).size == (px, px))
    r.caso('iconos/favicon.svg es un dibujo válido', (REPO / 'iconos/favicon.svg').read_text().startswith('<svg'))
    for pagina in ['index.html', 'sorteo.html', 'estadisticas.html']:
        h = (REPO / pagina).read_text(encoding='utf-8')
        head = h[:h.index('</head>')]
        enlaces = all(x in head for x in ['rel="icon" href="iconos/favicon.svg"', 'rel="apple-touch-icon"', 'rel="manifest" href="manifest.webmanifest"', 'name="theme-color"'])
        r.caso(f'{pagina}: enlaza ícono, ícono de iPhone y manifest en el <head>', enlaces)
    # Servido como sitio: el navegador encuentra y lee todo
    with servidor(REPO) as base:
        ctx = nuevo_contexto(nav); pg = ctx.new_page()
        estados = {}
        for ruta in ['manifest.webmanifest', 'iconos/favicon.svg', 'iconos/favicon-32.png', 'iconos/apple-touch-icon.png', 'iconos/icono-192.png', 'iconos/icono-512.png']:
            estados[ruta] = pg.request.get(base + ruta).status
        r.caso('sitio servido: todos los archivos del ícono responden (200)', all(v == 200 for v in estados.values()), estados)
        ctx.close()
