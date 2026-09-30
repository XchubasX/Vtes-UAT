"""Herramientas comunes para las pruebas del Organizador VTES.

Las pruebas abren las páginas reales del repositorio en un navegador automatizado
(Playwright + Chromium) con Firebase simulado, así que no tocan ninguna base de
datos real ni necesitan internet. Ver pruebas/README.md.
"""
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent          # carpeta del sitio
PRUEBAS = Path(__file__).resolve().parent
TMP = Path(tempfile.mkdtemp(prefix='vtes-pruebas-'))  # páginas armadas para cada corrida
ZONA = 'America/Mexico_City'                          # zona horaria fija del navegador de prueba

FIREBASE_SIMULADO = (PRUEBAS / 'firebase-simulado.js').read_text(encoding='utf-8')

# Sustitutos de los programas externos (no hay internet en las pruebas)
STUBS_EXTERNOS = """<style>.hidden{display:none !important}</style>
<script>
window.tailwind = {};
window.__sent = [];
window.emailjs = { init(o){ window.__ejsInit = o; }, send(s, t, p){ window.__sent.push(p); return Promise.resolve(); } };
window.flatpickr = function(sel, opts){ const el = document.querySelector(sel); return {
  setDate(d){ if (el && d) { const x = new Date(d); el.value = x.getFullYear()+'-'+String(x.getMonth()+1).padStart(2,'0')+'-'+String(x.getDate()).padStart(2,'0')+' '+String(x.getHours()).padStart(2,'0')+':'+String(x.getMinutes()).padStart(2,'0'); } },
  clear(){ if (el) el.value = ''; } }; };
</script>"""


# ---------------------------------------------------------------------------
# Fechas
# ---------------------------------------------------------------------------
def ahora_ms():
    return int(time.time() * 1000)


def iso(ms):
    return datetime.fromtimestamp(ms / 1000, timezone.utc).isoformat().replace('+00:00', 'Z')


DIA = 24 * 3600 * 1000


# ---------------------------------------------------------------------------
# Armar una página de prueba
# ---------------------------------------------------------------------------
def meter_archivos_propios(html, raiz=REPO):
    """Mete config.js, comun.js y js/*.js dentro de la página (en el mismo lugar
    y orden en que la página los carga)."""
    def sub(m):
        texto = (raiz / m.group(1)).read_text(encoding='utf-8')
        return '<script>' + texto.replace('</script>', '<\\/script>') + '</script>'
    return re.sub(r'<script src="((?:config|comun)\.js|js/[a-z]+\.js)\?v=[^"]*"></script>', sub, html)


def armar_pagina(archivo, seed=None, nombre=None, extra_head='', config_extra=None, raiz=REPO):
    """Devuelve la ruta de una copia de `archivo` lista para probar:
    archivos propios dentro, programas externos reemplazados y Firebase simulado."""
    html = (raiz / archivo).read_text(encoding='utf-8')
    html = meter_archivos_propios(html, raiz)
    if config_extra:
        for a, b in config_extra:
            html = html.replace(a, b)
    html = re.sub(r'<script src="https?://[^"]*"[^>]*></script>', '', html)
    html = re.sub(r'<link [^>]*>', '', html)
    semilla = '<script>window.__SEED__ = ' + json.dumps(seed or {'stats': {}}) + ';</script>'
    html = html.replace('<head>', '<head>' + STUBS_EXTERNOS + semilla + '<script>' + FIREBASE_SIMULADO + '</script>' + extra_head, 1)
    destino = TMP / (nombre or ('p_' + archivo))
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(html, encoding='utf-8')
    return destino


def url_archivo(ruta, sufijo=''):
    return 'file://' + str(ruta) + sufijo


# ---------------------------------------------------------------------------
# Servidor web local (para probar como lo publica GitHub Pages)
# ---------------------------------------------------------------------------
def _puerto_libre():
    s = socket.socket(); s.bind(('127.0.0.1', 0)); p = s.getsockname()[1]; s.close(); return p


@contextmanager
def servidor(carpeta_sitio, nombre='Vtes-UAT'):
    """Sirve `carpeta_sitio` en http://localhost:PUERTO/<nombre>/ y devuelve esa dirección."""
    raiz = Path(tempfile.mkdtemp(prefix='vtes-web-', dir=TMP))
    os.symlink(carpeta_sitio, raiz / nombre)
    puerto = _puerto_libre()
    proc = subprocess.Popen([sys.executable, '-m', 'http.server', str(puerto), '--bind', '127.0.0.1', '--directory', str(raiz)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(50):
            try:
                socket.create_connection(('127.0.0.1', puerto), timeout=0.2).close(); break
            except OSError:
                time.sleep(0.1)
        yield f'http://localhost:{puerto}/{nombre}/'
    finally:
        proc.terminate()


# ---------------------------------------------------------------------------
# Registro de resultados
# ---------------------------------------------------------------------------
class Grupo:
    """Resultados de un grupo de pruebas. `r.caso(nombre, condición, detalle)`."""

    def __init__(self, titulo):
        self.titulo = titulo
        self.casos = []  # (nombre, ok, detalle)

    def caso(self, nombre, ok, detalle=''):
        ok = bool(ok)
        self.casos.append((nombre, ok, '' if ok else str(detalle)))
        print(('  ✅ ' if ok else '  ❌ ') + nombre + ('' if ok else f'  → {detalle}'))
        return ok

    def errores_de_pagina(self, pagina, nombre='sin errores de JavaScript'):
        """Conecta un registro de errores a la página; llamar a .revisar() al final."""
        errores = []
        pagina.on('pageerror', lambda e: errores.append(str(e)))
        grupo = self

        class _R:
            def revisar(self_inner, etiqueta=nombre):
                grupo.caso(etiqueta, not errores, '; '.join(errores[:3]))
        return _R()

    @property
    def ok(self):
        return all(c[1] for c in self.casos)


def nuevo_contexto(navegador, **kw):
    kw.setdefault('timezone_id', ZONA)
    ctx = navegador.new_context(**kw)
    ctx.set_default_timeout(5000)  # si algo no aparece, fallar rápido en vez de esperar 30 s
    return ctx


def limpiar():
    shutil.rmtree(TMP, ignore_errors=True)
