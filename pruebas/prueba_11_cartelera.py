"""Diseño "Noche y hora": cartelera agrupada por noche, hora grande, barritas de asientos y pestañas."""
from herramientas import armar_pagina, url_archivo, nuevo_contexto, ahora_ms, iso, DIA

TITULO = 'Diseño "Noche y hora": cartelera por noches'


def _su(n, mio=None):
    d = {f'u{i}': {'uid': f'u{i}', 'nick': f'J{i}', 'at': i} for i in range(1, n + 1)}
    if mio:
        d[mio] = {'uid': mio, 'nick': 'Yo', 'at': 99}
    return d


def correr(nav, r):
    now = ahora_ms()
    hoy = now + 2 * 3600 * 1000          # dentro de 2 h (hoy o, cerca de medianoche, mañana)
    pasado = now + 3 * DIA
    seed = {'vtes_records': {
        'a': {'type': 'custom_table', 'name': 'Pronto', 'utcTime': iso(hoy), 'utcMs': hoy, 'modality': 'virtual', 'ownerUid': 'u1', 'platform': 'Lackey', 'format': 'v5', 'signups': _su(3)},
        'b': {'type': 'custom_table', 'name': 'Después', 'utcTime': iso(pasado), 'utcMs': pasado, 'modality': 'virtual', 'ownerUid': 'u1', 'platform': 'Succubus', 'signups': _su(3, 'yo')},
        'c': {'type': 'custom_table', 'name': 'Misma noche', 'utcTime': iso(pasado + 60000), 'utcMs': pasado + 60000, 'modality': 'virtual', 'ownerUid': 'yo', 'signups': _su(1)},
    }, 'stats': {}}
    ctx = nuevo_contexto(nav, viewport={'width': 390, 'height': 844}); pg = ctx.new_page(); err = r.errores_de_pagina(pg)
    pg.goto(url_archivo(armar_pagina('index.html', seed, 'cartelera.html'))); pg.wait_for_timeout(400)
    pg.evaluate("window.__setUser({uid:'yo', displayName:'Yo'})"); pg.wait_for_timeout(300)

    cont = pg.query_selector('#customTablesContainer')
    encabezados = [h.inner_text() for h in cont.query_selector_all('h2')]
    r.caso('las mesas se agrupan por noche (2 noches → 2 encabezados)', len(encabezados) == 2, encabezados)
    r.caso('la noche de hoy o mañana se nombra así ("Hoy, …" o "Mañana, …")', bool(encabezados) and encabezados[0].split(',')[0] in ('Hoy', 'Mañana'), encabezados)
    orden = [a.get_attribute('id') for a in cont.query_selector_all('article')]
    r.caso('las mesas van en orden de hora', orden == ['card-custom-a', 'card-custom-b', 'card-custom-c'], orden)
    hora = pg.query_selector('#card-custom-a .font-display')
    r.caso('la hora es el elemento grande de cada mesa', hora is not None and ':' in hora.inner_text() and 'text-7xl' in (hora.get_attribute('class') or ''))
    r.caso('la mesa que empieza pronto resalta su hora en ámbar', 'text-lampara' in (hora.get_attribute('class') or ''))
    barras = pg.query_selector('#card-custom-a [role="img"]')
    r.caso('barritas de asientos con descripción: 3 de 5', barras is not None and barras.get_attribute('aria-label') == '3 de 5 asientos ocupados')
    b_barras = pg.query_selector_all('#card-custom-b [role="img"] span')
    clases = [x.get_attribute('class') for x in b_barras]
    r.caso('tu asiento se marca distinto (violeta) y los libres en gris', len(clases) == 5 and sum('bg-violet-300' in c for c in clases) == 1 and sum('bg-zinc-700' in c for c in clases) == 1, clases)
    meta_a = pg.inner_text('#card-custom-a')
    r.caso('plataforma y formato en texto ("LackeyCCG · V5")', 'LackeyCCG · V5' in meta_a)
    r.caso('"en 2 h" sin emojis', 'en 2 h' in meta_a and '⏰' not in meta_a)
    r.caso('estado junto a la hora ("Faltan 2 jugador(es)")', 'Faltan 2 jugador(es)' in meta_a)
    r.caso('"Organizas tú" en la mesa propia', 'Organizas tú' in pg.inner_text('#card-custom-c'))
    r.caso('la pestaña activa se marca (Virtual)', 'tab-activa' in pg.get_attribute('#modeVirtualBtn', 'class') and pg.get_attribute('#modeVirtualBtn', 'aria-pressed') == 'true')
    pg.evaluate("setTableModality('presencial')"); pg.wait_for_timeout(200)
    r.caso('al cambiar de pestaña se marca Presencial', 'tab-activa' in pg.get_attribute('#modePresencialBtn', 'class') and 'tab-inactiva' in pg.get_attribute('#modeVirtualBtn', 'class'))
    r.caso('el título del sitio es "Organizador VTES"', pg.inner_text('h1').strip() == 'Organizador VTES')
    ancho = pg.evaluate('document.documentElement.scrollWidth')
    r.caso('en celular (390 px) no hay desplazamiento horizontal', ancho <= 390, ancho)
    err.revisar()
    ctx.close()
