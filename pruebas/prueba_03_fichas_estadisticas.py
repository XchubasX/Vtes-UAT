"""Fichas de estadísticas por cuenta y guardado separado (mesa primero, estadísticas después)."""
from herramientas import armar_pagina, url_archivo, nuevo_contexto

TITULO = 'Fichas de estadísticas por cuenta y guardado separado'


def _crear(pg):
    pg.click('#openCreateFormBtn'); pg.wait_for_timeout(100)
    pg.fill('#tableName', 'M'); pg.evaluate("document.getElementById('tableDateTime').value='2031-03-10 20:00'"); pg.fill('#tableCreator', 'Ana')
    pg.click('#createTableBtn'); pg.wait_for_timeout(400)


def correr(nav, r):
    ruta = armar_pagina('index.html', {'stats': {}}, 'fichas.html')
    logs = lambda pg: pg.evaluate('window.__store()')['stats'].get('tablesLog', {})

    ctx = nuevo_contexto(nav); pg = ctx.new_page(); err = r.errores_de_pagina(pg)
    pg.goto(url_archivo(ruta)); pg.wait_for_timeout(300)
    pg.evaluate("window.__setUser({uid:'uidA', displayName:'Ana'})"); pg.wait_for_timeout(200)
    _crear(pg); pg.click('#createdModal button')
    L = logs(pg)
    if not r.caso('al crear se guarda una ficha', len(L) == 1, L):
        return
    nid = list(L)[0]; f = L[nid]
    r.caso('al crear: la ficha guarda la cuenta del organizador', f.get('owner') == 'uidA' and f.get('uids') == {'uidA': True}, f)
    pg.click(f'#card-custom-{nid} >> text=Anotar a otra persona'); pg.wait_for_timeout(100)
    pg.fill('#joinNick', 'Amigo'); pg.click('#joinSubmitBtn'); pg.wait_for_timeout(300)
    f = logs(pg)[nid]
    r.caso('persona anotada por el organizador: cuenta por nick, no por cuenta', f['uids'] == {'uidA': True} and 'amigo' in f['players'], f)
    for u, n in [('uidB', 'Beto'), ('uidC', 'Caro'), ('uidD', 'Dani')]:
        pg.evaluate(f"window.__setUser({{uid:'{u}', displayName:'{n}'}})"); pg.wait_for_timeout(200)
        pg.click(f'#card-custom-{nid} >> text=¡Unirme a esta Mesa!'); pg.wait_for_timeout(100)
        pg.fill('#joinNick', n); pg.click('#joinSubmitBtn'); pg.wait_for_timeout(300)
    f = logs(pg)[nid]
    r.caso('cada jugador que se une queda con su cuenta', set(f['uids']) == {'uidA', 'uidB', 'uidC', 'uidD'}, f['uids'])
    pg.evaluate("window.__setUser({uid:'uidE', displayName:'Eli'})"); pg.wait_for_timeout(200)
    pg.click(f'#card-custom-{nid} >> text=Apuntarme como suplente'); pg.wait_for_timeout(100)
    pg.fill('#joinNick', 'Eli'); pg.click('#joinSubmitBtn'); pg.wait_for_timeout(300)
    f = logs(pg)[nid]
    r.caso('el suplente no cuenta como jugador (solo en suplentes)', 'uidE' not in f['uids'] and 'eli' in f.get('subs', {}))
    pg.evaluate("window.__setUser({uid:'uidA', displayName:'Ana'})"); pg.wait_for_timeout(300)
    pg.locator(f'#card-custom-{nid} span:has-text("Beto") >> button[title="Remover jugador"]').click(); pg.wait_for_timeout(100)
    pg.click('#uiDialogConfirm'); pg.wait_for_timeout(300); pg.click('#uiDialogCancel')
    f = logs(pg)[nid]
    r.caso('el suplente que sube queda con su cuenta; el que salió se conserva', 'uidE' in f['uids'] and 'uidB' in f['uids'], f['uids'])
    err.revisar()
    ctx.close()

    # Firebase rechaza las estadísticas: la mesa se crea igual
    ctx = nuevo_contexto(nav); pg = ctx.new_page(); err = r.errores_de_pagina(pg, 'sin errores de JavaScript (estadísticas rechazadas)')
    pg.goto(url_archivo(ruta)); pg.wait_for_timeout(300)
    pg.evaluate("window.__setUser({uid:'uidA', displayName:'Ana'})"); pg.wait_for_timeout(200)
    r.caso('el nombre de la mesa está limitado a 60 caracteres', pg.get_attribute('#tableName', 'maxlength') == '60')
    pg.evaluate("() => { window.__failNext = (u) => Object.keys(u).some(k => k.startsWith('stats/')); }")
    _crear(pg)
    st = pg.evaluate('window.__store()')
    r.caso('si las estadísticas fallan, la mesa se crea igual y aparece el aviso de éxito', len(st.get('vtes_records', {})) == 1 and pg.is_visible('#createdModal'))
    r.caso('las estadísticas rechazadas no se guardan', 'tablesLog' not in st['stats'])
    w = pg.evaluate('window.__writes')
    r.caso('mesa y estadísticas se guardan en pasos separados', all(not any(k.startswith('stats/') for k in x) or all(k.startswith('stats/') for k in x) for x in w))
    err.revisar()
    ctx.close()
