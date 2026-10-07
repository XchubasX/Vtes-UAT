// Pruebas de la lógica de avisos del servidor (avisos-servidor.js), sin internet.
// La corre prueba_20_avisos.py y escribe una lista JSON de [nombre, ok, detalle].
import { planear, mensaje, aparatosDe, mandar, estable, cuando, resumenAvisos } from '../avisos-servidor.js';

const casos = [];
const caso = (n, ok, d = '') => casos.push([n, !!ok, ok ? '' : JSON.stringify(d).slice(0, 300)]);
const MIN = 60000;
const AHORA = Date.parse('2026-10-06T20:00:00Z'); // 14:00 en México
const iso = ms => new Date(ms).toISOString();
const s = (uid, nick, at) => ({ uid, nick, at });
function mesa(n, extra = {}, minutos = 120) {
  const signups = {};
  for (let i = 0; i < n; i++) signups['u' + i] = s('u' + i, 'Jugador' + i, i + 1);
  return { name: 'Martes de V5', modality: 'virtual', platform: 'Lackey', ownerUid: 'dueño', utcTime: iso(AHORA + minutos * MIN), signups, ...extra };
}
const tipos = r => r.eventos.map(e => e.tipo + (e.minutos ? e.minutos : '')).sort().join(',');

// --- Mesa completa
let r = planear({ m1: mesa(5) }, {}, AHORA);
caso('mesa virtual con 5: «¡Mesa completa!» al creador y a los 5', tipos(r) === 'completa' && r.eventos[0].uids.length === 6 && r.eventos[0].uids.includes('dueño'), r.eventos);
let r2 = planear({ m1: mesa(5) }, r.estado, AHORA + 5 * MIN);
caso('«¡Mesa completa!» llega una sola vez', r2.eventos.length === 0, r2.eventos);
let r3 = planear({ m1: mesa(4) }, r2.estado, AHORA + 10 * MIN);
let r4 = planear({ m1: mesa(5) }, r3.estado, AHORA + 15 * MIN);
caso('si alguien se sale y otro entra, NO se repite «completa»', !r4.eventos.some(e => e.tipo === 'completa'), r4.eventos);
caso('mesa con 4 (no llena): no hay «completa»', planear({ m1: mesa(4) }, {}, AHORA).eventos.length === 0);
const presencial = mesa(8, { modality: 'presencial', venue: 'Tienda X', city: 'Zaragoza', originTz: 'Europe/Madrid' });
caso('evento presencial con muchos confirmados: no hay «completa»', !planear({ p1: presencial }, {}, AHORA).eventos.some(e => e.tipo === 'completa'));
caso('mesa que ya empezó: no se avisa nada', planear({ m1: mesa(5, {}, -10) }, {}, AHORA).eventos.length === 0);

// --- Quién recibe
const conAnotado = mesa(4);
conAnotado.signups['-kotro'] = s('u0', 'AmigoDeJugador0', 10); // lo anotó Jugador0 con su cuenta
let rq = planear({ m1: conAnotado }, {}, AHORA);
caso('los que anota otra persona (llave ≠ uid) no cuentan como cuenta propia', rq.eventos[0] && rq.eventos[0].uids.filter(u => u === 'u0').length === 1, rq.eventos);
const legado = mesa(3); legado.players = ['Viejo1', 'Viejo2'];
caso('jugadores del formato anterior (sin cuenta) cuentan para llenar la mesa', planear({ m1: legado }, {}, AHORA).eventos.some(e => e.tipo === 'completa'));

