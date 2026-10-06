"""Mudanza a eternalschedule.com: franja en la dirección vieja y salto automático desde el 11 oct 2026."""
from herramientas import armar_pagina, url_archivo, nuevo_contexto, ahora_ms, iso, DIA

TITULO = 'Mudanza: franja en GitHub hasta el 10 oct y salto automático a eternalschedule.com'


def correr(nav, r):
    fut = ahora_ms() + 2 * DIA
    seed = {'vtes_records': {'v1': {'type': 'custom_table', 'name': 'Martes de V5', 'utcTime': iso(fut), 'utcMs': fut,
                                    'modality': 'virtual', 'platform': 'Lackey', 'format': 'v5', 'ownerUid': 'u9', 'signups': {}}}, 'stats': {}}
    ctx = nuevo_contexto(nav, viewport={'width': 390, 'height': 844})
    pg = ctx.new_page(); err = r.errores_de_pagina(pg, 'sin errores de JavaScript (mudanza)')
    pg.goto(url_archivo(armar_pagina('index.html', seed, 'mudanza.html'))); pg.wait_for_timeout(400)

    casos = [
        ('principal', 'xchubasx.github.io', '/Organizador-Vtes/', '', '', 'https://eternalschedule.com/'),
        ('sin diagonal final', 'xchubasx.github.io', '/Organizador-Vtes', '', '', 'https://eternalschedule.com/'),
        ('index.html', 'xchubasx.github.io', '/Organizador-Vtes/index.html', '', '', 'https://eternalschedule.com/'),
        ('enlace a mesa', 'xchubasx.github.io', '/Organizador-Vtes/', '', '#mesa-abc', 'https://eternalschedule.com/#mesa-abc'),
        ('ciudad', 'xchubasx.github.io', '/Organizador-Vtes/Zaragoza', '', '', 'https://eternalschedule.com/Zaragoza'),
        ('ciudad vía 404 (?city=)', 'xchubasx.github.io', '/Organizador-Vtes/', '?city=Zaragoza', '', 'https://eternalschedule.com/?city=Zaragoza'),
        ('sorteo con datos', 'xchubasx.github.io', '/Organizador-Vtes/sorteo.html', '?event=p1', '', 'https://eternalschedule.com/sorteo.html?event=p1'),
        ('estadísticas', 'xchubasx.github.io', '/Organizador-Vtes/estadisticas.html', '', '', 'https://eternalschedule.com/estadisticas.html'),
        ('sitio de pruebas en GitHub → uat', 'xchubasx.github.io', '/Vtes-UAT/Zaragoza', '', '', 'https://uat.eternalschedule.com/Zaragoza'),
    ]
    for nombre, host, ruta, q, h, esperado in casos:
        got = pg.evaluate('([h, r, q, a]) => mudanzaDestino(h, r, q, a)', [host, ruta, q, h])
        r.caso(f'destino: {nombre} → {esperado}', got == esperado, got)
    for nombre, host, ruta in [('eternalschedule.com', 'eternalschedule.com', '/'), ('uat.eternalschedule.com', 'uat.eternalschedule.com', '/Zaragoza'),
                               ('workers.dev', 'elysium.chubas.workers.dev', '/'), ('otro repositorio de GitHub', 'xchubasx.github.io', '/liga-vtes-cdmx/')]:
        r.caso(f'en {nombre} no hace nada (ni franja ni salto)', pg.evaluate('([h, r]) => mudanzaDestino(h, r, "", "")', [host, ruta]) is None)

    r.caso('fecha del salto: domingo 11 oct 2026, 00:00 hora de México', pg.evaluate("MUDANZA_REDIRIGE_DESDE === Date.parse('2026-10-11T06:00:00Z')"))
    r.caso('sábado 10 oct 23:59 (México) todavía no salta', not pg.evaluate("mudanzaDebeRedirigir(Date.parse('2026-10-11T05:59:00Z'))"))
    r.caso('domingo 11 oct 00:00 (México) ya salta', pg.evaluate("mudanzaDebeRedirigir(Date.parse('2026-10-11T06:00:00Z'))"))

    r.caso('fuera de GitHub NO se pone el contador de visitas', pg.evaluate("!document.querySelector('script[data-cf-beacon]')"))
    n = pg.evaluate("(() => { const s = mudanzaPonerContador(); return [s.src, JSON.parse(s.getAttribute('data-cf-beacon')).token]; })()")
    r.caso('el contador de la dirección vieja usa Cloudflare Web Analytics con su token', n[0] == 'https://static.cloudflareinsights.com/beacon.min.js' and n[1] == 'ad00e9d4434c4fb195d0bfbcd033696a', n)
    r.caso('fuera de GitHub la franja no aparece', not pg.is_visible('#avisoMudanza'))
    pg.evaluate("mostrarAvisoMudanza('https://eternalschedule.com/#mesa-v1')"); pg.wait_for_timeout(100)
    t = pg.inner_text('#avisoMudanza') if pg.is_visible('#avisoMudanza') else ''
    r.caso('en GitHub aparece la franja "Elysium se mudó a eternalschedule.com"', 'Elysium se mudó a eternalschedule.com' in t, t[:80])
    r.caso('la franja dice la fecha "domingo 11 de octubre"', 'domingo 11 de octubre' in t)
    r.caso('la franja explica entrar con Google una vez y volver a agregar el ícono', 'una vez' in t and 'pantalla de inicio' in t)
    r.caso('la franja no tiene botón de cerrar', 'Entendido' not in t and 'Cerrar' not in t)
    r.caso('el botón lleva a la misma página en la dirección nueva', pg.get_attribute('#avisoMudanzaBoton', 'href') == 'https://eternalschedule.com/#mesa-v1')
    pg.evaluate("mostrarAvisoMudanza('https://uat.eternalschedule.com/')"); pg.wait_for_timeout(50)
    r.caso('en el sitio de pruebas de GitHub la franja apunta a uat.eternalschedule.com',
           'uat.eternalschedule.com' in pg.inner_text('#avisoMudanzaDominio') and pg.inner_text('#avisoMudanzaBoton') == 'Ir a uat.eternalschedule.com')
    r.caso('la franja va arriba de las pestañas', pg.evaluate("document.getElementById('avisoMudanza').compareDocumentPosition(document.getElementById('modeVirtualBtn')) & Node.DOCUMENT_POSITION_FOLLOWING") > 0)
    sobra = pg.evaluate('document.documentElement.scrollWidth - window.innerWidth')
    r.caso('con la franja nada se sale de la pantalla (390 px)', sobra <= 1, sobra)
    err.revisar()
    ctx.close()
