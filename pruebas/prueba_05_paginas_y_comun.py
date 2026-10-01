"""Las 3 páginas con config.js y comun.js: Firebase, App Check, franja, 💬, "Acerca de" y aviso legal."""
import re
from herramientas import armar_pagina, url_archivo, nuevo_contexto, REPO

TITULO = 'Las 3 páginas: config.js, comun.js, 💬, "Acerca de" y aviso legal'

# Registra con qué datos arrancan Firebase y App Check
ESPIA = """<script>window.__initArgs=null;(function(){const o=firebase.initializeApp; firebase.initializeApp=function(c){window.__initArgs=c; return o&&o.apply(this,arguments);};
 const a=firebase.appCheck; firebase.appCheck=function(){const r=a.apply(this,arguments); const act=r.activate; r.activate=function(p,t){window.__appCheckKey=p&&p.__key; return act.apply(this,arguments);}; return r;};
 firebase.appCheck.ReCaptchaEnterpriseProvider=function(k){this.__key=k;}; })();</script>"""


def correr(nav, r):
    cfg = (REPO / 'config.js').read_text(encoding='utf-8')
    proyecto = re.search(r'projectId: "([^"]+)"', cfg).group(1)
    clave = re.search(r"recaptchaKey: '([^']+)'", cfg).group(1)
    es_pruebas = 'esPruebas: true' in cfg

    # Las páginas y el código compartido no deben tener datos propios de un sitio
    datos = r'vtes-uat|vtes-scheduler|6LfWd7|6Lc2QL|AIzaSy|801358504439|897608138023'
    for rel in ['index.html', 'sorteo.html', 'estadisticas.html', 'comun.js'] + [f'js/{p.name}' for p in sorted((REPO / 'js').glob('*.js'))]:
        texto = (REPO / rel).read_text(encoding='utf-8').replace('@vtes-scheduler`', '')  # identificador fijo de eventos de calendario
        hallado = re.findall(datos, texto)
        r.caso(f'{rel}: no contiene datos propios del sitio (todo en config.js)', not hallado, hallado[:3])

    ctx = nuevo_contexto(nav)
    for archivo in ['index.html', 'sorteo.html', 'estadisticas.html']:
        pg = ctx.new_page(); err = r.errores_de_pagina(pg, f'{archivo}: sin errores de JavaScript')
        pg.goto(url_archivo(armar_pagina(archivo, {'stats': {}}, 'c_' + archivo, extra_head=ESPIA))); pg.wait_for_timeout(400)
        err.revisar()
        franja = 'SITIO DE PRUEBAS' in pg.inner_text('body')[:300]
        r.caso(f'{archivo}: franja de pruebas {"visible" if es_pruebas else "oculta"} según config.js', franja == es_pruebas)
        ia = pg.evaluate('window.__initArgs') or {}
        r.caso(f'{archivo}: Firebase arranca con el proyecto de config.js ({proyecto})', ia.get('projectId') == proyecto, ia.get('projectId'))
        r.caso(f'{archivo}: App Check se activa con la clave de config.js', pg.evaluate('window.__appCheckKey') == clave)
        r.caso(f'{archivo}: escapeHtml protege el texto', pg.evaluate("escapeHtml(`<b a='1'>&`)") == '&lt;b a=&#39;1&#39;&gt;&amp;')
        if archivo == 'estadisticas.html':
            r.caso('estadisticas.html: sin botón 💬 (a propósito)', pg.query_selector('#feedbackModal') is None)
            pg.close(); continue
        r.caso(f'{archivo}: normalizePlayer entiende "Jesus 8:05"', pg.evaluate("JSON.stringify(normalizePlayer('Jesus 8:05'))") == '{"nick":"Jesus","arrival":"08:05"}')
        r.caso(f'{archivo}: botón 💬 visible', pg.is_visible('button[onclick="openFeedbackModal()"]'))
        pg.click('button[onclick="openFeedbackModal()"]'); pg.wait_for_timeout(100)
        r.caso(f'{archivo}: 💬 abre su ventana', pg.is_visible('#feedbackModal'))
        pg.fill('#feedbackMessage', 'hola prueba'); pg.click('#feedbackSubmitBtn'); pg.wait_for_timeout(200)
        sent = pg.evaluate('window.__sent')
        quiere = 'sorteo' if archivo == 'sorteo.html' else 'index'
        r.caso(f'{archivo}: 💬 envía el mensaje por EmailJS indicando la página ({quiere})', len(sent) == 1 and sent[0]['message'] == 'hola prueba' and sent[0]['page'] == quiere, sent)
        r.caso(f'{archivo}: 💬 confirma el envío', 'Gracias' in pg.inner_text('#feedbackStatus'))
        pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
        r.caso(f'{archivo}: ya no hay botón "?" en el encabezado', pg.locator('header button[onclick^="openAboutModal"]').count() == 0)
        pg.click('footer >> text=Acerca de · Aviso legal'); pg.wait_for_timeout(150)
        r.caso(f'{archivo}: el pie "Acerca de · Aviso legal" abre la ventana', pg.is_visible('#aboutModal'))
        r.caso(f'{archivo}: la ventana abre desde arriba ("Cómo funciona"), no en lo legal',
               pg.evaluate("(() => { const m = document.querySelector('#aboutModal [class*=overflow-y-auto]') || document.getElementById('aboutModal'); return m.scrollTop === 0; })()"))
        legal = pg.inner_text('#aboutLegal') if pg.query_selector('#aboutLegal') else ''
        r.caso(f'{archivo}: aviso legal Dark Pack completo (logo, no oficial, texto de Paradox)',
               pg.query_selector('#aboutLegal img') is not None and 'no oficial' in legal and 'Paradox Interactive AB, and are used with permission' in legal)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
        r.caso(f'{archivo}: Escape cierra "Acerca de"', not pg.is_visible('#aboutModal'))
        pg.close()

    # Con esPruebas cambiado al contrario, la franja se comporta al revés
    otro = ('esPruebas: true', 'esPruebas: false') if es_pruebas else ('esPruebas: false', 'esPruebas: true')
    pg = ctx.new_page()
    pg.goto(url_archivo(armar_pagina('index.html', {'stats': {}}, 'c_invertido.html', config_extra=[otro]))); pg.wait_for_timeout(300)
    r.caso('al cambiar esPruebas, la franja aparece o desaparece', ('SITIO DE PRUEBAS' in pg.inner_text('body')[:300]) != es_pruebas)
    ctx.close()
