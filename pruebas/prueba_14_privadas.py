"""Mesas privadas (solo virtuales): plegadas al final, se despliegan, cualquiera se une, el organizador cambia la privacidad."""
from herramientas import armar_pagina, url_archivo, nuevo_contexto, ahora_ms, iso, DIA

TITULO = 'Mesas privadas: plegadas al final de la lista'


def correr(nav, r):
    t1, t2, t3 = ahora_ms() + DIA, ahora_ms() + 2 * DIA, ahora_ms() + 3 * DIA
    seed = {'vtes_records': {
        'priv': {'type': 'custom_table', 'name': 'Solo los de siempre', 'utcTime': iso(t1), 'utcMs': t1, 'modality': 'virtual',
                 'platform': 'Lackey', 'format': 'v5', 'discord': 'vtes.gg/amigos', 'gamePassword': 'x', 'ownerUid': 'uidO', 'privada': True,
                 'signups': {'uidO': {'uid': 'uidO', 'nick': 'Org', 'at': 1}}},
        'pub': {'type': 'custom_table', 'name': 'Mesa abierta', 'utcTime': iso(t3), 'utcMs': t3, 'modality': 'virtual',
                'platform': 'Lackey', 'ownerUid': 'uidO', 'signups': {}},
        'pub2': {'type': 'custom_table', 'name': 'Otra abierta', 'utcTime': iso(t2), 'utcMs': t2, 'modality': 'virtual',
                 'platform': 'Lackey', 'ownerUid': 'uidO', 'signups': {}}},
        'stats': {}}
    ruta = armar_pagina('index.html', seed, 'privadas.html')
    ctx = nuevo_contexto(nav, viewport={'width': 390, 'height': 844}); pg = ctx.new_page(); err = r.errores_de_pagina(pg, 'sin errores de JavaScript (mesas privadas)')
    pg.goto(url_archivo(ruta)); pg.wait_for_timeout(300)

    orden = pg.eval_on_selector_all('#customTablesContainer > [id^=card-custom-]', 'els => els.map(e => e.id.replace("card-custom-", ""))')
    r.caso('las públicas van primero por hora y la privada al final (aunque sea antes)', orden == ['pub2', 'pub', 'priv'], orden)
    fila = pg.inner_text('#card-custom-priv')
    r.caso('plegada: una línea con "Privada", nombre y cupo', 'Privada' in fila and 'Solo los de siempre' in fila and '1/5' in fila, fila.replace('\n', ' | '))
    r.caso('plegada: no muestra Discord ni botones', 'vtes.gg/amigos' not in fila and 'Unirme' not in fila)
    r.caso('plegada: avisa a lectores de pantalla que se puede abrir', pg.get_attribute('#card-custom-priv', 'aria-expanded') == 'false')

    pg.click('#card-custom-priv'); pg.wait_for_timeout(150)
    card = pg.inner_text('#card-custom-priv')
    r.caso('al tocarla se despliega la tarjeta completa', 'vtes.gg/amigos' in card and 'Contraseña' in card and 'Ocultar' in card)
    r.caso('desplegada: lleva la etiqueta "Privada" junto al nombre', 'Privada' in pg.inner_text('#card-custom-priv h3'))
    r.caso('desplegada: cualquiera ve "¡Unirme a esta Mesa!"', '¡Unirme a esta Mesa!' in card)
    r.caso('sin sesión no se ve "Hacer pública"', 'Hacer pública' not in card)

    pg.click('#card-custom-priv >> text=Ocultar'); pg.wait_for_timeout(150)
    r.caso('"Ocultar" la vuelve a plegar', 'vtes.gg/amigos' not in pg.inner_text('#card-custom-priv'))

    # Cualquiera puede unirse a una privada
    pg.click('#card-custom-priv'); pg.wait_for_timeout(100)
    pg.click('#card-custom-priv >> text=¡Unirme a esta Mesa!'); pg.wait_for_timeout(100)
    pg.click('#loginModalBtn'); pg.wait_for_timeout(300)
    pg.fill('#joinNick', 'Ana'); pg.click('#joinSubmitBtn'); pg.wait_for_timeout(300)
    su = pg.evaluate('window.__store()')['vtes_records']['priv'].get('signups', {})
    r.caso('una persona cualquiera se une a la mesa privada', 'uidA' in su, su)
    r.caso('después de unirse la mesa sigue desplegada', 'vtes.gg/amigos' in pg.inner_text('#card-custom-priv'))

    # El organizador cambia la privacidad
    pg.evaluate("window.__setUser({uid:'uidO', displayName:'Org'})"); pg.wait_for_timeout(300)
    r.caso('el organizador ve "Hacer pública"', 'Hacer pública' in pg.inner_text('#card-custom-priv'))
    pg.click('#card-custom-priv >> text=Hacer pública'); pg.wait_for_timeout(100); pg.click('#uiDialogConfirm'); pg.wait_for_timeout(300)
    rec = pg.evaluate('window.__store()')['vtes_records']['priv']
    r.caso('"Hacer pública" quita el dato privada', 'privada' not in rec, rec.get('privada'))
    orden = pg.eval_on_selector_all('#customTablesContainer > [id^=card-custom-]', 'els => els.map(e => e.id.replace("card-custom-", ""))')
    r.caso('ya pública, vuelve a su lugar por hora', orden == ['priv', 'pub2', 'pub'], orden)
    pg.click('#card-custom-pub >> text=Hacer privada'); pg.wait_for_timeout(100); pg.click('#uiDialogConfirm'); pg.wait_for_timeout(300)
    r.caso('"Hacer privada" guarda privada: true y la pliega', pg.evaluate('window.__store()')['vtes_records']['pub'].get('privada') is True
           and pg.get_attribute('#card-custom-pub', 'aria-expanded') == 'false')

    # Crear una mesa privada desde el formulario
    pg.click('#openCreateFormBtn'); pg.wait_for_timeout(100)
    r.caso('el formulario de mesa virtual tiene la casilla "Mesa privada"', pg.is_visible('#tablePrivada'))
    pg.fill('#tableName', 'Privada nueva')
    pg.evaluate("document.getElementById('tableDateTime').value = '2031-03-10 20:00'")
    pg.fill('#tableCreator', 'Org'); pg.check('#tablePrivada')
    pg.click('#createTableBtn'); pg.wait_for_timeout(300)
    nuevas = [(k, v) for k, v in pg.evaluate('window.__store()')['vtes_records'].items() if v.get('name') == 'Privada nueva']
    r.caso('crear con la casilla guarda privada: true', len(nuevas) == 1 and nuevas[0][1].get('privada') is True, nuevas)
    if nuevas:
        pg.click('#createdModal button'); pg.wait_for_timeout(300)
        r.caso('al cerrar "Mesa creada", la privada nueva aparece desplegada', 'Ocultar' in pg.inner_text(f'#card-custom-{nuevas[0][0]}'))
    pg.click('#openCreateFormBtn'); pg.wait_for_timeout(100)
    r.caso('al volver a abrir el formulario la casilla está desmarcada', not pg.is_checked('#tablePrivada'))
    pg.evaluate("setTableModality('presencial')"); pg.wait_for_timeout(100)
    r.caso('presencial: la casilla no aparece', not pg.is_visible('#tablePrivada'))
    err.revisar()
    ctx.close()

    # Enlace directo a una mesa privada: se abre desplegada
    ctx = nuevo_contexto(nav); pg = ctx.new_page()
    pg.goto(url_archivo(ruta) + '#mesa-priv'); pg.wait_for_timeout(600)
    r.caso('enlace directo (#mesa-…) a una privada la abre desplegada', 'vtes.gg/amigos' in pg.inner_text('#card-custom-priv'))
    ctx.close()
