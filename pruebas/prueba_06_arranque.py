"""Arranque de la página principal: enlace por ciudad (/Zaragoza), enlace directo (#mesa-…), zona horaria."""
import shutil
from herramientas import armar_pagina, nuevo_contexto, servidor, ahora_ms, iso, DIA, TMP

TITULO = 'Arranque: enlace por ciudad y enlace directo a una mesa'


def correr(nav, r):
    fut = ahora_ms() + 3 * DIA
    seed = {'vtes_records': {
        'pz': {'type': 'custom_table', 'name': 'Evento Zaragoza', 'utcTime': iso(fut), 'utcMs': fut, 'modality': 'presencial', 'originTz': 'Europe/Madrid',
               'venue': 'T', 'city': 'Zaragoza', 'country': 'España', 'ownerUid': 'u1', 'signups': {}},
        'pm': {'type': 'custom_table', 'name': 'Evento CDMX', 'utcTime': iso(fut), 'utcMs': fut, 'modality': 'presencial', 'originTz': 'America/Mexico_City',
               'venue': 'T', 'city': 'CDMX', 'country': 'México', 'ownerUid': 'u1', 'signups': {}},
        'vv': {'type': 'custom_table', 'name': 'Mesa Virtual', 'utcTime': iso(fut), 'utcMs': fut, 'modality': 'virtual', 'ownerUid': 'u1', 'signups': {}}},
        'stats': {}}
    sitio = TMP / 'sitio_arranque'
    sitio.mkdir(exist_ok=True)
    shutil.copy(armar_pagina('index.html', seed, 'arranque.html'), sitio / 'index.html')
    with servidor(sitio) as base:
        ctx = nuevo_contexto(nav)
        pg = ctx.new_page(); err = r.errores_de_pagina(pg, 'sin errores de JavaScript (enlace por ciudad)')
        pg.goto(base + '?city=Zaragoza'); pg.wait_for_timeout(400)  # así llega desde 404.html
        t = pg.inner_text('#customTablesContainer')
        r.caso('enlace por ciudad: abre Presencial filtrado a Zaragoza', 'Evento Zaragoza' in t and 'Evento CDMX' not in t and 'Mesa Virtual' not in t, t[:120])
        r.caso('enlace por ciudad: deja la dirección limpia (/Zaragoza)', pg.url.endswith('/Zaragoza'), pg.url)
        err.revisar()
        pg = ctx.new_page(); err = r.errores_de_pagina(pg, 'sin errores de JavaScript (enlace directo)')
        pg.goto(base + '#mesa-pm'); pg.wait_for_timeout(500)
        r.caso('enlace directo: abre la pestaña correcta y muestra la mesa', pg.is_visible('#card-custom-pm'))
        tz = pg.evaluate("document.getElementById('userTimezone').textContent")
        r.caso('al arrancar escribe la zona horaria de quien visita (con nombre legible)', tz == 'Tu zona horaria: Ciudad de México (America/Mexico_City)', tz)
        r.caso('la zona horaria está dentro de la ventana Acerca de, no en el encabezado', pg.evaluate("!!document.querySelector('#aboutModal #userTimezone') && !document.querySelector('header #userTimezone')"))
        r.caso('el encabezado solo tiene el título y la sesión (sin subtítulo ni "?")', pg.evaluate("document.querySelector('header').children.length") == 2 and 'Coordinador' not in pg.inner_text('header'))
        err.revisar()
        ctx.close()
