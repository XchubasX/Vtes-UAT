"""Avisos de mesa en el celular (tablero 24): lógica del servidor, ventana «¿Te avisamos?», menú, guía de iPhone y Worker."""
import json, re, subprocess
from herramientas import armar_pagina, url_archivo, nuevo_contexto, ahora_ms, iso, DIA, REPO, PRUEBAS

TITULO = 'Avisos de mesa en el celular (completa, suplente que entra y aviso previo)'

# Navegador simulado con avisos: permiso, service worker y Firebase Messaging
SIMULADOR_AVISOS = """<script>
window.__permisoPedido = 0; window.__permiso = 'default'; window.__respuestaPermiso = 'granted';
window.__token = 'token-1'; window.__tokensBorrados = 0; window.__fetch = [];
if (!window.__sinAvisos) {
  window.Notification = { get permission() { return window.__permiso; },
    requestPermission() { window.__permisoPedido++; window.__permiso = window.__respuestaPermiso; return Promise.resolve(window.__permiso); } };
  window.PushManager = function () {};
  Object.defineProperty(navigator, 'serviceWorker', { value: { register: (u) => { window.__sw = u; return Promise.resolve({}); } }, configurable: true });
  window.firebase.messaging = () => ({
    getToken: (o) => { window.__vapid = o && o.vapidKey; return Promise.resolve(window.__token); },
    deleteToken: () => { window.__tokensBorrados++; return Promise.resolve(true); },
    onMessage: (cb) => { window.__alMensaje = cb; }
  });
}
window.fetch = (u, o) => { window.__fetch.push([u, o && o.method, o && o.headers && o.headers.Authorization]); return Promise.resolve({ ok: true, status: 200 }); };
</script>"""
CONFIG_CON_LLAVE = [(re.search(r"vapidKey: '[^']*'", (REPO / "config.js").read_text()).group(0), "vapidKey: 'LLAVE-PRUEBA'")]
USUARIO = "window.__setUser({uid:'uidA', displayName:'Ana', getIdToken: () => Promise.resolve('id-token-ana')})"


def pagina(nav, nombre, seed=None, antes='', ua=None, app=False):
    extra = '<script>' + antes + '</script>' + SIMULADOR_AVISOS
    if app:
        extra += "<script>window.matchMedia = (q) => ({ matches: String(q).includes('standalone'), addListener(){}, removeListener(){} });</script>"
    html = armar_pagina('index.html', seed or {'vtes_records': {}, 'stats': {}}, nombre, extra_head=extra, config_extra=CONFIG_CON_LLAVE)
    kw = {'viewport': {'width': 390, 'height': 844}}
    if ua: kw['user_agent'] = ua
    ctx = nuevo_contexto(nav, **kw)
    pg = ctx.new_page()
    return ctx, pg, html


def aparatos(pg, uid='uidA'):
    return ((pg.evaluate('window.__store()').get('avisos') or {}).get(uid)) or {}


