"""Aviso de bienvenida, estado de la mesa, botones accesibles, letra mínima, "Cargando" y error de conexión."""
import re
from herramientas import armar_pagina, url_archivo, nuevo_contexto, ahora_ms, iso, DIA, REPO

TITULO = 'Aviso de bienvenida y experiencia de uso'


def _signups(n):
    return {f'u{i}': {'uid': f'u{i}', 'nick': f'J{i}', 'at': i} for i in range(1, n + 1)}


def correr(nav, r):
    # --- Aviso de bienvenida
    ctx = nuevo_contexto(nav); pg = ctx.new_page(); err = r.errores_de_pagina(pg, 'sin errores de JavaScript (aviso)')
    ruta = armar_pagina('index.html', {'stats': {}}, 'aviso.html')
    pg.goto(url_archivo(ruta)); pg.wait_for_timeout(300)
    r.caso('sin sesión se ve el aviso de bienvenida', pg.is_visible('#loginNotice'))
    r.caso('botón grande "Entrar con Google" visible', pg.is_visible('#authBar button'))
    pg.click('#loginNotice >> text=Entendido'); pg.wait_for_timeout(100)
    r.caso('"Entendido" oculta el aviso', not pg.is_visible('#loginNotice'))
    pg.reload(); pg.wait_for_timeout(300)
    r.caso('el aviso no vuelve tras recargar', not pg.is_visible('#loginNotice'))
    pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(300)
    pg.click('#loginNotice >> text=Entrar con Google'); pg.wait_for_timeout(100)
    r.caso('el botón del aviso abre el inicio de sesión', pg.is_visible('#loginModal'))
    pg.click('#loginModalBtn'); pg.wait_for_timeout(300)
    r.caso('con sesión desaparecen el aviso y el botón', not pg.is_visible('#loginNotice') and 'Cerrar sesión' in pg.inner_text('#authBar'))
    err.revisar()
    ctx.close()

    # --- Estado de la mesa y botones
    fut = ahora_ms() + 3 * DIA
    seed = {'vtes_records': {
        'm4': {'type': 'custom_table', 'name': 'Cuatro', 'utcTime': iso(fut), 'utcMs': fut, 'modality': 'virtual', 'ownerUid': 'u1', 'signups': _signups(4)},
        'm5': {'type': 'custom_table', 'name': 'Cinco', 'utcTime': iso(fut), 'utcMs': fut, 'modality': 'virtual', 'ownerUid': 'u1', 'signups': _signups(6)},
        'p1': {'type': 'custom_table', 'name': 'Presencial', 'utcTime': iso(fut), 'utcMs': fut, 'modality': 'presencial', 'originTz': 'America/Mexico_City',
               'venue': 'T', 'city': 'CDMX', 'country': 'México', 'ownerUid': 'u1',
               'signups': {'u1': {'uid': 'u1', 'nick': 'J1', 'arrival': '18:00', 'at': 1}, 'u2': {'uid': 'u2', 'nick': 'J2', 'at': 2}}}},
        'stats': {}}
    ctx = nuevo_contexto(nav, viewport={'width': 390, 'height': 844}); pg = ctx.new_page(); err = r.errores_de_pagina(pg, 'sin errores de JavaScript (tarjetas)')
    pg.goto(url_archivo(armar_pagina('index.html', seed, 'experiencia.html'))); pg.wait_for_timeout(400)
    t4 = pg.inner_text('#card-custom-m4'); t5 = pg.inner_text('#card-custom-m5')
    r.caso('con 4 jugadores dice "Lista para jugar" y "4 de 5"', 'Lista para jugar' in t4 and '4 de 5' in t4)
    r.caso('con 5 jugadores dice "Mesa llena" y "5 de 5"', 'Mesa llena' in t5 and '5 de 5' in t5)
    r.caso('mesa del ícono con 4: 4 lugares iluminados, 1 libre y centro verde',
           pg.eval_on_selector('#card-custom-m4 .cupo-mesa svg', "s => [s.querySelectorAll('.lugar-ocupado').length, s.querySelectorAll('.lugar-libre').length, s.querySelector('circle').getAttribute('stroke')]") == [4, 1, '#22C55E'])
    r.caso('mesa del ícono con 5: los 5 lugares iluminados',
           pg.eval_on_selector('#card-custom-m5 .cupo-mesa svg', "s => [s.querySelectorAll('.lugar-ocupado').length, s.querySelectorAll('.lugar-libre').length]") == [5, 0])
    r.caso('el dibujo se oculta a lectores de pantalla (el texto ya lo dice)', pg.get_attribute('#card-custom-m4 .cupo-mesa svg', 'aria-hidden') == 'true')
    r.caso('ya no aparece "Mesa Completa"', 'Completa' not in pg.inner_text('#customTablesContainer'))
    pequenos = []
    for rel in ['index.html', 'sorteo.html'] + [f'js/{p.name}' for p in sorted((REPO / 'js').glob('*.js'))]:
        pequenos += [rel] * len(re.findall(r'text-\[1[01]px\]', (REPO / rel).read_text(encoding='utf-8')))
    r.caso('no quedan textos de 10–11 px', not pequenos, pequenos)
    pg.evaluate("window.__setUser({uid:'u1',displayName:'J1'})"); pg.wait_for_timeout(300)
    xs = pg.query_selector_all('#card-custom-m4 button[title="Remover jugador"]')
    r.caso('botones × con descripción para lectores de pantalla', len(xs) == 3 and all((x.get_attribute('aria-label') or '').startswith('Quitar a J') for x in xs), len(xs))
    r.caso('zona táctil ampliada en ×', bool(xs) and 'py-1.5' in xs[0].get_attribute('class'))
    sub = pg.query_selector('#card-custom-m5 button[title="Quitar suplente"]')
    r.caso('quitar suplente con descripción', sub is not None and 'suplentes' in (sub.get_attribute('aria-label') or ''))
    pg.evaluate("setTableModality('presencial')"); pg.wait_for_timeout(300)
    ed = pg.query_selector_all('#card-custom-p1 button[title="Editar hora de llegada"]')
    r.caso('✏️ más grande y con descripción', len(ed) == 2 and 'py-1.5' in ed[0].get_attribute('class') and bool(ed[0].get_attribute('aria-label')))
    r.caso('💬 con descripción', pg.get_attribute('button[onclick="openFeedbackModal()"]', 'aria-label') == 'Reportar un bug o sugerencia')
    err.revisar()
    ctx.close()

    # --- "Cargando" mientras llegan los datos, y error de conexión
    def con_lectura(modo):
        js = ("setTimeout(()=>errcb&&errcb(new Error('permission_denied')),200);" if modo == 'falla'
              else "setTimeout(()=>on(ev,cb,errcb),1500);")
        extra = """<script>(function(){const orig=firebase.database; firebase.database=function(){const d=orig.apply(this,arguments); const r=d.ref.bind(d);
          d.ref=function(p){const ref=r(p); if(p==='vtes_records'){const on=ref.on.bind(ref); ref.on=function(ev,cb,errcb){ %s }; } return ref;}; return d;};})();</script>""" % js
        return armar_pagina('index.html', seed, f'lectura_{modo}.html', extra_head=extra)
    ctx = nuevo_contexto(nav)
    pg = ctx.new_page(); err = r.errores_de_pagina(pg, 'sin errores de JavaScript (carga lenta)')
    pg.goto(url_archivo(con_lectura('lenta'))); pg.wait_for_timeout(300)
    r.caso('mientras llegan los datos dice "Cargando mesas…"', 'Cargando mesas' in pg.inner_text('#customTablesContainer'))
    pg.evaluate("setTableModality('presencial')"); pg.wait_for_timeout(100)
    r.caso('al cambiar de pestaña sigue diciendo "Cargando" (no "no hay mesas")', 'Cargando mesas' in pg.inner_text('#customTablesContainer'))
    pg.wait_for_timeout(1700)
    r.caso('al llegar los datos aparecen las mesas', 'Presencial' in pg.inner_text('#customTablesContainer'))
    err.revisar()
    pg = ctx.new_page(); err = r.errores_de_pagina(pg, 'sin errores de JavaScript (sin conexión)')
    pg.goto(url_archivo(con_lectura('falla'))); pg.wait_for_timeout(500)
    t = pg.inner_text('#customTablesContainer')
    r.caso('si Firebase falla muestra "No se pudo conectar" y botón para recargar', 'No se pudo conectar' in t and 'Volver a cargar' in t)
    err.revisar()
    ctx.close()
