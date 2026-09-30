"""Orden de Asientos (sorteo.html): lista de confirmados, sorteo de una mesa y reparto en varias mesas."""
from herramientas import armar_pagina, url_archivo, nuevo_contexto, ahora_ms, iso, DIA

TITULO = 'Orden de Asientos: confirmados, una mesa y reparto en mesas'


def correr(nav, r):
    fut = ahora_ms() + DIA
    seed = {'vtes_records': {'ev': {'type': 'custom_table', 'name': 'Torneo', 'venue': 'Tienda', 'utcTime': iso(fut), 'utcMs': fut,
                                    'modality': 'presencial', 'originTz': 'America/Mexico_City', 'ownerUid': 'u1',
                                    'players': ['Viejo1', 'Viejo2 18:00'],
                                    'signups': {'u2': {'uid': 'u2', 'nick': 'Segundo', 'at': 20}, 'u1': {'uid': 'u1', 'nick': 'Primero', 'at': 10},
                                                'x3': {'uid': 'u1', 'nick': 'Tercero', 'at': 30}}}}, 'stats': {}}
    ruta = armar_pagina('sorteo.html', seed, 'sorteo.html')
    ctx = nuevo_contexto(nav)
    pg = ctx.new_page(); err = r.errores_de_pagina(pg)
    pg.goto(url_archivo(ruta, '?tableId=ev')); pg.wait_for_timeout(400)
    nombres = pg.evaluate('candidateNames.map(n => n.nick)')
    r.caso('carga los confirmados: primero los antiguos, luego por orden de llegada', nombres == ['Viejo1', 'Viejo2', 'Primero', 'Segundo', 'Tercero'], nombres)
    r.caso('muestra el nombre del evento', 'Torneo' in pg.inner_text('#eventLabel'))
    pg.click('#sortearBtn'); pg.wait_for_timeout(300)
    orden = pg.inner_text('#orderList-single')
    r.caso('una mesa: el resultado incluye a los 5 con su presa', all(n in orden for n in nombres) and orden.count('presa') == 5, orden[:200])

    tam = pg.evaluate('[9,10,11,7,6,8,3].map(n => { const t = computeTableSizes(n); return t.sizes.join("+") + "|" + t.leftover; })')
    r.caso('reparto: 9→5+4, 10→5+5, 11→5+5 y 1 sin mesa, 7→5 y 2, 6→5 y 1, 8→4+4, 3→3 sin mesa',
           tam == ['5+4|0', '5+5|0', '5+5|1', '5|2', '5|1', '4+4|0', '|3'], tam)
    # Agregar nombres a mano hasta 9 y repartir
    for n in ['A', 'B', 'C', 'D']:
        pg.fill('#extraNameInput', n); pg.keyboard.press('Enter'); pg.wait_for_timeout(50)
    r.caso('se pueden agregar nombres a mano', pg.evaluate('candidateNames.length') == 9)
    pg.click('#modeMultiBtn'); pg.wait_for_timeout(100)
    pg.click('#sortearBtn'); pg.wait_for_timeout(300)
    res = pg.inner_text('#resultContent')
    r.caso('varias mesas: 9 jugadores quedan en 2 mesas, sin "Mesa Incompleta"', res.count('presa') == 9 and 'Incompleta' not in res, res[:200])
    pg.evaluate('toggleCheck(0); toggleCheck(1)'); pg.wait_for_timeout(100)
    pg.click('#sortearBtn'); pg.wait_for_timeout(300)
    r.caso('varias mesas con 7: una mesa de 5 y "Mesa Incompleta" con 2', 'Mesa Incompleta' in pg.inner_text('#resultContent') and '2 personas' in pg.inner_text('#resultContent'))
    r.caso('el sorteo no escribe nada en la base de datos', pg.evaluate('window.__writes.length') == 0)
    err.revisar()
    ctx.close()
