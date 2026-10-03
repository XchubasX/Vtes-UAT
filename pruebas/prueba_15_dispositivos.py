"""Matriz de aparatos: el sitio toma el camino correcto en cada celular, computadora y navegador dentro de apps.

Simula cada aparato con su identificación de navegador, tamaño de pantalla y pantalla táctil.
No sustituye la prueba en aparatos reales (lo que pasa DENTRO de WhatsApp, Google o Safari
no se ve aquí): para eso está la lista de revisión manual del proyecto.
"""
from herramientas import armar_pagina, url_archivo, nuevo_contexto, ahora_ms, iso, DIA

TITULO = 'Aparatos: Android, iPhone, iPad, computadora y navegadores dentro de apps'

AND = 'Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36'
IPH = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1'
MAC = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15'
WIN = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'

# nombre, identificación, ancho, alto, táctil, puntos táctiles, ¿celular?, ¿dentro de otra app?
PERFILES = [
    ('Android · Chrome', AND, 412, 915, True, 5, True, False),
    ('Android · pantalla chica (360 px)', AND, 360, 740, True, 5, True, False),
    ('iPhone · Safari', IPH, 390, 844, True, 5, True, False),
    ('iPhone SE (320 px)', IPH, 320, 568, True, 5, True, False),
    ('iPad · Safari (se presenta como Mac)', MAC, 820, 1180, True, 5, True, False),
    ('Computadora Windows · Edge/Chrome', WIN, 1366, 768, False, 0, False, False),
    ('Mac · Safari', MAC, 1440, 900, False, 0, False, False),
    ('Android · dentro de WhatsApp', AND.replace('Linux; Android 14; Pixel 7', 'Linux; Android 14; Pixel 7; wv'), 412, 915, True, 5, True, True),
    ('iPhone · dentro de Instagram', IPH.replace(' Safari/604.1', ' Instagram 350.0.0'), 390, 844, True, 5, True, True),
    ('Android · dentro de Facebook', AND + ' [FBAN/EMA;FBAV/450.0]', 412, 915, True, 5, True, True),
]


