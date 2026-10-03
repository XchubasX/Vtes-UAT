"""Mudanza a Cloudflare: enlaces por ciudad en cualquier dirección y publicación sin la carpeta de pruebas."""
import re
import shutil
import subprocess
import tempfile
from herramientas import REPO, TMP, nuevo_contexto

TITULO = 'Cloudflare: enlaces de ciudad en GitHub y en dominio propio; qué se publica'


def correr(nav, r):
    html = (REPO / '404.html').read_text(encoding='utf-8')
    m = re.search(r'function destino404[\s\S]*?\n  }\n', html)
    r.caso('404.html tiene la función que calcula a dónde redirigir', m is not None)
    ctx = nuevo_contexto(nav); pg = ctx.new_page(); pg.set_content('<p>x</p>')
    pg.add_script_tag(content=m.group(0))
    casos = [
        ('GitHub, sitio real con ciudad', 'xchubasx.github.io', '/Organizador-Vtes/Zaragoza', '/Organizador-Vtes/?city=Zaragoza'),
        ('GitHub, sitio de pruebas con ciudad', 'xchubasx.github.io', '/Vtes-UAT/Zaragoza', '/Vtes-UAT/?city=Zaragoza'),
        ('GitHub, ciudad con acento y espacio', 'xchubasx.github.io', '/Vtes-UAT/Ciudad%20de%20M%C3%A9xico', '/Vtes-UAT/?city=Ciudad%20de%20M%C3%A9xico'),
        ('GitHub, ciudad con diagonal final', 'xchubasx.github.io', '/Vtes-UAT/Zaragoza/', '/Vtes-UAT/?city=Zaragoza'),
        ('GitHub, página que no existe sin ciudad', 'xchubasx.github.io', '/Vtes-UAT/', '/Vtes-UAT/'),
        ('Cloudflare pages.dev con ciudad', 'elysium-uat.pages.dev', '/Zaragoza', '/?city=Zaragoza'),
        ('Dominio propio con ciudad', 'eternalschedule.com', '/Zaragoza', '/?city=Zaragoza'),
        ('Dominio propio con www y acento', 'www.eternalschedule.com', '/M%C3%A1laga', '/?city=M%C3%A1laga'),
        ('Dominio propio, raíz', 'eternalschedule.com', '/', '/'),
    ]
    for nombre, host, ruta, esperado in casos:
        got = pg.evaluate('([h, p]) => destino404(h, p)', [host, ruta])
        r.caso(f'404: {nombre} → {esperado}', got == esperado, got)
    ctx.close()

    # Lo que publica Cloudflare: correr el mismo script en una copia del repositorio
    copia = __import__('pathlib').Path(tempfile.mkdtemp(prefix='cf-', dir=TMP)) / 'repo'
    shutil.copytree(REPO, copia, ignore=shutil.ignore_patterns('.git', '__pycache__'))
    res = subprocess.run(['bash', 'cloudflare-publicar.sh'], cwd=copia, capture_output=True, text=True)
    r.caso('el script de publicación de Cloudflare termina sin errores', res.returncode == 0, res.stderr[-300:])
    pub = copia / 'publicado'
    nombres = {p.name for p in pub.iterdir()} if pub.exists() else set()
    r.caso('se publican las páginas y archivos del sitio',
           {'index.html', 'sorteo.html', 'estadisticas.html', '404.html', 'config.js', 'comun.js', 'js', 'iconos', 'manifest.webmanifest'} <= nombres, sorted(nombres))
    r.caso('NO se publica la carpeta de pruebas ni archivos internos',
           not ({'pruebas', 'README.md', '_config.yml', 'cloudflare-publicar.sh', '.git', '.claude', '.gitignore', 'publicado'} & nombres), sorted(nombres))
    r.caso('se publican todos los archivos de js/', sorted(p.name for p in (pub / 'js').iterdir()) == sorted(p.name for p in (REPO / 'js').iterdir()))
