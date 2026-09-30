"""Página de estadísticas: acceso con Google (administrador y lectores) y panel de personas."""
from datetime import datetime, timezone
from herramientas import armar_pagina, url_archivo, nuevo_contexto

TITULO = 'Página de estadísticas: acceso y conteo de personas'


def _mes(delta, dia):
    """Fecha ISO del día `dia` del mes actual + `delta` meses (fechas relativas: la prueba no caduca)."""
    hoy = datetime.now(timezone.utc)
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