def correr(nav, r):
    fut = ahora_ms() + 2 * DIA
    seed = {'vtes_records': {
        'v1': {'type': 'custom_table', 'name': 'Martes de V5 con nombre largo para probar', 'utcTime': iso(fut), 'utcMs': fut, 'modality': 'virtual',
               'platform': 'Lackey', 'format': 'v5', 'discord': 'https://discord.gg/vtes-espanol-servidor-largo', 'gamePassword': 'x', 'ownerUid': 'u9',
               'notes': 'Principiantes bienvenidos 🦇', 'signups': {f'u{i}': {'uid': f'u{i}', 'nick': n, 'at': i} for i, n in enumerate(['Nocturna', 'GabrielaTzimisce', 'Lasombra'], 1)}},
        'p1': {'type': 'custom_table', 'name': 'Jueves en El Dragón', 'utcTime': iso(fut), 'utcMs': fut, 'modality': 'presencial',
               'originTz': 'Europe/Madrid', 'venue': 'Tienda El Dragón', 'city': 'Zaragoza', 'country': 'España',
               'mapsLink': 'https://maps.google.com/?q=dragon', 'ownerUid': 'u9', 'signups': {'a': {'uid': 'a', 'nick': 'Toni', 'arrival': '18:00', 'at': 1}}}},
        'stats': {}}
    ruta = armar_pagina('index.html', seed, 'dispositivos.html')

    for nombre, ua, ancho, alto, tactil, puntos, celular, en_app in PERFILES:
        ctx = nuevo_contexto(nav, user_agent=ua, viewport={'width': ancho, 'height': alto}, has_touch=tactil, is_mobile=tactil and ancho < 800)
        ctx.add_init_script(f"Object.defineProperty(Navigator.prototype, 'maxTouchPoints', {{get: () => {puntos}}});")
        pg = ctx.new_page(); err = r.errores_de_pagina(pg, f'{nombre}: sin errores de JavaScript')
        pg.goto(url_archivo(ruta)); pg.wait_for_timeout(400)

        r.caso(f'{nombre}: se reconoce como {"celular" if celular else "computadora"}', pg.evaluate('esCelular()') == celular)
        url = pg.evaluate("whatsappShareUrl('🦇 hola\\nmundo')")
        esperado = 'https://api.whatsapp.com/send?text=' if celular else 'https://web.whatsapp.com/send?text='
        r.caso(f'{nombre}: WhatsApp por {"la app" if celular else "WhatsApp Web directo"}', url.startswith(esperado) and '%F0%9F%A6%87' in url and '%0A' in url, url[:45])
        r.caso(f'{nombre}: {"detecta" if en_app else "no confunde"} navegador dentro de otra app', pg.evaluate('isInAppBrowser()') == en_app)

        # Nada se sale de la pantalla (lista virtual, presencial y menú Invitar abierto)
        desborde = []
        for paso in ['virtual', 'invitar', 'presencial']:
            if paso == 'invitar':
                pg.click('#invitar-boton-v1'); pg.wait_for_timeout(100)
            if paso == 'presencial':
                pg.evaluate("closeInviteMenus(); setTableModality('presencial')"); pg.wait_for_timeout(200)
            sobra = pg.evaluate('document.documentElement.scrollWidth - window.innerWidth')
            if sobra > 1:
                desborde.append(f'{paso}: {sobra}px')
        r.caso(f'{nombre}: nada se sale de la pantalla ({ancho} px)', not desborde, desborde)

        # Iniciar sesión: dentro de otra app se pide abrir en Chrome/Safari; si no, la ventana normal
        pg.evaluate('void requireLogin()'); pg.wait_for_timeout(200)
        if en_app:
            titulo = pg.inner_text('#uiDialogTitle') if pg.is_visible('#uiDialog') else ''
            r.caso(f'{nombre}: al entrar pide abrir en {"Chrome" if "Android" in ua else "Safari"}', ('Chrome' if 'Android' in ua else 'Safari') in titulo and not pg.is_visible('#loginModal'), titulo)
        else:
            r.caso(f'{nombre}: al entrar muestra la ventana de Google', pg.is_visible('#loginModal'))
        err.revisar()
        ctx.close()

    # --- Copiar enlace y calendario (iguales en todos los aparatos; se prueban una vez)
    ctx = nuevo_contexto(nav, viewport={'width': 390, 'height': 844}); pg = ctx.new_page()
    pg.goto(url_archivo(ruta)); pg.wait_for_timeout(400)
    pg.evaluate("window.__copiado = null; Object.defineProperty(navigator, 'clipboard', {value: {writeText: (x) => { window.__copiado = x; return Promise.resolve(); }}, configurable: true})")
    pg.evaluate("void shareTableLink('v1')"); pg.wait_for_timeout(200)
    r.caso('copiar enlace: copia el enlace directo a la mesa', (pg.evaluate('window.__copiado') or '').endswith('#mesa-v1'))
    pg.evaluate("Object.defineProperty(navigator, 'clipboard', {value: {writeText: () => Promise.reject(new Error('bloqueado'))}, configurable: true})")
    pg.evaluate("void shareTableLink('v1')"); pg.wait_for_timeout(200)
    r.caso('copiar enlace: si el navegador no deja copiar, lo muestra para copiarlo a mano',
           pg.is_visible('#uiDialog') and pg.input_value('#uiDialog input').endswith('#mesa-v1'))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(100)

    pg.evaluate("openCalendarModal('v1')"); pg.wait_for_timeout(100)
    g = pg.get_attribute('#calendarGoogleLink', 'href') or ''
    r.caso('calendario de Google: enlace con título, fechas y enlace a la mesa',
           g.startswith('https://calendar.google.com/calendar/render?action=TEMPLATE') and '&dates=' in g and 'mesa-v1' in g, g[:70])
    pg.evaluate("window.__ics = null; const o = URL.createObjectURL; URL.createObjectURL = (b) => { b.text().then(t => window.__ics = t); return 'blob:x'; }; HTMLAnchorElement.prototype.click = function(){};")
    pg.evaluate('downloadCalendarFile()'); pg.wait_for_timeout(200)
    ics = pg.evaluate('window.__ics') or ''
    r.caso('archivo de calendario (.ics): formato válido para iPhone y Outlook',
           ics.startswith('BEGIN:VCALENDAR') and 'BEGIN:VEVENT' in ics and 'DTSTART:' in ics and 'END:VCALENDAR' in ics and '\r\n' in ics, ics[:40])
    r.caso('archivo de calendario: conserva acentos y emojis de las notas', '🦇' in ics or 'Principiantes' in ics)
    r.caso('el calendario no incluye la contraseña de la partida', 'Contraseña' not in ics and 'gamePassword' not in ics)
    ctx.close()
