"""El sitio servido tal cual (como GitHub Pages), con sus archivos separados de verdad.

Solo se reemplazan los programas externos (Google, Tailwind, EmailJS, calendario)
por simulaciones. Detecta problemas de orden de carga, rutas o archivos faltantes
que las otras pruebas (que meten los archivos dentro de la página) no verían.
"""
import json
import re
from herramientas import nuevo_contexto, servidor, REPO, FIREBASE_SIMULADO, ahora_ms, iso, DIA

TITULO = 'Sitio servido como en GitHub, con sus archivos separados'


def correr(nav, r):
    fut = ahora_ms() + 3 * DIA
    seed = {'vtes_records': {'m1': {'type': 'custom_table', 'name': 'Mesa Real', 'utcTime': iso(fut), 'utcMs': fut, 'modality': 'virtual',
                                    'ownerUid': 'u1', 'signups': {'u1': {'uid': 'u1', 'nick': 'Ana', 'at': 1}}}}, 'stats': {}}
    sustitutos = {
        'firebase-app-compat': 'window.__SEED__=' + json.dumps(seed) + ';' + FIREBASE_SIMULADO,
        'cdn.tailwindcss.com': 'window.tailwind={};',
        'email.min.js': 'window.emailjs={init(){},send(){return Promise.resolve()}};',
        'flatpickr.min.js': 'window.flatpickr=function(){return{setDate(){},clear(){}}};',
    }
    locales = []

    def ruta(route):
        u = route.request.url
        if u.startswith('http://localhost'):
            if u.split('?')[0].endswith('.html') or u.split('?')[0].endswith('/'):
                # Quitar las huellas de integridad: nuestros sustitutos no coinciden con ellas (a propósito)
                resp = route.fetch()
                return route.fulfill(response=resp, body=re.sub(r' integrity="[^"]*"', '', resp.text()))
            return route.continue_()
        for clave, cuerpo in sustitutos.items():
            if clave in u:
                return route.fulfill(status=200, content_type='application/javascript', body=cuerpo)
        return route.fulfill(status=200, content_type='text/plain', body='')

    with servidor(REPO) as base:
        ctx = nuevo_contexto(nav)
        ctx.route('**/*', ruta)
        for archivo, espera in [('index.html', 'Mesa Real'), ('sorteo.html?tableId=m1', 'Ana'), ('estadisticas.html', None)]:
            pg = ctx.new_page(); err = r.errores_de_pagina(pg, f'{archivo}: sin errores de JavaScript')
            pg.on('response', lambda resp: resp.url.startswith('http://localhost') and locales.append((resp.url.split('?')[0].split('/', 3)[-1], resp.status)))
            pg.goto(base + archivo); pg.wait_for_timeout(700)
            err.revisar()
            if espera:
                r.caso(f'{archivo}: carga los datos ({espera})', espera in pg.inner_text('body'))
            pg.close()
        ctx.close()

    malos = sorted({x for x in locales if x[1] != 200})
    r.caso('todos los archivos propios responden (sin 404)', not malos, malos)
    cargados = {u.split('/', 1)[-1] for u, _ in locales}
    en_js = {f'js/{p.name}' for p in (REPO / 'js').glob('*.js')}
    r.caso('cada archivo de js/ se usa en la página principal', en_js <= cargados, sorted(en_js - cargados))
    r.caso('config.js y comun.js se cargan', {'config.js', 'comun.js'} <= cargados, sorted(cargados))
