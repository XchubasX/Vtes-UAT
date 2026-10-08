"""Mudanza a eternalschedule.com: franja en la dirección vieja, salto automático (desde el 8 oct 2026) y aviso «¿Despertando del Torpor?»."""
import shutil
from herramientas import armar_pagina, url_archivo, nuevo_contexto, ahora_ms, iso, DIA, TMP, servidor

TITULO = 'Mudanza: salto automático a eternalschedule.com y aviso «¿Despertando del Torpor?»'


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

    for nombre, host, origen, ruta, ciudad, esperado in [
        ('sitio viejo', 'xchubasx.github.io', 'https://xchubasx.github.io', '/Organizador-Vtes/', False, 'https://eternalschedule.com/'),
        ('sitio viejo sin diagonal final', 'xchubasx.github.io', 'https://xchubasx.github.io', '/Organizador-Vtes', False, 'https://eternalschedule.com/'),
        ('sitio viejo con ciudad', 'xchubasx.github.io', 'https://xchubasx.github.io', '/Organizador-Vtes/Zaragoza', True, 'https://eternalschedule.com/'),
        ('pruebas viejo', 'xchubasx.github.io', 'https://xchubasx.github.io', '/Vtes-UAT/', False, 'https://uat.eternalschedule.com/'),
        ('eternalschedule.com', 'eternalschedule.com', 'https://eternalschedule.com', '/', False, 'https://eternalschedule.com/'),
        ('eternalschedule.com con ciudad', 'eternalschedule.com', 'https://eternalschedule.com', '/Zaragoza', True, 'https://eternalschedule.com/'),
        ('uat.eternalschedule.com', 'uat.eternalschedule.com', 'https://uat.eternalschedule.com', '/', False, 'https://uat.eternalschedule.com/')]:
        got = pg.evaluate('([h, o, p, c]) => siteBaseUrlFor(h, o, p, c)', [host, origen, ruta, ciudad])
        r.caso(f'enlace de invitación desde {nombre} → {esperado}', got == esperado, got)

    r.caso('fecha del salto (adelantada): jueves 8 oct 2026, 15:00 hora de México', pg.evaluate("MUDANZA_REDIRIGE_DESDE === Date.parse('2026-10-08T21:00:00Z')"))
    r.caso('jueves 8 oct 14:59 (México) todavía no salta', not pg.evaluate("mudanzaDebeRedirigir(Date.parse('2026-10-08T20:59:00Z'))"))
    r.caso('jueves 8 oct 15:00 (México) ya salta', pg.evaluate("mudanzaDebeRedirigir(Date.parse('2026-10-08T21:00:00Z'))"))
    r.caso('hoy (ahora mismo) ya salta', pg.evaluate("mudanzaDebeRedirigir(Date.now())"))
    r.caso('las 3 páginas cargan la versión nueva de mudanza.js', all('mudanza.js?v=20261008b' in open(f).read() for f in ['index.html','sorteo.html','estadisticas.html']))

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
    torpor(nav, r, seed)


IPHONE = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
ANDROID = 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Mobile Safari/537.36'


