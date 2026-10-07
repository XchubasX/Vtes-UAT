"""Página de estadísticas: acceso con Google (administrador y lectores) y panel de personas."""
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from herramientas import armar_pagina, url_archivo, nuevo_contexto, ZONA

TITULO = 'Página de estadísticas: acceso y conteo de personas'


def _mes(delta, dia):
    """Fecha ISO del día `dia` del mes actual + `delta` meses (fechas relativas: la prueba no caduca).
    "Mes actual" en la zona del navegador de prueba (no en UTC): la página cuenta los meses
    con la hora de quien la ve, y al final de cada mes UTC ya va en el mes siguiente."""
    hoy = datetime.now(ZoneInfo(ZONA))
    y, m = hoy.year, hoy.month + delta
    while m <= 0:
        m += 12; y -= 1
    return f'{y:04d}-{m:02d}-{dia:02d}T20:00:00Z'


def _ficha(fecha, uids, owner, mod='virtual'):
    return {'modality': mod, 'startAt': fecha, 'players': {u.lower(): u for u in uids}, 'uids': {u: True for u in uids}, 'owner': owner}


def correr(nav, r):
    # --- Acceso
    seed = {'admins': {'uidA': True}, 'statsReaders': {'uidC': True},
            'stats': {'virtualJoins': 3, 'tablesLog': {'t1': {'modality': 'virtual', 'startAt': _mes(0, 1), 'players': {'ana': 'Ana'}, 'format': 'v5'}}}}
    ctx = nuevo_contexto(nav); pg = ctx.new_page(); err = r.errores_de_pagina(pg, 'sin errores de JavaScript (acceso)')
    pg.goto(url_archivo(armar_pagina('estadisticas.html', seed, 'est_acceso.html'))); pg.wait_for_timeout(300)
    r.caso('sin sesión: botón "Entrar con Google" y sin datos', pg.is_visible('#gateLoginBtn') and not pg.is_visible('#statsContent'))
    r.caso('no hay campo de contraseña', pg.locator('#gatePassword').count() == 0)
    pg.evaluate("window.__setUser({uid:'uidB', displayName:'Beto'})"); pg.wait_for_timeout(300)
    r.caso('cuenta sin permiso: mensaje "sin acceso" y Cerrar sesión', 'no tiene acceso' in pg.inner_text('#gateMsg') and pg.is_visible('#gateSignOutBtn') and not pg.is_visible('#statsContent'))
    pg.evaluate("window.__setUser({uid:'uidC', displayName:'Coordinador'})"); pg.wait_for_timeout(300)
    r.caso('un lector de estadísticas ve los datos', pg.is_visible('#statsContent'))
    r.caso('el lector no borra ni escribe nada', pg.evaluate('window.__writes.length') == 0)
    pg.evaluate("window.__setUser({uid:'uidB', displayName:'Beto'})"); pg.wait_for_timeout(300)
    r.caso('al cambiar a una cuenta sin permiso se ocultan los datos', not pg.is_visible('#statsContent'))
    pg.click('#gateSignOutBtn'); pg.wait_for_timeout(200)
    r.caso('cerrar sesión regresa al botón de entrar', pg.is_visible('#gateLoginBtn'))
    pg.click('#gateLoginBtn'); pg.wait_for_timeout(400)  # el inicio simulado entra como uidA (administrador)
    r.caso('el administrador ve las estadísticas', pg.is_visible('#statsContent') and not pg.is_visible('#gateSection'))
    r.caso('se dibujan las cifras', len(pg.inner_text('#kpis')) > 0)
    r.caso('avisos: sin datos dice «Todavía nadie ha activado los avisos»', 'Todavía nadie ha activado los avisos' in pg.inner_text('[aria-labelledby="hAvisos"]'))
    err.revisar()
    ctx.close()

    # --- ¿Se usan los avisos? (tablero 25)
    from datetime import timedelta
    hace = lambda d: (datetime.now(timezone.utc) - timedelta(days=d)).strftime('%Y-%m-%dT%H:%M:%SZ')
    seed_av = {'admins': {'uidA': True}, 'stats': {
        'avisos': {'personas': 3, 'aparatos': 4, 'tipos': {'iphone': 1, 'android': 2, 'pc': 0, 'sinDato': 1}, 'minutos': {'m15': 1, 'm30': 3}, 'actualizado': 1},
        'tablesLog': {'a': _ficha(hace(3), ['u1', 'u2', 'u3'], 'u4'), 'b': _ficha(hace(10), ['u5', 'u1'], 'u1'),
                      'viejo': _ficha(hace(45), ['u9'], 'u9'), 'pres': _ficha(hace(2), ['p1', 'p2'], 'p1', 'presencial')}}}
    ctx = nuevo_contexto(nav); pg = ctx.new_page(); err = r.errores_de_pagina(pg, 'sin errores de JavaScript (avisos en estadísticas)')
    pg.goto(url_archivo(armar_pagina('estadisticas.html', seed_av, 'est_avisos.html'))); pg.wait_for_timeout(300)
    pg.click('#gateLoginBtn'); pg.wait_for_timeout(400)
    t = pg.inner_text('[aria-labelledby="hAvisos"]')
    tn = ' '.join(t.split())  # cada número va en su propia pastilla: se juntan los renglones
    r.caso('avisos: «Personas con avisos» 3 de 5 que jugaron virtuales en 30 días (60%)', 'Personas con avisos' in t and 'de 5 personas que jugaron mesas virtuales en los últimos 30 días (60%)' in t, t)
    r.caso('avisos: «Aparatos con avisos» 4', 'Aparatos con avisos\n4' in t, t)
    r.caso('avisos: tipo de aparato con Android 2 (50%), iPhone 1 y «Sin dato» 1', 'Android 2 (50%)' in tn and 'iPhone 1 (25%)' in tn and 'Sin dato 1 (25%)' in tn, tn)
    r.caso('avisos: 30 minutos 3 (75%) y 15 minutos 1 (25%)', '30 minutos 3 (75%)' in tn and '15 minutos 1 (25%)' in tn, tn)
    r.caso('avisos: explica «Sin dato» y que no se guarda quién es quién', 'Sin dato»: aparatos' in t and 'No se guarda quién es quién' in t, t)
    r.caso('avisos: el recuadro va después de «¿Se usan los suplentes?»',
           pg.evaluate("document.getElementById('hSubs').compareDocumentPosition(document.getElementById('hAvisos')) & Node.DOCUMENT_POSITION_FOLLOWING") > 0)
    pg.set_viewport_size({'width': 390, 'height': 844}); pg.wait_for_timeout(200)
    r.caso('avisos: nada se sale de la pantalla en celular (390 px)', pg.evaluate("document.documentElement.scrollWidth - window.innerWidth") <= 1, pg.evaluate("document.documentElement.scrollWidth"))
    err.revisar()
    ctx.close()

    # --- Personas (fechas relativas al mes actual)
    tl = {'a1': _ficha(_mes(-2, 5), ['A', 'B', 'C'], 'A'), 'a2': _ficha(_mes(-2, 20), ['A', 'C'], 'A'),
          'b1': _ficha(_mes(-1, 3), ['A', 'B', 'D'], 'B'), 'b2': _ficha(_mes(-1, 17), ['D'], 'A', 'presencial'),
          'c1': _ficha(_mes(0, 2), ['A', 'E', 'F'], 'A'), 'c2': _ficha(_mes(0, 3), ['E'], 'E'),
          'old': {'modality': 'virtual', 'startAt': _mes(-3, 10), 'players': {'x': 'X'}}}
    ctx = nuevo_contexto(nav, viewport={'width': 1100, 'height': 900}); pg = ctx.new_page(); err = r.errores_de_pagina(pg, 'sin errores de JavaScript (personas)')
    pg.goto(url_archivo(armar_pagina('estadisticas.html', {'admins': {'uidA': True}, 'stats': {'tablesLog': tl}}, 'est_personas.html'))); pg.wait_for_timeout(200)
    pg.evaluate("window.__setUser({uid:'uidA'})"); pg.wait_for_timeout(500)
    k = pg.inner_text('#peopleKpis')
    r.caso('personas este mes: 3 (A, E, F)', 'Personas este mes\n3' in k, k.replace('\n', ' | '))
    r.caso('personas nuevas este mes: 2 (E, F)', 'nuevas este mes\n2' in k, k.replace('\n', ' | '))
    r.caso('regresaron: 1 de las 3 del mes pasado (33%)', '33%' in k and '1 de las 3' in k, k.replace('\n', ' | '))
    r.caso('personas que organizan en 3 meses: 3 (A, B, E)', 'Personas que organizan\n3' in k, k.replace('\n', ' | '))
    err.revisar()
    pg2 = ctx.new_page(); err2 = r.errores_de_pagina(pg2, 'sin errores de JavaScript (sin datos de cuentas)')
    pg2.goto(url_archivo(armar_pagina('estadisticas.html', {'admins': {'uidA': True}, 'stats': {'tablesLog': {'old': tl['old']}}}, 'est_vacio.html'))); pg2.wait_for_timeout(200)
    pg2.evaluate("window.__setUser({uid:'uidA'})"); pg2.wait_for_timeout(500)
    r.caso('sin datos de cuentas: mensaje de espera', 'Todavía no hay mesas registradas con cuentas' in pg2.inner_text('#chartPeople'))
    err2.revisar()
    ctx.close()
