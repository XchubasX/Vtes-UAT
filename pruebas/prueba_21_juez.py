"""Tarjeta «Juez de reglas» (beta privada): arriba de Ligas, lleva a juez.eternalschedule.com/beta."""
from herramientas import armar_pagina, url_archivo, nuevo_contexto

TITULO = 'Tarjeta «Juez de reglas» (beta privada, arriba de Ligas)'


def correr(nav, r):
    ctx = nuevo_contexto(nav, viewport={'width': 390, 'height': 844})
    pg = ctx.new_page(); err = r.errores_de_pagina(pg, 'sin errores de JavaScript (tarjeta del juez)')
    pg.goto(url_archivo(armar_pagina('index.html', {'vtes_records': {}, 'stats': {}}, 'juez.html'))); pg.wait_for_timeout(400)
    t = pg.inner_text('#tarjetaJuez') if pg.is_visible('#tarjetaJuez') else ''
    r.caso('se ve la tarjeta «Juez de reglas»', 'Juez de reglas' in t, t)
    r.caso('dice «BETA PRIVADA · SOLICITA ACCESO»', 'BETA PRIVADA · SOLICITA ACCESO' in t, t)
    r.caso('va arriba de la tarjeta de Ligas',
           pg.evaluate("document.getElementById('tarjetaJuez').compareDocumentPosition(document.getElementById('tarjetaLigas')) & Node.DOCUMENT_POSITION_FOLLOWING") > 0)
    href = pg.get_attribute('#tarjetaJuez', 'href')
    r.caso('lleva a https://juez.eternalschedule.com/beta', href == 'https://juez.eternalschedule.com/beta', href)
    sobra = pg.evaluate('document.documentElement.scrollWidth - window.innerWidth')
    r.caso('con la tarjeta nada se sale de la pantalla (390 px)', sobra <= 1, sobra)
    err.revisar()
    ctx.close()