def torpor(nav, r, seed):
    """Aviso «¿Despertando del Torpor?» al llegar desde la dirección vieja (8 oct 2026)."""
    pagina = armar_pagina('index.html', seed, 'torpor.html')
    ctx = nuevo_contexto(nav, viewport={'width': 390, 'height': 844})
    pg = ctx.new_page(); err = r.errores_de_pagina(pg, 'sin errores de JavaScript (aviso Torpor)')
    pg.goto(url_archivo(pagina)); pg.wait_for_timeout(300)
    for url, esperado in [('https://eternalschedule.com/', 'https://eternalschedule.com/?desde=github'),
                          ('https://eternalschedule.com/#mesa-abc', 'https://eternalschedule.com/?desde=github#mesa-abc'),
                          ('https://eternalschedule.com/?city=Zaragoza', 'https://eternalschedule.com/?city=Zaragoza&desde=github'),
                          ('https://eternalschedule.com/sorteo.html?event=p1', 'https://eternalschedule.com/sorteo.html?event=p1&desde=github')]:
        got = pg.evaluate('u => mudanzaConMarca(u)', url)
        r.caso(f'el salto agrega la marca: {url} → {esperado}', got == esperado, got)
    inv = pg.evaluate("siteBaseUrlFor('xchubasx.github.io', 'https://xchubasx.github.io', '/Organizador-Vtes/', false)")
    r.caso('las invitaciones NO llevan la marca', 'desde' not in inv, inv)
    r.caso('sin la marca el aviso Torpor no aparece', not pg.is_visible('#avisoTorpor'))

    pg.goto(url_archivo(pagina, '?desde=github#mesa-v1')); pg.wait_for_timeout(400)
    r.caso('al llegar con la marca aparece el aviso Torpor', pg.is_visible('#avisoTorpor'))
    t = pg.inner_text('#avisoTorpor') if pg.is_visible('#avisoTorpor') else ''
    r.caso('título «¿Despertando del Torpor?»', '¿Despertando del Torpor?' in t, t[:60])
    r.caso('dice que Elysium cambió de sede a eternalschedule.com', 'cambió de sede' in t and 'eternalschedule.com' in t)
    r.caso('pide actualizar favoritos y volver a agregar a la pantalla de inicio', 'favoritos' in t and 'pantalla de inicio' in t)
    r.caso('tiene los botones «Cómo agregarla» y «Entendido»', 'Cómo agregarla' in t and 'Entendido' in t)
    r.caso('la marca se borra de la barra de direcciones', 'desde' not in pg.evaluate('location.search'), pg.evaluate('location.href'))
    r.caso('el enlace a la mesa (#mesa-v1) se conserva', pg.evaluate('location.hash') == '#mesa-v1', pg.evaluate('location.hash'))
    r.caso('el aviso va arriba de las pestañas', pg.evaluate("document.getElementById('avisoTorpor').compareDocumentPosition(document.getElementById('modeVirtualBtn')) & Node.DOCUMENT_POSITION_FOLLOWING") > 0)
    sobra = pg.evaluate('document.documentElement.scrollWidth - window.innerWidth')
    r.caso('con el aviso nada se sale de la pantalla (390 px)', sobra <= 1, sobra)
    pg.reload(); pg.wait_for_timeout(300)
    r.caso('si recarga sin cerrarlo, el aviso sigue (aún no lo ha visto)', pg.is_visible('#avisoTorpor'))
    pg.click('#avisoTorporCerrar'); pg.wait_for_timeout(100)
    r.caso('«Entendido» lo cierra', not pg.is_visible('#avisoTorpor'))
    pg.goto(url_archivo(pagina, '?desde=github')); pg.wait_for_timeout(300)
    r.caso('ya visto: aunque vuelva a llegar desde la dirección vieja, no sale otra vez', not pg.is_visible('#avisoTorpor'))
    err.revisar(); ctx.close()

    sitio = TMP / 'sitio_torpor'
    sitio.mkdir(exist_ok=True)
    shutil.copy(pagina, sitio / 'index.html')
    with servidor(sitio) as base:
        ctx = nuevo_contexto(nav, viewport={'width': 390, 'height': 844})
        pg = ctx.new_page(); err = r.errores_de_pagina(pg, 'sin errores de JavaScript (aviso Torpor con ciudad)')
        pg.goto(base + '?city=Zaragoza&desde=github'); pg.wait_for_timeout(400)  # así llega desde 404.html
        r.caso('con ciudad (?city=Zaragoza) también aparece el aviso', pg.is_visible('#avisoTorpor'))
        r.caso('con ciudad, el filtro de ciudad sigue funcionando (pestaña Presencial)', 'bg-wine-600' in (pg.get_attribute('#modePresencialBtn', 'class') or ''))
        r.caso('con ciudad, la dirección queda limpia (/Zaragoza, sin la marca)', pg.url.endswith('/Zaragoza'), pg.url)
        err.revisar(); ctx.close()

    ctx = nuevo_contexto(nav, viewport={'width': 390, 'height': 844})
    pg = ctx.new_page(); err = r.errores_de_pagina(pg, 'sin errores de JavaScript (marca en sorteo)')
    sorteo = armar_pagina('sorteo.html', seed, 'torpor_sorteo.html')
    pg.goto(url_archivo(sorteo, '?desde=github')); pg.wait_for_timeout(300)
    r.caso('llegando al sorteo: la marca se borra de la dirección', 'desde' not in pg.evaluate('location.search'))
    r.caso('llegando al sorteo: el aviso queda pendiente para la página principal', pg.evaluate("localStorage.getItem('elysium_torpor_pendiente')") == '1')
    pg.goto(url_archivo(pagina)); pg.wait_for_timeout(300)
    r.caso('al pasar después a la página principal, aparece el aviso', pg.is_visible('#avisoTorpor'))
    err.revisar(); ctx.close()

    for nombre, ua, ver_iphone, ver_android, ancho in [('iPhone', IPHONE, True, False, 390), ('Android', ANDROID, False, True, 412), ('computadora', None, True, True, 1280)]:
        kw = {'viewport': {'width': ancho, 'height': 844}}
        if ua: kw['user_agent'] = ua
        ctx = nuevo_contexto(nav, **kw)
        pg = ctx.new_page(); err = r.errores_de_pagina(pg, f'sin errores de JavaScript (guía en {nombre})')
        pg.goto(url_archivo(pagina, '?desde=github')); pg.wait_for_timeout(300)
        pg.click('#avisoTorporGuia'); pg.wait_for_timeout(150)
        r.caso(f'{nombre}: «Cómo agregarla» abre la guía', pg.is_visible('#guiaAgregarElysium'))
        r.caso(f'{nombre}: muestra los pasos de iPhone = {ver_iphone} y de Android = {ver_android}',
               pg.is_visible('#guiaAgregarIPhone') == ver_iphone and pg.is_visible('#guiaAgregarAndroid') == ver_android)
        g = pg.inner_text('#guiaAgregarElysium')
        r.caso(f'{nombre}: la guía incluye «Borra el ícono viejo» y entrar con Google', 'Borra el ícono viejo' in g and 'Google' in g)
        r.caso(f'{nombre}: al abrir la guía el aviso se cierra para siempre', not pg.is_visible('#avisoTorpor') and pg.evaluate("localStorage.getItem('elysium_torpor_visto')") == '1')
        pg.click('#guiaAgregarElysium button'); pg.wait_for_timeout(100)
        r.caso(f'{nombre}: «Entendido» cierra la guía', not pg.is_visible('#guiaAgregarElysium'))
        err.revisar(); ctx.close()
