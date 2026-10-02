"""Página principal: sesión, crear, unirse, anotar a otros, suplentes, vetar, eventos presenciales."""
from herramientas import armar_pagina, url_archivo, nuevo_contexto, ahora_ms, iso, DIA

TITULO = 'Página principal: sesión, mesas, suplentes y veto'


def correr(nav, r):
    fut = ahora_ms() + 5 * DIA
    seed = {'vtes_records': {
        'legacy1': {'type': 'custom_table', 'name': 'Mesa Vieja', 'utcTime': iso(fut), 'modality': 'virtual',
                    'deletePin': '1234', 'originTz': 'America/Mexico_City', 'platform': 'Lackey', 'players': ['Old1', 'Old2']},
    }, 'stats': {}}
    pagina_html = armar_pagina('index.html', seed, 'principal.html')
    ctx = nuevo_contexto(nav)
    page = ctx.new_page()
    err = r.errores_de_pagina(page)
    page.goto(url_archivo(pagina_html)); page.wait_for_timeout(300)

    txt = page.inner_text('#customTablesContainer')
    r.caso('mesa antigua visible con sus jugadores (sin sesión)', 'Mesa Vieja' in txt and 'Old1' in txt and 'Old2' in txt)
    r.caso('sin sesión no se ven botones de gestión', 'Cerrar Mesa' not in txt and 'Editar mesa' not in txt)
    r.caso('la barra de sesión ofrece entrar', 'Entrar con Google' in page.inner_text('#authBar'))

    page.click('text=¡Unirme a esta Mesa!'); page.wait_for_timeout(100)
    r.caso('al unirse sin sesión aparece la ventana de Google', page.is_visible('#loginModal'))
    page.click('#loginModalBtn'); page.wait_for_timeout(300)
    r.caso('tras iniciar sesión se abre la ventana para unirse', page.is_visible('#joinModal'))
    page.fill('#joinNick', 'Ana'); page.click('#joinSubmitBtn'); page.wait_for_timeout(300)
    st = page.evaluate('window.__store()')
    su = st['vtes_records']['legacy1'].get('signups', {})
    r.caso('se guarda signups/uidA con nick y hora del servidor', 'uidA' in su and su['uidA']['nick'] == 'Ana' and isinstance(su['uidA']['at'], int), su)
    r.caso('contador virtualJoins +1', st['stats'].get('virtualJoins') == 1, st['stats'].get('virtualJoins'))
    txt = page.inner_text('#customTablesContainer')
    r.caso('Ana aparece como "tú" con botón Salir', 'Ana' in txt and '· tú' in txt and 'Salir de la mesa' in txt)
    r.caso('ya anotada: no aparece el botón para unirse otra vez', '¡Unirme a esta Mesa!' not in txt)
    r.caso('Ana no organiza la mesa vieja: sin gestión', 'Cerrar Mesa' not in txt)

    # Crear mesa nueva como Ana
    page.click('#openCreateFormBtn'); page.wait_for_timeout(100)
    r.caso('con sesión, el formulario de crear se abre directo', page.is_visible('#createFormPanel'))
    page.fill('#tableName', 'Mesa de Ana')
    page.evaluate("document.getElementById('tableDateTime').value = '2031-03-10 20:00'")
    page.fill('#tableCreator', 'Ana')
    page.click('#createTableBtn'); page.wait_for_timeout(300)
    st = page.evaluate('window.__store()')
    nuevas = [(k, v) for k, v in st['vtes_records'].items() if v.get('name') == 'Mesa de Ana']
    if not r.caso('crear mesa: se guarda la mesa nueva', len(nuevas) == 1, nuevas):
        return
    nid, nt = nuevas[0]
    r.caso('mesa nueva con ownerUid y utcMs, sin PIN ni lista vieja', nt.get('ownerUid') == 'uidA' and isinstance(nt.get('utcMs'), int) and 'deletePin' not in nt and 'players' not in nt, nt)
    r.caso('la organizadora queda anotada en signups', nt['signups']['uidA']['nick'] == 'Ana')
    r.caso('aparece la ventana "¡Mesa creada con éxito!"', page.is_visible('#createdModal'))
    page.click('#createdModal button'); page.wait_for_timeout(100)
    card = page.inner_text(f'#card-custom-{nid}')
    r.caso('la organizadora ve sus botones de gestión', 'Organizas tú' in card and 'Cerrar Mesa' in card and 'Editar mesa' in card)
    r.caso('la organizadora puede anotar a otra persona', 'Anotar a otra persona' in card)

    page.click(f'#card-custom-{nid} >> text=Anotar a otra persona'); page.wait_for_timeout(100)
    r.caso('al anotar a otra persona el nick viene vacío', page.input_value('#joinNick') == '')
    page.fill('#joinNick', 'AmigoDeAna'); page.click('#joinSubmitBtn'); page.wait_for_timeout(300)
    su = page.evaluate('window.__store()')['vtes_records'][nid]['signups']
    amigo = [k for k, v in su.items() if v['nick'] == 'AmigoDeAna']
    r.caso('persona anotada con llave aleatoria y la cuenta de la organizadora', len(amigo) == 1 and amigo[0] != 'uidA' and su[amigo[0]]['uid'] == 'uidA', su)

    # Beto entra y se une
    page.evaluate("window.__setUser({uid:'uidB', displayName:'Beto'})"); page.wait_for_timeout(300)
    card = page.inner_text(f'#card-custom-{nid}')
    r.caso('Beto no ve gestión en una mesa ajena', 'Cerrar Mesa' not in card and 'Editar mesa' not in card)
    page.click(f'#card-custom-{nid} >> text=¡Unirme a esta Mesa!'); page.wait_for_timeout(100)
    page.fill('#joinNick', 'ana'); page.click('#joinSubmitBtn'); page.wait_for_timeout(200)
    r.caso('un nick repetido (sin importar mayúsculas) se rechaza', 'ya está anotado' in page.inner_text('#joinNickError'))
    page.fill('#joinNick', 'Beto'); page.click('#joinSubmitBtn'); page.wait_for_timeout(300)
    r.caso('Beto queda anotado con su cuenta', 'uidB' in page.evaluate('window.__store()')['vtes_records'][nid]['signups'])
    r.caso('Beto no ve × para quitar a otros', page.inner_html(f'#card-custom-{nid}').count('title="Remover jugador"') == 0)

    # Llenar la mesa y un suplente
    for uid, nick in [('uidC', 'Caro'), ('uidD', 'Dani')]:
        page.evaluate(f"window.__setUser({{uid:'{uid}', displayName:'{nick}'}})"); page.wait_for_timeout(200)
        page.click(f'#card-custom-{nid} >> text=¡Unirme a esta Mesa!'); page.wait_for_timeout(100)
        page.fill('#joinNick', nick); page.click('#joinSubmitBtn'); page.wait_for_timeout(300)
    page.evaluate("window.__setUser({uid:'uidE', displayName:'Eli'})"); page.wait_for_timeout(200)
    card = page.inner_text(f'#card-custom-{nid}')
    r.caso('mesa llena (5/5) dice "Mesa llena" y ofrece suplente', 'Mesa llena (5/5)' in card and 'Apuntarme como suplente' in card)
    page.click(f'#card-custom-{nid} >> text=Apuntarme como suplente'); page.wait_for_timeout(100)
    page.fill('#joinNick', 'Eli'); page.click('#joinSubmitBtn'); page.wait_for_timeout(300)
    card = page.inner_text(f'#card-custom-{nid}')
    r.caso('Eli aparece como suplente 1 con su botón de salir', 'Suplentes (1/3)' in card and 'Salir de suplentes' in card)
    st = page.evaluate('window.__store()')
    r.caso('la ficha de estadísticas registra al suplente', any('eli' in (v.get('subs') or {}) for v in st['stats']['tablesLog'].values()))

    # La organizadora quita a Beto -> Eli sube
    page.evaluate("window.__setUser({uid:'uidA', displayName:'Ana'})"); page.wait_for_timeout(300)
    r.caso('la organizadora ve × en los demás jugadores', page.inner_html(f'#card-custom-{nid}').count('title="Remover jugador"') >= 3)
    antes = st['stats'].get('virtualJoins')
    page.locator(f'#card-custom-{nid} span:has-text("Beto") >> button[title="Remover jugador"]').click(); page.wait_for_timeout(100)
    page.click('#uiDialogConfirm'); page.wait_for_timeout(300)
    r.caso('aviso: Eli (suplente) ocupa la plaza', page.is_visible('#uiDialog') and 'Eli' in page.inner_text('#uiDialogMessage'))
    page.click('#uiDialogCancel')
    st = page.evaluate('window.__store()')
    r.caso('Beto quitado de la mesa', 'uidB' not in st['vtes_records'][nid]['signups'])
    r.caso('el suplente que sube cuenta como unión', st['stats'].get('virtualJoins') == antes + 1)
    r.caso('la ficha registra al suplente promovido', any('eli' in (v.get('promoted') or {}) for v in st['stats']['tablesLog'].values()))
    r.caso('ya no hay suplentes en la tarjeta', 'Suplentes' not in page.inner_text(f'#card-custom-{nid}'))

    # Administradora: veto
    page.evaluate("window.__store().admins = {uidA: true}")
    page.evaluate("window.__setUser({uid:'uidA', displayName:'Ana'})"); page.wait_for_timeout(300)
    r.caso('la barra muestra "Administrador"', 'Administrador' in page.inner_text('#authBar'))
    legacy = page.inner_html('#card-custom-legacy1')
    r.caso('la administradora puede gestionar la mesa antigua', 'Cerrar Mesa' in legacy and 'title="Remover jugador"' in legacy)
    page.locator(f'#card-custom-{nid} span:has-text("Caro") >> button[title="Vetar esta cuenta"]').click(); page.wait_for_timeout(100)
    page.click('#uiDialogConfirm'); page.wait_for_timeout(300)
    st = page.evaluate('window.__store()')
    r.caso('Caro vetada y quitada de la mesa', st.get('banned', {}).get('uidC', {}).get('nick') == 'Caro' and 'uidC' not in st['vtes_records'][nid]['signups'])
    page.evaluate("window.__setUser({uid:'uidC', displayName:'Caro'})"); page.wait_for_timeout(300)
    r.caso('una cuenta vetada se muestra bloqueada', 'Cuenta bloqueada' in page.inner_text('#authBar'))
    n = page.evaluate('window.__writes.length')
    page.click('#card-custom-legacy1 >> text=¡Unirme a esta Mesa!'); page.wait_for_timeout(200)
    r.caso('una cuenta vetada no puede unirse', not page.is_visible('#joinModal') and page.evaluate('window.__writes.length') == n)

    page.evaluate("window.__setUser({uid:'uidA', displayName:'Ana'})"); page.wait_for_timeout(300)
    page.locator('#card-custom-legacy1 span:has-text("Old1") >> button[title="Remover jugador"]').click(); page.wait_for_timeout(100)
    page.click('#uiDialogConfirm'); page.wait_for_timeout(300)
    pl = page.evaluate('window.__store()')['vtes_records']['legacy1'].get('players')
    pl = list(pl.values()) if isinstance(pl, dict) else pl
    r.caso('la administradora quita un registro antiguo (Old1)', pl == ['Old2'], pl)

    # Evento presencial con hora de llegada
    page.evaluate("window.__setUser({uid:'uidB', displayName:'Beto'})"); page.wait_for_timeout(300)
    page.click('#modePresencialBtn'); page.click('#openCreateFormBtn'); page.wait_for_timeout(100)
    page.fill('#tableName', 'Torneo')
    page.evaluate("document.getElementById('tableDateTime').value = '2031-03-11 17:00'")
    page.fill('#tableCreator', 'Beto'); page.fill('#tableVenue', 'Tienda'); page.fill('#tableCity', 'CDMX')
    page.evaluate("document.getElementById('tableCreatorArrival').value = '17:30'")
    page.click('#createTableBtn'); page.wait_for_timeout(300); page.click('#createdModal button')
    st = page.evaluate('window.__store()')
    tid = [k for k, v in st['vtes_records'].items() if v.get('name') == 'Torneo'][0]
    r.caso('evento presencial: se guarda la hora de llegada del organizador', st['vtes_records'][tid]['signups']['uidB'].get('arrival') == '17:30')
    r.caso('contador de eventos presenciales +1', st['stats'].get('presencialEventsCreated') == 1)
    page.locator(f'#card-custom-{tid} button[title="Editar hora de llegada"]').first.click(); page.wait_for_timeout(100)
    page.fill('#uiDialogInput', '18:15'); page.click('#uiDialogConfirm'); page.wait_for_timeout(300)
    r.caso('el jugador edita su propia hora de llegada', page.evaluate('window.__store()')['vtes_records'][tid]['signups']['uidB'].get('arrival') == '18:15')

    page.click('#authBar >> text=Cerrar sesión'); page.wait_for_timeout(300)
    r.caso('tras cerrar sesión no hay botones de gestión', 'Cerrar Evento' not in page.inner_text(f'#card-custom-{tid}'))
    err.revisar()
    ctx.close()

    # Navegador dentro de WhatsApp (Android)
    ctx2 = nuevo_contexto(nav, user_agent='Mozilla/5.0 (Linux; Android 13; Pixel 7; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0 Mobile Safari/537.36 WhatsApp/2.24')
    p2 = ctx2.new_page()
    p2.goto(url_archivo(pagina_html)); p2.wait_for_timeout(300)
    p2.click('text=¡Unirme a esta Mesa!'); p2.wait_for_timeout(200)
    r.caso('dentro de WhatsApp (Android) pide abrir en Chrome', p2.is_visible('#uiDialog') and 'Chrome' in p2.inner_text('#uiDialogTitle') and not p2.is_visible('#loginModal'))
    ctx2.close()
