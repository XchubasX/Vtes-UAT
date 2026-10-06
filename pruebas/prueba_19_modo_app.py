"""Modo app (ícono) e inicio de sesión con Google por nuestro dominio: worker.js, wrangler.jsonc, config.js y sesión."""
import json, re, subprocess
from herramientas import armar_pagina, url_archivo, nuevo_contexto, REPO

TITULO = 'Modo app desde el ícono e inicio de sesión con Google por nuestro dominio'


def correr(nav, r):
    # --- worker.js: solo /__/auth/ va a Firebase
    code = ("import('" + (REPO / 'worker.js').as_uri() + "').then(m => console.log(JSON.stringify(["
            "m.destinoAuth('https://uat.eternalschedule.com/__/auth/handler?apiKey=x', 'vtes-uat.firebaseapp.com'),"
            "m.destinoAuth('https://uat.eternalschedule.com/__/auth/iframe.js', 'vtes-uat.firebaseapp.com'),"
            "m.destinoAuth('https://uat.eternalschedule.com/Zaragoza', 'vtes-uat.firebaseapp.com'),"
            "m.destinoAuth('https://uat.eternalschedule.com/', 'vtes-uat.firebaseapp.com')])))")
    out = subprocess.run(['node', '--input-type=module', '-e', code], capture_output=True, text=True)
    res = json.loads(out.stdout or 'null') or [None] * 4
    r.caso('worker.js: /__/auth/handler se reenvía a Firebase con su consulta', res[0] == 'https://vtes-uat.firebaseapp.com/__/auth/handler?apiKey=x', res)
    r.caso('worker.js: /__/auth/iframe.js también', res[1] == 'https://vtes-uat.firebaseapp.com/__/auth/iframe.js', res)
    r.caso('worker.js: las páginas del sitio (/, /Zaragoza) NO se tocan', res[2] is None and res[3] is None, res)

    # --- wrangler.jsonc y publicación
    w = (REPO / 'wrangler.jsonc').read_text(encoding='utf-8')
    wj = json.loads(re.sub(r'^\s*//.*$', '', w, flags=re.M))
    cfg = (REPO / 'config.js').read_text(encoding='utf-8')
    proyecto = re.search(r'projectId:\s*"([^"]+)"', cfg).group(1)
    r.caso('wrangler: usa worker.js y el sitio con binding ASSETS', wj.get('main') == 'worker.js' and wj['assets'].get('binding') == 'ASSETS')
    r.caso('wrangler: el worker corre primero solo en /__/auth/* y /api/*', wj['assets'].get('run_worker_first') == ['/__/auth/*', '/api/*'])
    r.caso('wrangler: reenvía al Firebase de ESTE sitio (' + proyecto + ')', wj.get('vars', {}).get('FIREBASE_AUTH_HOST') == proyecto + '.firebaseapp.com', wj.get('vars'))
    pub = (REPO / 'cloudflare-publicar.sh').read_text(encoding='utf-8')
    r.caso('worker.js no se publica como archivo del sitio', 'worker.js' in pub)

    # --- config.js: authDomain según la dirección
    def auth_domain(host):
        code = 'var location={hostname:%s};var window={};%s;console.log(window.VTES_CONFIG.firebase.authDomain)' % (json.dumps(host), cfg)
        return subprocess.run(['node', '-e', code], capture_output=True, text=True).stdout.strip()
    for host, esperado in [('uat.eternalschedule.com', 'uat.eternalschedule.com'), ('eternalschedule.com', 'eternalschedule.com'),
                           ('elysium-uat.chubas.workers.dev', 'elysium-uat.chubas.workers.dev'), ('xchubasx.github.io', proyecto + '.firebaseapp.com'),
                           ('localhost', proyecto + '.firebaseapp.com')]:
        r.caso(f'config: en {host} el inicio de sesión pasa por {esperado}', auth_domain(host) == esperado, auth_domain(host))

    # --- Sesión: navegador normal → ventanita; modo app → página de Google
    ctx = nuevo_contexto(nav, viewport={'width': 390, 'height': 844})
    pg = ctx.new_page(); err = r.errores_de_pagina(pg, 'sin errores de JavaScript (modo app)')
    pg.goto(url_archivo(armar_pagina('index.html', {'vtes_records': {}, 'stats': {}}, 'modoapp.html'))); pg.wait_for_timeout(400)
    r.caso('en el navegador normal NO se considera modo app', pg.evaluate('abiertoComoApp()') is False)
    pg.evaluate("void (window.matchMedia = (q) => ({ matches: String(q).includes('standalone'), addListener(){}, removeListener(){} }))")
    r.caso('abierto desde el ícono SÍ se considera modo app', pg.evaluate('abiertoComoApp()') is True)
    pg.evaluate("document.getElementById('loginModal').classList.remove('hidden'); doGoogleLogin()"); pg.wait_for_timeout(200)
    r.caso('en modo app, «Entrar con Google» va a la página de Google (sin ventanita)', pg.evaluate('!!window.__redirigioAGoogle'))
    pg.evaluate("window.__RESULTADO_REDIRECT__ = { user: { uid: 'uidA' } }; resultadoEntrarConGoogle()"); pg.wait_for_timeout(200)
    r.caso('al regresar de Google avisa «Sesión iniciada»', 'Sesión iniciada' in pg.inner_text('body'))
    err.revisar()
    ctx.close()
