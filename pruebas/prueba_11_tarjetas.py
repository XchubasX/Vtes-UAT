"""Tarjetas rediseñadas: fecha y hora arriba, cupo al lado, Discord y contraseña visibles para cualquiera."""
from herramientas import armar_pagina, url_archivo, nuevo_contexto, ahora_ms, iso, DIA

TITULO = 'Tarjetas: fecha y hora al frente, datos de la partida siempre visibles'


def correr(nav, r):
    fut = ahora_ms() + 3 * DIA
    seed = {'vtes_records': {
        'v1': {'type': 'custom_table', 'name': 'Martes de V5', 'utcTime': iso(fut), 'utcMs': fut, 'modality': 'virtual',
               'platform': 'Lackey', 'format': 'v5', 'discord': 'vtes.gg/mx', 'gamePassword': 'sangre123', 'ownerUid': 'u1',
               'signups': {f'u{i}': {'uid': f'u{i}', 'nick': f'J{i}', 'at': i} for i in range(1, 4)}},
        'p1': {'type': 'custom_table', 'name': 'Jueves en El Dragón', 'utcTime': iso(fut), 'utcMs': fut, 'modality': 'presencial',
               'originTz': 'Europe/Madrid', 'recurrence': 'weekly', 'venue': 'Tienda El Dragón', 'city': 'Zaragoza', 'country': 'España',
               'mapsLink': 'https://maps.google.com/?q=dragon', 'ownerUid': 'u1',
               'signups': {'u1': {'uid': 'u1', 'nick': 'Lasombra', 'arrival': '18:00', 'at': 1}}}},
        'stats': {}}
    ctx = nuevo_contexto(nav, viewport={'width': 390, 'height': 844})
    pg = ctx.new_page(); err = r.errores_de_pagina(pg, 'sin errores de JavaScript (tarjetas nuevas)')
    pg.goto(url_archivo(armar_pagina('index.html', seed, 'tarjetas.html'))); pg.wait_for_timeout(400)

    t = pg.inner_text('#card-custom-v1')
    hora = pg.evaluate("new Date(%d).toLocaleTimeString(undefined,{hour:'2-digit',minute:'2-digit'})" % fut)
    fecha = pg.evaluate("fechaTarjeta(new Date(%d).toISOString())" % fut)
    r.caso('la tarjeta empieza con la fecha, luego la hora y después el nombre',
           t.find(fecha) == 0 and t.find(fecha) < t.find(hora) < t.find('Martes de V5'), t[:80])
    r.caso('la fecha lleva el día completo ("martes 30 sep")', len(fecha.split()) == 3, fecha)
    r.caso('el cupo va junto a la fecha: "Faltan 2 · 3/5"', 'Faltan 2 · 3/5' in t)
    r.caso('se ven 2 lugares "libre"', t.count('libre') == 2, t.count('libre'))
    r.caso('virtual: dice "hora de Ciudad de México" (la zona de quien mira)', 'hora de Ciudad de México' in t and 'tu hora' not in t)
    r.caso('zona sin nombre en la lista: usa la última parte ("Europe/Oslo" → "Oslo")', pg.evaluate("nombreZona('Europe/Oslo')") == 'Oslo')
    r.caso('plataforma y formato en una sola línea: "LackeyCCG · V5"', 'LackeyCCG · V5' in t)
    r.caso('sin sesión (espectador) se ve el Discord', 'vtes.gg/mx' in t)
    r.caso('sin sesión se ve el renglón de contraseña, oculta con puntitos', 'Contraseña' in t and '••••••' in t and 'sangre123' not in t)
    pg.click('#gamepwd-v1-boton'); pg.wait_for_timeout(100)
    t = pg.inner_text('#card-custom-v1')
    r.caso('"Ver" muestra la contraseña y el botón cambia a "Ocultar"', 'sangre123' in t and '••••••' not in t and 'Ocultar' in t)
    pg.click('#gamepwd-v1-boton'); pg.wait_for_timeout(100)
    r.caso('"Ocultar" la vuelve a esconder', 'sangre123' not in pg.inner_text('#card-custom-v1'))
    r.caso('sin sesión no hay botones de editar Discord ni contraseña', 'Editar' not in pg.inner_text('#card-custom-v1'))
    botones = ' '.join(pg.eval_on_selector_all('#customTablesContainer button', 'bs => bs.map(b => b.innerText)'))
    r.caso('los botones ya no llevan emojis', not any(e in botones for e in '➕📲🔗📅🚪📝✏️🎲⏭️⏳'), botones[:120])
    r.caso('botón principal "¡Unirme a esta Mesa!" y secundarios Invitar · Calendario; ya no hay "Compartir"',
           all(x in botones for x in ['¡Unirme a esta Mesa!', 'Invitar', 'Calendario']) and 'Compartir' not in botones)
    r.caso('el menú de Invitar empieza cerrado', not pg.is_visible('#invitar-v1'))
    pg.click('#invitar-boton-v1'); pg.wait_for_timeout(100)
    menu = pg.inner_text('#invitar-v1') if pg.is_visible('#invitar-v1') else ''
    r.caso('al tocar Invitar se abre con "Mensaje por WhatsApp" y "Copiar enlace"', 'Mensaje por WhatsApp' in menu and 'Copiar enlace' in menu)
    r.caso('el botón avisa a lectores de pantalla que el menú está abierto', pg.get_attribute('#invitar-boton-v1', 'aria-expanded') == 'true')
    pg.click('h1'); pg.wait_for_timeout(100)
    r.caso('tocar fuera cierra el menú', not pg.is_visible('#invitar-v1'))
    pg.click('#invitar-boton-v1'); pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
    r.caso('Escape cierra el menú', not pg.is_visible('#invitar-v1'))
    pg.evaluate("window.__abierto = null; window.open = (u) => { window.__abierto = u; }")
    pg.click('#invitar-boton-v1'); pg.click('#invitar-v1 >> text=Mensaje por WhatsApp'); pg.wait_for_timeout(100)
    abierto = pg.evaluate("window.__abierto") or ''
    r.caso('"Mensaje por WhatsApp" abre WhatsApp con la invitación y cierra el menú', 'whatsapp.com/send' in abierto and 'Martes%20de%20V5' in abierto and not pg.is_visible('#invitar-v1'), abierto[:80])
    pg.evaluate("window.__copiado = null; Object.defineProperty(navigator, 'clipboard', {value: {writeText: (x) => { window.__copiado = x; return Promise.resolve(); }}, configurable: true}); navigator.share = () => Promise.reject(new Error('no debía usarse')); true")
    pg.click('#invitar-boton-v1'); pg.click('#invitar-v1 >> text=Copiar enlace'); pg.wait_for_timeout(200)
    r.caso('"Copiar enlace" copia el enlace directo (aunque el celular tenga menú de compartir)', (pg.evaluate("window.__copiado") or '').endswith('#mesa-v1'))
    r.caso('al copiar avisa "Enlace copiado"', 'Enlace copiado' in pg.inner_text('#toastContainer'))
    r.caso('el tiempo relativo sigue actualizándose (clase rel-time)', pg.query_selector('#card-custom-v1 .rel-time') is not None)

    pg.evaluate("setTableModality('presencial')"); pg.wait_for_timeout(300)
    t = pg.inner_text('#card-custom-p1')
    r.caso('presencial: dice "hora de Zaragoza"', 'hora de Zaragoza' in t)
    r.caso('presencial: "Presencial · cada …" en una línea', 'Presencial · cada ' in t)
    r.caso('presencial: lugar, ciudad y "Ver mapa"', 'Tienda El Dragón' in t and 'Zaragoza, España' in t and 'Ver mapa' in t)
    r.caso('presencial: sin lugares "libre" ni Discord', 'libre' not in t and 'Discord' not in t)
    r.caso('presencial: cupo "1 confirmado"', '1 confirmado' in t)
    r.caso('presencial: "Orden de Asientos" visible para todos', 'Orden de Asientos' in t)

    pg.evaluate("window.__setUser({uid:'u1',displayName:'J1'})"); pg.wait_for_timeout(300)
    pg.evaluate("setTableModality('virtual')"); pg.wait_for_timeout(300)
    t = pg.inner_text('#card-custom-v1')
    r.caso('organizador: "Organizas tú" en la línea de datos', 'LackeyCCG · V5 · Organizas tú' in t)
    r.caso('organizador: puede editar Discord y contraseña', t.count('Editar') >= 2 and 'Editar mesa' in t and 'Cerrar Mesa' in t)
    err.revisar()
    ctx.close()
