"""Aviso temporal del ícono nuevo: solo celular, se cierra con "Entendido", caduca el 8 oct 2026."""
from herramientas import armar_pagina, url_archivo, nuevo_contexto

TITULO = 'Aviso temporal del ícono nuevo'
FIN = 1791525600000  # 2026-10-09T06:00:00Z


def correr(nav, r):
    ruta = armar_pagina('index.html', {'stats': {}}, 'aviso_icono.html')
    ctx = nuevo_contexto(nav, viewport={'width': 390, 'height': 844}); pg = ctx.new_page(); err = r.errores_de_pagina(pg, 'sin errores de JavaScript (aviso del ícono)')
    pg.goto(url_archivo(ruta)); pg.wait_for_timeout(300)
    hoy_valido = pg.evaluate('Date.now()') < FIN
    if hoy_valido:
        r.caso('celular: el aviso se ve', pg.is_visible('#avisoIcono'))
    texto = pg.text_content('#avisoIcono') or ''
    r.caso('el texto menciona la "G" (Android) y la "V" (iPhone)', '"G"' in texto and '"V"' in texto, texto.strip()[:90])
    pg.click('#avisoIcono >> text=Entendido'); pg.wait_for_timeout(100)
    r.caso('"Entendido" lo cierra', not pg.is_visible('#avisoIcono'))
    pg.reload(); pg.wait_for_timeout(300)
    r.caso('no vuelve a salir tras recargar', not pg.is_visible('#avisoIcono'))
    pg.evaluate('localStorage.clear()')
    pg.evaluate(f'Date.now = () => {FIN}; mostrarAvisoIcono()')
    r.caso('a partir del 9 oct (hora de México) ya no se muestra', not pg.is_visible('#avisoIcono'))
    pg.evaluate(f'Date.now = () => {FIN - 60000}; mostrarAvisoIcono()')
    r.caso('el 8 oct a las 23:59 (México) todavía se muestra', pg.is_visible('#avisoIcono'))
    err.revisar()
    ctx.close()
    ctx = nuevo_contexto(nav, viewport={'width': 1280, 'height': 900}); pg = ctx.new_page()
    pg.goto(url_archivo(ruta)); pg.wait_for_timeout(300)
    pg.evaluate(f'Date.now = () => {FIN - 60000}; mostrarAvisoIcono()')
    r.caso('computadora: el aviso no se muestra', not pg.is_visible('#avisoIcono'))
    ctx.close()
