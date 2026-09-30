"""Revisiones del código sin abrir el navegador: sintaxis, versiones ?v=, huellas de integridad y orden de carga."""
import re
import shutil
import subprocess
from herramientas import REPO, TMP

TITULO = 'Revisión del código: sintaxis, versiones e integridad'


def correr(nav, r):
    node = shutil.which('node')
    archivos = ['config.js', 'comun.js'] + [f'js/{p.name}' for p in sorted((REPO / 'js').glob('*.js'))]
    for rel in archivos:
        if not node:
            r.caso(f'{rel}: sintaxis correcta', False, 'no está instalado node'); continue
        p = subprocess.run([node, '--check', str(REPO / rel)], capture_output=True, text=True)
        r.caso(f'{rel}: sintaxis correcta', p.returncode == 0, p.stderr.strip()[:200])
    for pagina in ['index.html', 'sorteo.html', 'estadisticas.html']:
        html = (REPO / pagina).read_text(encoding='utf-8')
        if node:
            bloques = re.findall(r'<script>(.*?)</script>', html, re.S)
            malos = []
            for i, b in enumerate(bloques):
                f = TMP / f'chk_{pagina}_{i}.js'; f.write_text(b, encoding='utf-8')
                p = subprocess.run([node, '--check', str(f)], capture_output=True, text=True)
                if p.returncode: malos.append(p.stderr.strip()[:150])
            r.caso(f'{pagina}: sintaxis correcta del código dentro de la página', not malos, malos)
        propios = re.findall(r'<script src="((?:config|comun)\.js|js/[a-z]+\.js)\?v=([^"]+)"></script>', html)
        faltan = [f for f, _ in propios if not (REPO / f).exists()]
        r.caso(f'{pagina}: todos los archivos propios que carga existen', not faltan, faltan)
        r.caso(f'{pagina}: carga config.js antes que comun.js', [f for f, _ in propios][:2] == ['config.js', 'comun.js'], [f for f, _ in propios][:2])
        cuerpo = re.search(r'^<body\b', html, re.M).start()  # la etiqueta real, no un comentario que la mencione
        r.caso(f'{pagina}: config.js y comun.js van dentro del <body> (App Check lo necesita)', all(html.index(f'src="{f}?') > cuerpo for f in ['config.js', 'comun.js']))
        externos = re.findall(r'<(?:script src|link rel="stylesheet" href)="(https://cdn\.jsdelivr\.net/[^"]+)"([^>]*)>', html)
        sin_huella = [u for u, resto in externos if 'integrity="sha256-' not in resto]
        r.caso(f'{pagina}: los programas de jsDelivr tienen versión fija y huella de integridad', not sin_huella and all('@' in u for u, _ in externos), sin_huella)
        if pagina == 'index.html':
            orden = [f for f, _ in propios if f.startswith('js/')]
            r.caso('index.html: arranque.js se carga al final', bool(orden) and orden[-1] == 'js/arranque.js', orden)
            versiones = {v for f, v in propios if f.startswith('js/')}
            r.caso('index.html: todos los archivos de js/ con la misma versión ?v=', len(versiones) == 1, versiones)
    vers = {}
    for pagina in ['index.html', 'sorteo.html', 'estadisticas.html']:
        for f, v in re.findall(r'<script src="((?:config|comun)\.js)\?v=([^"]+)"></script>', (REPO / pagina).read_text(encoding='utf-8')):
            vers.setdefault(f, set()).add(v)
    r.caso('las 3 páginas usan la misma versión ?v= de config.js y comun.js', all(len(v) == 1 for v in vers.values()), vers)
