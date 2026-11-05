"""Botón «Juez de reglas» (beta privada): en la misma línea que Ligas, lleva a juez.eternalschedule.com/beta."""
from herramientas import armar_pagina, url_archivo, nuevo_contexto

TITULO = 'Botón «Juez de reglas» (beta privada, en la misma línea que Ligas)'


def correr(nav, r):
    ctx = nuevo_contexto(nav, viewport={'width': 390, 'height': 844})
    pg = ctx.new_page(); err = r.errores_de_pagina(pg, 'sin errores de JavaScript (botón del juez)')
    pg.goto(url_archivo(armar_pagina('index.html', {'vtes_records': {}, 'stats': {}}, 'juez.html'))); pg.wait_for_timeout(400)
    t = pg.inner_text('#tarjetaJuez') if pg.is_visible('#tarjetaJuez') else ''
    r.caso('se ve el botón «Juez de reglas»', 'Juez de reglas' in t, t)
    r.caso('va antes del botón de Ligas',
           pg.evaluate("document.getElementById('tarjetaJuez').compareDocumentPosition(document.getElementById('tarjetaLigas')) & Node.DOCUMENT_POSITION_FOLLOWING") > 0)
    r.caso('los botones de Juez y Ligas comparten el mismo contenedor',
           pg.evaluate("document.getElementById('tarjetaJuez').parentElement === document.getElementById('tarjetaLigas').parentElement"))
    href = pg.get_attribute('#tarjetaJuez', 'href')
    r.caso('lleva a https://juez.eternalschedule.com/beta', href == 'https://juez.eternalschedule.com/beta', href)
    sobra = pg.evaluate('document.documentElement.scrollWidth - window.innerWidth')
    r.caso('con el botón nada se sale de la pantalla (390 px)', sobra <= 1, sobra)
    err.revisar()
    ctx.close()