// --- Aviso previo
const r30 = planear({ m1: mesa(4, {}, 29) }, { m1: { completa: true } }, AHORA);
caso('a 29 min con 4 jugadores: aviso de 30 min (no el de 15 todavía)', tipos(r30) === 'previo30', r30.eventos);
const r15 = planear({ m1: mesa(4, {}, 29) }, r30.estado, AHORA + 15 * MIN);
caso('a 14 min: aviso de 15 min y no se repite el de 30', tipos(r15) === 'previo15', r15.eventos);
const r15b = planear({ m1: mesa(4, {}, 29) }, r15.estado, AHORA + 20 * MIN);
caso('cada aviso previo llega una sola vez', r15b.eventos.length === 0, r15b.eventos);
caso('con 3 jugadores NO hay aviso previo para nadie (ni el creador)', planear({ m1: mesa(3, {}, 10) }, {}, AHORA).eventos.length === 0);
caso('a 2 horas no hay aviso previo todavía', planear({ m1: mesa(4, {}, 120) }, {}, AHORA).eventos.length === 0);
const r30b = planear({ m1: (() => { const m = mesa(4, {}, 29); m.signups.u9 = s('u9', 'Nuevo', 20); return m; })() }, r30.estado, AHORA + 4 * MIN);
caso('quien entra después del aviso de 30 min lo recibe solo él', r30b.eventos.length === 1 && r30b.eventos[0].uids.join() === 'u9', r30b.eventos);
const reprog = planear({ m1: mesa(4, {}, 29) }, { m1: { previo: { utc: 'otra-hora', m30: { dueño: true, u0: true, u1: true, u2: true, u3: true } } } }, AHORA);
caso('si cambian la hora de la mesa, el aviso previo vuelve a salir', tipos(reprog) === 'previo30', reprog.eventos);
const pres = planear({ p1: mesa(4, { modality: 'presencial', originTz: 'Europe/Madrid', venue: 'Tienda X', city: 'Zaragoza' }, 10) }, {}, AHORA);
caso('eventos presenciales: ningún aviso (ni previo ni nada)', pres.eventos.length === 0 && !('p1' in pres.estado), pres);

// --- Suplentes
const llena7 = mesa(7); // u0..u4 juegan, u5 y u6 suplentes
const e1 = planear({ m1: llena7 }, {}, AHORA);
caso('los suplentes no reciben «completa»', !e1.eventos[0].uids.includes('u5') && !e1.eventos[0].uids.includes('u6'), e1.eventos);
caso('se recuerda quiénes son suplentes', JSON.stringify(e1.estado.m1.suplentes) === '["u5","u6"]', e1.estado.m1);
const sinU2 = mesa(7); delete sinU2.signups.u2; // Jugador2 se sale → sube u5
const e2 = planear({ m1: sinU2 }, e1.estado, AHORA + 5 * MIN);
const ent = e2.eventos.find(e => e.tipo === 'entraste');
caso('cuando un suplente sube a jugador: «¡Entraste a la mesa!» solo a él', ent && ent.uids.join() === 'u5', e2.eventos);
caso('«Ocupas el lugar de Jugador2»', ent && ent.reemplazo === 'Jugador2', ent);
caso('al subir el suplente no se repite «completa»', !e2.eventos.some(e => e.tipo === 'completa'));
const e3 = planear({ m1: sinU2 }, e2.estado, AHORA + 10 * MIN);
caso('«¡Entraste a la mesa!» no se repite', e3.eventos.length === 0, e3.eventos);
const sup30 = planear({ m1: (() => { const m = mesa(7, {}, 25); return m; })() }, { m1: { completa: true } }, AHORA);
caso('aviso previo: los suplentes no lo reciben', sup30.eventos[0] && !sup30.eventos[0].uids.includes('u5'), sup30.eventos);

// --- Limpieza del estado
const lim = planear({}, { vieja: { completa: true }, _prueba: { x: 1 } }, AHORA);
caso('las mesas que ya no existen se borran de avisosEnviados', lim.estado.vieja === null && !('_prueba' in lim.estado), lim.estado);
caso('comparación estable sin importar el orden', estable({ a: 1, b: [1, { c: 2, d: 3 }] }) === estable({ b: [1, { d: 3, c: 2 }], a: 1 }));