def correr(nav, r):
    # ------------------------------------------------------------------ servidor
    out = subprocess.run(['node', str(PRUEBAS / 'avisos-servidor-prueba.mjs')], capture_output=True, text=True)
    try:
        casos = json.loads(out.stdout)
    except Exception:
        casos = [['servidor: la prueba de la lógica corre', False, (out.stderr or out.stdout)[:300]]]
    for nombre, ok, det in casos:
        r.caso('servidor: ' + nombre, ok, det)

    # ------------------------------------------------------------------ Worker y archivos
    w = (REPO / 'wrangler.jsonc').read_text(encoding='utf-8')
    wj = json.loads(re.sub(r'^\s*//.*$', '', w, flags=re.M))
    cfg = (REPO / 'config.js').read_text(encoding='utf-8')
    proyecto = re.search(r'projectId:\s*"([^"]+)"', cfg).group(1)
    r.caso('wrangler: cron cada 5 minutos', wj.get('triggers', {}).get('crons') == ['*/5 * * * *'], wj.get('triggers'))
    r.caso('wrangler: el worker atiende /api/* (aviso de prueba)', '/api/*' in wj['assets'].get('run_worker_first', []))
    v = wj.get('vars', {})
    r.caso('wrangler: base de datos y llave del MISMO proyecto que config.js (' + proyecto + ')',
           v.get('FIREBASE_DB_URL') in cfg and v.get('FIREBASE_API_KEY') in cfg and proyecto in v.get('FIREBASE_DB_URL', ''), v)
    r.caso('wrangler: la cuenta de servicio NO está en el archivo (es secreto de Cloudflare)', 'private_key' not in w and 'FIREBASE_CUENTA_SERVICIO"' not in w)
    sitio_ok = ('uat.' in v.get('SITIO', '')) == ('esPruebas: true' in cfg)
    r.caso('wrangler: los avisos abren el sitio correcto (pruebas → uat)', sitio_ok, v.get('SITIO'))
    pub = (REPO / 'cloudflare-publicar.sh').read_text(encoding='utf-8')
    r.caso('avisos-servidor.js no se publica como archivo del sitio', 'avisos-servidor.js' in pub)
    sw = (REPO / 'firebase-messaging-sw.js').read_text(encoding='utf-8')
    idx = (REPO / 'index.html').read_text(encoding='utf-8')
    ver = re.search(r'firebasejs/([\d.]+)/firebase-app-compat', idx).group(1)
    r.caso('service worker: usa config.js y la misma versión de Firebase que la página (' + ver + ')',
           "importScripts('config.js" in sw and sw.count('firebasejs/' + ver + '/') == 2)
    r.caso('service worker: atiende el toque ANTES que Firebase (abre la mesa aunque Elysium ya esté abierto)',
           sw.find("addEventListener('notificationclick'") != -1 and sw.find("addEventListener('notificationclick'") < sw.find('importScripts(')
           and 'stopImmediatePropagation' in sw and "postMessage({ tipo: 'abrirMesa'" in sw and 'openWindow(link)' in sw)
    srv = (REPO / 'avisos-servidor.js').read_text(encoding='utf-8')
    r.caso('servidor: el aviso lleva el enlace y la mesa en sus datos', 'data: { link: enlace, mesa:' in srv)
    r.caso('la página carga firebase-messaging-compat de la misma versión', 'firebasejs/' + ver + '/firebase-messaging-compat.js' in idx)
    code = ("import('" + (REPO / 'worker.js').as_uri() + "').then(async m => { const env = { FIREBASE_AUTH_HOST: 'x.firebaseapp.com', ASSETS: { fetch: () => new Response('sitio') } };"
            "const a = await m.default.fetch(new Request('https://uat.eternalschedule.com/api/aviso-prueba'), env);"
            "const b = await m.default.fetch(new Request('https://uat.eternalschedule.com/api/aviso-prueba', { method: 'POST' }), env);"
            "const c = await m.default.fetch(new Request('https://uat.eternalschedule.com/Zaragoza'), env);"
            "console.log(JSON.stringify([a.status, b.status, await c.text(), typeof m.default.scheduled])) })")
    out = subprocess.run(['node', '--input-type=module', '-e', code], capture_output=True, text=True)
    res = json.loads(out.stdout or 'null') or [None] * 4
    r.caso('worker: /api/aviso-prueba solo acepta POST', res[0] == 405, res or out.stderr[:200])
    r.caso('worker: sin el secreto configurado responde «falta la cuenta de servicio» (503)', res[1] == 503, res)
    r.caso('worker: las páginas del sitio siguen igual', res[2] == 'sitio', res)
    r.caso('worker: tiene la tarea programada (scheduled)', res[3] == 'function', res)

    # ------------------------------------------------------------------ ventana «¿Te avisamos?» al unirse
    fut = ahora_ms() + 5 * DIA
    seed = {'vtes_records': {'m1': {'type': 'custom_table', 'name': 'Martes de V5', 'utcTime': iso(fut), 'utcMs': fut, 'modality': 'virtual',
                                    'ownerUid': 'otro', 'originTz': 'America/Mexico_City', 'platform': 'Lackey'}}, 'stats': {}}
    ctx, pg, html = pagina(nav, 'avisos1.html', seed)
    err = r.errores_de_pagina(pg, 'sin errores de JavaScript (avisos en computadora)')
    pg.goto(url_archivo(html)); pg.wait_for_timeout(300)
    r.caso('sin sesión no aparece el botón «Avisos»', 'Avisos' not in pg.inner_text('#authBar'))
    pg.evaluate(USUARIO); pg.wait_for_timeout(300)
    r.caso('con sesión aparece «🔕 Avisos» junto a «Cerrar sesión»', '🔕 Avisos' in pg.inner_text('#authBar') and 'Cerrar sesión' in pg.inner_text('#authBar'))
    pg.click('text=¡Unirme a esta Mesa!'); pg.wait_for_timeout(100)
    pg.fill('#joinNick', 'Ana'); pg.click('#joinSubmitBtn'); pg.wait_for_timeout(400)
    r.caso('al unirse aparece «🔔 ¿Te avisamos?»', pg.is_visible('#avisosOferta') and '¿Te avisamos?' in pg.inner_text('#avisosOferta'))
    t = pg.inner_text('#avisosOferta')
    r.caso('la ventana explica los 3 avisos y la regla de «al menos 4»', 'llene' in t and 'entras a jugar' in t and 'al menos 4' in t)
    r.caso('30 minutos viene elegido', 'bg-wine-600' in pg.get_attribute('#avisosOferta [data-minutos="30"]', 'class'))
    r.caso('«No guardamos tu correo ni tu número»', 'No guardamos tu correo ni tu número' in t)
    pg.click('#avisosOferta [data-minutos="15"]')
    pg.click('#avisosOferta >> text=Activar avisos'); pg.wait_for_timeout(400)
    ap = aparatos(pg)
    d = list(ap.values())[0] if ap else {}
    r.caso('«Activar avisos» pide permiso al navegador', pg.evaluate('window.__permisoPedido') == 1)
    r.caso('se guarda el aparato con su token, 15 min y zona horaria', d.get('token') == 'token-1' and d.get('minutos') == 15 and d.get('zona') == 'America/Mexico_City', ap)
    r.caso('no se guarda correo ni teléfono', set(d.keys()) == {'token', 'minutos', 'zona', 'at'}, d)
    r.caso('usa la llave pública de config.js y el service worker firebase-messaging-sw.js', pg.evaluate('window.__vapid') == 'LLAVE-PRUEBA' and pg.evaluate('window.__sw') == 'firebase-messaging-sw.js')
    r.caso('avisa «Avisos activados (15 min antes)» y la barra cambia a «🔔 Avisos»', 'Avisos activados (15 min antes)' in pg.inner_text('body') and '🔔 Avisos' in pg.inner_text('#authBar'))
    r.caso('la ventana se cierra', not pg.is_visible('#avisosOferta'))

    # Menú
    pg.click('#authBar >> text=Avisos'); pg.wait_for_timeout(200)
    r.caso('menú: «Avisos en este celular» · ACTIVADOS', 'ACTIVADOS' in pg.inner_text('#avisosMenu') and 'DESACTIVADOS' not in pg.inner_text('#avisosMenu'))
    pg.click('#avisosMenu [data-minutos="30"]'); pg.wait_for_timeout(300)
    r.caso('menú: cambiar a 30 minutos se guarda de inmediato', list(aparatos(pg).values())[0].get('minutos') == 30)
    pg.click('#avisosMenu >> text=Mandarme un aviso de prueba'); pg.wait_for_timeout(300)
    f = pg.evaluate('window.__fetch')
    r.caso('aviso de prueba: lo pide al servidor (/api/aviso-prueba) con la sesión', f and f[-1] == ['/api/aviso-prueba', 'POST', 'Bearer id-token-ana'], f)
    r.caso('aviso de prueba: avisa que ya se envió', 'Aviso de prueba enviado' in pg.inner_text('body'))
    pg.evaluate("window.__alMensaje({ notification: { title: '¡Mesa completa! 🦇', body: 'Martes de V5' } })"); pg.wait_for_timeout(100)
    r.caso('con Elysium abierto, el aviso sale como mensaje en la página', '¡Mesa completa!' in pg.inner_text('#toastContainer'))
    pg.evaluate("abrirMesaDeAviso('m1')"); pg.wait_for_timeout(400)
    r.caso('al tocar el aviso con Elysium abierto, se va a la mesa (#mesa-m1)', pg.evaluate('location.hash') == '#mesa-m1' and 'ya terminó' not in pg.inner_text('#toastContainer'))
    pg.click('#authBar >> text=Avisos'); pg.wait_for_timeout(100)
    pg.click('#avisosMenu >> text=Desactivar'); pg.wait_for_timeout(300)
    r.caso('«Desactivar» borra el aparato y su token', aparatos(pg) == {} and pg.evaluate('window.__tokensBorrados') == 1, aparatos(pg))
    r.caso('después de desactivar la barra dice «🔕 Avisos»', '🔕 Avisos' in pg.inner_text('#authBar'))

    # La ventana no vuelve a salir; al cerrar sesión se borran los avisos
    pg.evaluate("window.__setUser({uid:'uidB', displayName:'Beto', getIdToken: () => Promise.resolve('x')})"); pg.wait_for_timeout(300)
    pg.click('text=¡Unirme a esta Mesa!'); pg.wait_for_timeout(100)
    pg.fill('#joinNick', 'Beto'); pg.click('#joinSubmitBtn'); pg.wait_for_timeout(400)
    r.caso('la ventana «¿Te avisamos?» sale una sola vez por aparato', not pg.is_visible('#avisosOferta'))
    pg.click('#authBar >> text=Avisos'); pg.click('#avisosMenu >> text=Activar avisos'); pg.wait_for_timeout(400)
    r.caso('desde el menú también se activan', len(aparatos(pg, 'uidB')) == 1)
    pg.click('#authBar >> text=Cerrar sesión'); pg.wait_for_timeout(400)
    r.caso('al cerrar sesión se borran los avisos de esa cuenta en este aparato', aparatos(pg, 'uidB') == {})
    err.revisar()
    ctx.close()

    # ------------------------------------------------------------------ al volver a abrir: sigue activado y renueva el token
    disp = 'dPRUEBA'
    seed2 = {'vtes_records': {}, 'stats': {}, 'avisos': {'uidA': {disp: {'token': 'token-viejo', 'minutos': 15, 'zona': 'America/Mexico_City', 'at': 1}}}}
    antes = "try { localStorage.setItem('elysium_avisos_disp', '%s'); } catch (e) {}" % disp
    ctx, pg, html = pagina(nav, 'avisos2.html', seed2, antes)
    pg.goto(url_archivo(html)); pg.evaluate("window.__permiso = 'granted'"); pg.wait_for_timeout(200)
    pg.evaluate(USUARIO); pg.wait_for_timeout(500)
    r.caso('al volver: «🔔 Avisos» (sigue activado en este aparato)', '🔔 Avisos' in pg.inner_text('#authBar'), pg.inner_text('#authBar'))
    r.caso('al volver: si el token cambió se actualiza', aparatos(pg).get(disp, {}).get('token') == 'token-1', aparatos(pg))
    pg.click('#authBar >> text=Avisos'); pg.wait_for_timeout(100)
    r.caso('al volver: el menú recuerda 15 minutos', 'bg-wine-600' in pg.get_attribute('#avisosMenu [data-minutos="15"]', 'class'))
    ctx.close()

    # ------------------------------------------------------------------ permiso negado
    ctx, pg, html = pagina(nav, 'avisos3.html')
    pg.goto(url_archivo(html)); pg.evaluate("window.__respuestaPermiso = 'denied'"); pg.evaluate(USUARIO); pg.wait_for_timeout(300)
    pg.evaluate('abrirMenuAvisos()'); pg.click('#avisosMenu >> text=Activar avisos'); pg.wait_for_timeout(300)
    r.caso('si no da permiso: explica cómo activarlo (candado → Notificaciones)', pg.is_visible('#avisosNoDisponible') and 'candado' in pg.inner_text('#avisosNoDisponible'))
    r.caso('si no da permiso: no se guarda nada', aparatos(pg) == {})
    ctx.close()

    # ------------------------------------------------------------------ iPhone
    UA_IPHONE = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1'
    ctx, pg, html = pagina(nav, 'avisos4.html', ua=UA_IPHONE)
    err = r.errores_de_pagina(pg, 'sin errores de JavaScript (iPhone)')
    pg.goto(url_archivo(html)); pg.evaluate(USUARIO); pg.wait_for_timeout(300)
    pg.evaluate('ofrecerAvisos()'); pg.click('#avisosOferta >> text=Activar avisos'); pg.wait_for_timeout(200)
    r.caso('iPhone en Safari: «Activar avisos» muestra la guía «En iPhone, primero instala Elysium»', pg.is_visible('#avisosGuiaIPhone') and 'primero instala Elysium' in pg.inner_text('#avisosGuiaIPhone'))
    g = pg.inner_text('#avisosGuiaIPhone')
    r.caso('la guía tiene los 4 pasos (Compartir, Agregar a pantalla de inicio, abrir desde el ícono, Activar avisos)',
           all(x in g for x in ['Toca Compartir', '«Agregar a pantalla de inicio»', 'Abre Elysium desde el ícono', 'Toca «Activar avisos»']))
    r.caso('la guía dice quitar el ícono viejo y que necesita iOS 16.4', 'Quítalo y vuelve a agregarlo' in g and 'iOS 16.4' in g)
    r.caso('iPhone en Safari: NO pide permiso (no funcionaría)', pg.evaluate('window.__permisoPedido') == 0)
    err.revisar()
    ctx.close()

    ctx, pg, html = pagina(nav, 'avisos5.html', ua=UA_IPHONE, app=True)
    pg.goto(url_archivo(html)); pg.evaluate(USUARIO); pg.wait_for_timeout(300)
    pg.evaluate('abrirMenuAvisos()'); pg.click('#avisosMenu >> text=Activar avisos'); pg.wait_for_timeout(400)
    r.caso('iPhone desde el ícono: pide permiso y se activan como en Android', pg.evaluate('window.__permisoPedido') == 1 and len(aparatos(pg)) == 1)
    ctx.close()

    ctx, pg, html = pagina(nav, 'avisos6.html', antes='window.__sinAvisos = true', ua=UA_IPHONE, app=True)
    pg.goto(url_archivo(html)); pg.evaluate(USUARIO); pg.wait_for_timeout(300)
    pg.evaluate('abrirMenuAvisos()'); pg.click('#avisosMenu >> text=Activar avisos'); pg.wait_for_timeout(200)
    r.caso('iPhone viejo (antes de iOS 16.4): sugiere usar «Calendario»', pg.is_visible('#avisosNoDisponible') and 'iOS 16.4' in pg.inner_text('#avisosNoDisponible') and 'Calendario' in pg.inner_text('#avisosNoDisponible'))
    ctx.close()

    ctx, pg, html = pagina(nav, 'avisos7.html', antes='window.__sinAvisos = true')
    pg.goto(url_archivo(html)); pg.evaluate(USUARIO); pg.wait_for_timeout(300)
    pg.evaluate('ofrecerAvisos()'); pg.wait_for_timeout(100)
    r.caso('computadora con navegador sin avisos: la ventana no se ofrece', not pg.is_visible('#avisosOferta'))
    ctx.close()

    # Sin llave configurada (como el sitio real mientras no se configure): nada cambia
    sin_llave = [(CONFIG_CON_LLAVE[0][0], "vapidKey: ''")]
    html = armar_pagina('index.html', {'vtes_records': {}, 'stats': {}}, 'avisos8.html', extra_head=SIMULADOR_AVISOS, config_extra=sin_llave)
    ctx = nuevo_contexto(nav); pg = ctx.new_page()
    pg.goto(url_archivo(html)); pg.evaluate(USUARIO); pg.wait_for_timeout(300)
    pg.evaluate('ofrecerAvisos()'); pg.wait_for_timeout(100)
    r.caso('sin la llave pública en config.js la ventana no aparece', not pg.is_visible('#avisosOferta'))
    ctx.close()
