"""Botón «Ligas y torneos»: arriba de las pestañas; pruebas → uat-ligas, producción → ligas."""
from herramientas import armar_pagina, url_archivo, nuevo_contexto

TITULO = 'Botón «Ligas y torneos» (enlace al sitio de ligas del mismo entorno)'


def correr(nav, r):
    ctx = nuevo_contexto(nav, viewport={'width': 390, 'height': 844})
    pg = ctx.new_page(); err = r.errores_de_pagina(pg, 'sin errores de JavaScript (botón de ligas)')
    pg.goto(url_archivo(armar_pagina('index.html', {'vtes_records': {}, 'stats': {}}, 'ligas.html'))); pg.wait_for_timeout(400)
    t = pg.inner_text('#tarjetaLigas') if pg.is_visible('#tarjetaLigas') else ''
    r.caso('se ve el botón «Ligas y torneos»', 'Ligas y torneos' in t, t)
    clases = pg.get_attribute('#tarjetaLigas', 'class')
    r.caso('el botón pide al menos 44 px de alto para tocarlo fácil', 'min-h-[44px]' in clases, clases)
    r.caso('va arriba de las pestañas Virtual / Presencial',
           pg.evaluate("document.getElementById('tarjetaLigas').compareDocumentPosition(document.getElementById('modeVirtualBtn')) & Node.DOCUMENT_POSITION_FOLLOWING") > 0)
    href = pg.get_attribute('#tarjetaLigas', 'href')
    r.caso('en el sitio de pruebas lleva a uat-ligas.eternalschedule.com (nunca a producción)', href == 'https://uat-ligas.eternalschedule.com', href)
    r.caso('en el sitio real llevaría a ligas.eternalschedule.com',
           pg.evaluate("(() => { const a = VTES_CONFIG.esPruebas; VTES_CONFIG.esPruebas = false; const u = enlaceLigas(); VTES_CONFIG.esPruebas = a; return u; })()") == 'https://ligas.eternalschedule.com')
    sobra = pg.evaluate('document.documentElement.scrollWidth - window.innerWidth')
    r.caso('con el botón nada se sale de la pantalla (390 px)', sobra <= 1, sobra)
    err.revisar()
    ctx.close()