// --- Textos
const ap = { token: 't', minutos: 30, zona: 'America/Mexico_City' };
const mC = mensaje({ tipo: 'completa', mesa: mesa(5, {}, 300) }, ap, AHORA);
caso('texto «completa»: nombre, «hoy 19:00 (Méx)» y «Ya están los 5»', mC.titulo === '¡Mesa completa! 🦇' && mC.texto === 'Martes de V5 · hoy 19:00 (Méx). Ya están los 5.', mC);
const mE = mensaje({ tipo: 'completa', mesa: mesa(5, {}, 300) }, { ...ap, zona: 'Europe/Madrid' }, AHORA);
caso('en España la hora sale en hora de España', mE.texto.includes('hoy 03:00 (Esp)') || mE.texto.includes('mañana 03:00 (Esp)'), mE);
const mS = mensaje({ tipo: 'entraste', mesa: mesa(5, {}, 300), reemplazo: 'Toni' }, ap, AHORA);
caso('texto «entraste»: «Ocupas el lugar de Toni (eras suplente)»', mS.titulo === '¡Entraste a la mesa! 🦇' && mS.texto.endsWith('Ocupas el lugar de Toni (eras suplente).'), mS);
const mP = mensaje({ tipo: 'previo', mesa: mesa(4, {}, 29), minutos: 30, jugadores: 4 }, ap, AHORA);
caso('texto previo: «En 30 minutos empieza tu mesa» con plataforma y «4 de 5 jugadores»', mP.titulo === 'En 30 minutos empieza tu mesa' && mP.texto.includes('Lackey') && mP.texto.includes('4 de 5 jugadores'), mP);
const mP2 = mensaje({ tipo: 'previo', mesa: mesa(4, {}, 12), minutos: 30, jugadores: 4 }, ap, AHORA);
caso('si el aviso sale tarde dice los minutos reales («En 12 minutos»)', mP2.titulo === 'En 12 minutos empieza tu mesa', mP2);
caso('«mañana» cuando es al día siguiente', cuando(iso(AHORA + 20 * 3600000), 'America/Mexico_City', AHORA).startsWith('mañana'), cuando(iso(AHORA + 20 * 3600000), 'America/Mexico_City', AHORA));

// --- Aparatos y envío
const avisos = { u1: { d1: { token: 'A', minutos: 15 }, d2: { token: 'B', minutos: 30 } } };
caso('aviso previo de 30 min: solo a los aparatos que eligieron 30', aparatosDe({ tipo: 'previo', minutos: 30 }, 'u1', avisos).map(x => x[0]).join() === 'd2');
caso('«completa»: a todos los aparatos de la persona', aparatosDe({ tipo: 'completa' }, 'u1', avisos).length === 2);
caso('persona sin avisos activados: no se le manda nada', aparatosDe({ tipo: 'completa' }, 'u7', avisos).length === 0);
const llamadas = [];
const enviar = async (tok, m, link) => { llamadas.push([tok, link]); return tok === 'B' ? 'borrar' : 'ok'; };
const res = await mandar([{ tipo: 'completa', mesaId: 'm1', mesa: mesa(5), uids: ['u1'] }], avisos, enviar, 'https://uat.eternalschedule.com', AHORA);
caso('al tocar el aviso se abre la mesa (#mesa-…)', llamadas[0] && llamadas[0][1] === 'https://uat.eternalschedule.com/#mesa-m1', llamadas);
caso('los aparatos que ya no existen se borran de avisos/', JSON.stringify(res.borrar) === '{"avisos/u1/d2":null}' && res.enviados === 1, res);

// --- Totales para Estadísticas (tablero 25)
const res2 = resumenAvisos({
  ana: { d1: { token: 'a', minutos: 30, tipo: 'iphone' }, d2: { token: 'b', minutos: 15, tipo: 'pc' } },
  beto: { d3: { token: 'c', minutos: 30, tipo: 'android' } },
  caro: { d4: { token: 'd', minutos: 30 } },
  vacio: {}
});
caso('Estadísticas: personas, aparatos, tipo y 15/30', estable(res2) === estable({ personas: 3, aparatos: 4, tipos: { iphone: 1, android: 1, pc: 1, sinDato: 1 }, minutos: { m15: 1, m30: 3 } }), res2);
caso('Estadísticas: los totales no llevan uid, token ni nombres', !/ana|beto|caro|"a"|token/.test(JSON.stringify(res2)), res2);

console.log(JSON.stringify(casos));
