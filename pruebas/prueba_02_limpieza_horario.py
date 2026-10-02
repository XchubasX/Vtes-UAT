"""Limpieza de mesas vencidas, eventos semanales, salir, editar horario y cerrar."""
from datetime import datetime
from herramientas import armar_pagina, url_archivo, nuevo_contexto, ahora_ms, iso, DIA

TITULO = 'Limpieza de vencidas, eventos semanales, salir, editar horario y cerrar'


def correr(nav, r):
    now = ahora_ms()
    vieja = now - 5 * 3600 * 1000
    vieja_p = now - 30 * 3600 * 1000
    fut = now + 3 * DIA
    seed = {'vtes_records': {
        'expV': {'type': 'custom_table', 'name': 'Vencida', 'utcTime': iso(vieja), 'utcMs': vieja, 'modality': 'virtual', 'ownerUid': 'uidZ',
                 'signups': {'uidZ': {'uid': 'uidZ', 'nick': 'Z', 'at': 1}}},
        'expW': {'type': 'custom_table', 'name': 'Semanal', 'utcTime': iso(vieja_p), 'utcMs': vieja_p, 'modality': 'presencial', 'recurrence': 'weekly',
                 'originTz': 'America/Mexico_City', 'venue': 'T', 'city': 'CDMX', 'country': 'México', 'ownerUid': 'uidZ',
                 'signups': {'uidZ': {'uid': 'uidZ', 'nick': 'Z', 'at': 1}}},
        'mine': {'type': 'custom_table', 'name': 'MiMesa', 'utcTime': iso(fut), 'utcMs': fut, 'modality': 'virtual', 'ownerUid': 'uidA',
                 'originTz': 'America/Mexico_City',
                 'signups': {'uidA': {'uid': 'uidA', 'nick': 'Ana', 'at': 1}, 'uidB': {'uid': 'uidB', 'nick': 'Beto', 'at': 2}}},
    }, 'stats': {}}
    ctx = nuevo_contexto(nav); pg = ctx.new_page(); err = r.errores_de_pagina(pg)
    pg.goto(url_archivo(armar_pagina('index.html', seed, 'limpieza.html'))); pg.wait_for_timeout(300)
    st = pg.evaluate('window.__store()')
    r.caso('sin sesión no se intenta limpiar nada', 'expV' in st['vtes_records'] and pg.evaluate('window.__writes.length') == 0)
    r.caso('la mesa vencida no se muestra', 'Vencida' not in pg.inner_text('#customTablesContainer'))
    pg.evaluate("window.__setUser({uid:'uidB', displayName:'Beto'})"); pg.wait_for_timeout(200)
    pg.evaluate("firebase.database().ref('stats/x').set(1)"); pg.wait_for_timeout(300)  # provoca un nuevo dibujado
    st = pg.evaluate('window.__store()'); w = pg.evaluate('window.__writes')
    r.caso('con sesión, la mesa vencida se borra', 'expV' not in st['vtes_records'])
    ew = st['vtes_records']['expW']
    roll = [x for x in w if any('expW' in k for k in x)]
    r.caso('evento semanal: solo cambia fecha y se vacían las listas', len(roll) == 1 and set(roll[0].keys()) == {
        'vtes_records/expW/utcTime', 'vtes_records/expW/utcMs', 'vtes_records/expW/signups', 'vtes_records/expW/players'}, roll)
    coherente = abs(datetime.fromisoformat(ew['utcTime'].replace('Z', '+00:00')).timestamp() * 1000 - ew['utcMs']) < 1
    r.caso('evento semanal: nueva fecha dentro de lo que permiten las reglas', ew['utcMs'] > now - DIA and ew['utcMs'] < now + 8 * DIA and 'signups' not in ew and coherente, ew)

    pg.click('#card-custom-mine >> text=Salir de la mesa'); pg.wait_for_timeout(100); pg.click('#uiDialogConfirm'); pg.wait_for_timeout(300)
    r.caso('Beto sale de la mesa por su cuenta', 'uidB' not in pg.evaluate('window.__store()')['vtes_records']['mine']['signups'])

    pg.evaluate("window.__setUser({uid:'uidA', displayName:'Ana'})"); pg.wait_for_timeout(300)
    pg.click('#card-custom-mine >> text=Editar mesa'); pg.wait_for_timeout(100)
    pg.evaluate("document.getElementById('editScheduleDateTime').value='2031-05-01 21:00'")
    pg.click('#editScheduleSaveBtn'); pg.wait_for_timeout(300)
    m = pg.evaluate('window.__store()')['vtes_records']['mine']
    r.caso('editar horario guarda utcTime y utcMs juntos', m['utcMs'] == int(datetime.fromisoformat(m['utcTime'].replace('Z', '+00:00')).timestamp() * 1000) and m['utcTime'].startswith('2031-05'), m.get('utcTime'))
    nombre_antes = m['name']
    r.caso('editar solo el horario no cambia el nombre', m['name'] == nombre_antes)
    pg.click('#card-custom-mine >> text=Editar mesa'); pg.wait_for_timeout(100)
    r.caso('la ventana se llama "Editar mesa" y trae el nombre actual', pg.inner_text('#editScheduleTitle') == 'Editar mesa' and pg.input_value('#editScheduleName') == nombre_antes)
    utc_antes = m['utcTime']
    pg.fill('#editScheduleName', '  Mesa renombrada  '); pg.click('#editScheduleSaveBtn'); pg.wait_for_timeout(300)
    m = pg.evaluate('window.__store()')['vtes_records']['mine']
    r.caso('cambiar solo el nombre lo guarda (sin espacios) y deja el horario igual', m['name'] == 'Mesa renombrada' and m['utcTime'] == utc_antes, (m['name'], m['utcTime']))
    r.caso('la tarjeta muestra el nombre nuevo', 'Mesa renombrada' in pg.inner_text('#card-custom-mine'))
    pg.click('#card-custom-mine >> text=Editar mesa'); pg.wait_for_timeout(100)
    pg.fill('#editScheduleName', 'Nombre y hora'); pg.evaluate("document.getElementById('editScheduleDateTime').value='2031-06-02 20:00'")
    pg.click('#editScheduleSaveBtn'); pg.wait_for_timeout(300)
    m = pg.evaluate('window.__store()')['vtes_records']['mine']
    r.caso('cambiar nombre y horario a la vez guarda los dos', m['name'] == 'Nombre y hora' and m['utcTime'].startswith('2031-06'), (m['name'], m['utcTime']))
    pg.click('#card-custom-mine >> text=Editar mesa'); pg.wait_for_timeout(100)
    pg.fill('#editScheduleName', '   '); pg.click('#editScheduleSaveBtn'); pg.wait_for_timeout(300)
    r.caso('un nombre vacío no se guarda', pg.evaluate('window.__store()')['vtes_records']['mine']['name'] == 'Nombre y hora')
    r.caso('el campo de nombre limita a 60 caracteres', pg.get_attribute('#editScheduleName', 'maxlength') == '60')
    pg.evaluate('closeEditScheduleModal()'); pg.wait_for_timeout(100)
    pg.click('#card-custom-mine >> text=Cerrar Mesa'); pg.wait_for_timeout(100); pg.click('#uiDialogConfirm'); pg.wait_for_timeout(300)
    r.caso('la organizadora cierra su mesa', 'mine' not in pg.evaluate('window.__store()')['vtes_records'])
    err.revisar()
    ctx.close()
