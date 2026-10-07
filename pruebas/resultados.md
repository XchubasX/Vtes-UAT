# Resultados de las pruebas

**✅ TODO BIEN** — 89 de 89 casos pasaron.

- Fecha: 06/10/2026 18:30 (hora de Ciudad de México)
- Versión probada: `b201f2d` + cambios aún sin guardar
- Duración: 13 s
- Grupos corridos: solo los que contienen «prueba_20»
- Cómo se prueba: navegador automatizado con Firebase simulado (no toca datos reales). No sustituye la revisión en el sitio de pruebas: estilos y servicios de Google reales solo se ven ahí.

## Resumen por grupo

| # | Grupo | Casos | Resultado |
|---|---|---|---|
| 1 | Avisos de mesa en el celular (completa, suplente que entra y aviso previo) | 89 | ✅ |

## Todos los casos

### 1. Avisos de mesa en el celular (completa, suplente que entra y aviso previo)

| # | Caso | Resultado |
|---|---|---|
| 1 | servidor: mesa virtual con 5: «¡Mesa completa!» al creador y a los 5 | ✅ |
| 2 | servidor: «¡Mesa completa!» llega una sola vez | ✅ |
| 3 | servidor: si alguien se sale y otro entra, NO se repite «completa» | ✅ |
| 4 | servidor: mesa con 4 (no llena): no hay «completa» | ✅ |
| 5 | servidor: evento presencial con muchos confirmados: no hay «completa» | ✅ |
| 6 | servidor: mesa que ya empezó: no se avisa nada | ✅ |
| 7 | servidor: los que anota otra persona (llave ≠ uid) no cuentan como cuenta propia | ✅ |
| 8 | servidor: jugadores del formato anterior (sin cuenta) cuentan para llenar la mesa | ✅ |
| 9 | servidor: a 29 min con 4 jugadores: aviso de 30 min (no el de 15 todavía) | ✅ |
| 10 | servidor: a 14 min: aviso de 15 min y no se repite el de 30 | ✅ |
| 11 | servidor: cada aviso previo llega una sola vez | ✅ |
| 12 | servidor: con 3 jugadores NO hay aviso previo para nadie (ni el creador) | ✅ |
| 13 | servidor: a 2 horas no hay aviso previo todavía | ✅ |
| 14 | servidor: quien entra después del aviso de 30 min lo recibe solo él | ✅ |
| 15 | servidor: si cambian la hora de la mesa, el aviso previo vuelve a salir | ✅ |
| 16 | servidor: evento presencial con 4 confirmados: hay aviso previo | ✅ |
| 17 | servidor: los suplentes no reciben «completa» | ✅ |
| 18 | servidor: se recuerda quiénes son suplentes | ✅ |
| 19 | servidor: cuando un suplente sube a jugador: «¡Entraste a la mesa!» solo a él | ✅ |
| 20 | servidor: «Ocupas el lugar de Jugador2» | ✅ |
| 21 | servidor: al subir el suplente no se repite «completa» | ✅ |
| 22 | servidor: «¡Entraste a la mesa!» no se repite | ✅ |
| 23 | servidor: aviso previo: los suplentes no lo reciben | ✅ |
| 24 | servidor: las mesas que ya no existen se borran de avisosEnviados | ✅ |
| 25 | servidor: comparación estable sin importar el orden | ✅ |
| 26 | servidor: texto «completa»: nombre, «hoy 19:00 (Méx)» y «Ya están los 5» | ✅ |
| 27 | servidor: en España la hora sale en hora de España | ✅ |
| 28 | servidor: texto «entraste»: «Ocupas el lugar de Toni (eras suplente)» | ✅ |
| 29 | servidor: texto previo: «En 30 minutos empieza tu mesa» con plataforma y «4 de 5 jugadores» | ✅ |
| 30 | servidor: si el aviso sale tarde dice los minutos reales («En 12 minutos») | ✅ |
| 31 | servidor: presencial: hora del lugar, tienda y «6 confirmados» | ✅ |
| 32 | servidor: «mañana» cuando es al día siguiente | ✅ |
| 33 | servidor: aviso previo de 30 min: solo a los aparatos que eligieron 30 | ✅ |
| 34 | servidor: «completa»: a todos los aparatos de la persona | ✅ |
| 35 | servidor: persona sin avisos activados: no se le manda nada | ✅ |
| 36 | servidor: al tocar el aviso se abre la mesa (#mesa-…) | ✅ |
| 37 | servidor: los aparatos que ya no existen se borran de avisos/ | ✅ |
| 38 | wrangler: cron cada 5 minutos | ✅ |
| 39 | wrangler: el worker atiende /api/* (aviso de prueba) | ✅ |
| 40 | wrangler: base de datos y llave del MISMO proyecto que config.js (vtes-uat) | ✅ |
| 41 | wrangler: la cuenta de servicio NO está en el archivo (es secreto de Cloudflare) | ✅ |
| 42 | wrangler: los avisos abren el sitio correcto (pruebas → uat) | ✅ |
| 43 | avisos-servidor.js no se publica como archivo del sitio | ✅ |
| 44 | service worker: usa config.js y la misma versión de Firebase que la página (9.23.0) | ✅ |
| 45 | service worker: atiende el toque ANTES que Firebase (abre la mesa aunque Elysium ya esté abierto) | ✅ |
| 46 | servidor: el aviso lleva el enlace y la mesa en sus datos | ✅ |
| 47 | la página carga firebase-messaging-compat de la misma versión | ✅ |
| 48 | worker: /api/aviso-prueba solo acepta POST | ✅ |
| 49 | worker: sin el secreto configurado responde «falta la cuenta de servicio» (503) | ✅ |
| 50 | worker: las páginas del sitio siguen igual | ✅ |
| 51 | worker: tiene la tarea programada (scheduled) | ✅ |
| 52 | sin sesión no aparece el botón «Avisos» | ✅ |
| 53 | con sesión aparece «🔕 Avisos» junto a «Cerrar sesión» | ✅ |
| 54 | al unirse aparece «🔔 ¿Te avisamos?» | ✅ |
| 55 | la ventana explica los 3 avisos y la regla de «al menos 4» | ✅ |
| 56 | 30 minutos viene elegido | ✅ |
| 57 | «No guardamos tu correo ni tu número» | ✅ |
| 58 | «Activar avisos» pide permiso al navegador | ✅ |
| 59 | se guarda el aparato con su token, 15 min y zona horaria | ✅ |
| 60 | no se guarda correo ni teléfono | ✅ |
| 61 | usa la llave pública de config.js y el service worker firebase-messaging-sw.js | ✅ |
| 62 | avisa «Avisos activados (15 min antes)» y la barra cambia a «🔔 Avisos» | ✅ |
| 63 | la ventana se cierra | ✅ |
| 64 | menú: «Avisos en este celular» · ACTIVADOS | ✅ |
| 65 | menú: cambiar a 30 minutos se guarda de inmediato | ✅ |
| 66 | aviso de prueba: lo pide al servidor (/api/aviso-prueba) con la sesión | ✅ |
| 67 | aviso de prueba: avisa que ya se envió | ✅ |
| 68 | con Elysium abierto, el aviso sale como mensaje en la página | ✅ |
| 69 | al tocar el aviso con Elysium abierto, se va a la mesa (#mesa-m1) | ✅ |
| 70 | «Desactivar» borra el aparato y su token | ✅ |
| 71 | después de desactivar la barra dice «🔕 Avisos» | ✅ |
| 72 | la ventana «¿Te avisamos?» sale una sola vez por aparato | ✅ |
| 73 | desde el menú también se activan | ✅ |
| 74 | al cerrar sesión se borran los avisos de esa cuenta en este aparato | ✅ |
| 75 | sin errores de JavaScript (avisos en computadora) | ✅ |
| 76 | al volver: «🔔 Avisos» (sigue activado en este aparato) | ✅ |
| 77 | al volver: si el token cambió se actualiza | ✅ |
| 78 | al volver: el menú recuerda 15 minutos | ✅ |
| 79 | si no da permiso: explica cómo activarlo (candado → Notificaciones) | ✅ |
| 80 | si no da permiso: no se guarda nada | ✅ |
| 81 | iPhone en Safari: «Activar avisos» muestra la guía «En iPhone, primero instala Elysium» | ✅ |
| 82 | la guía tiene los 4 pasos (Compartir, Agregar a pantalla de inicio, abrir desde el ícono, Activar avisos) | ✅ |
| 83 | la guía dice quitar el ícono viejo y que necesita iOS 16.4 | ✅ |
| 84 | iPhone en Safari: NO pide permiso (no funcionaría) | ✅ |
| 85 | sin errores de JavaScript (iPhone) | ✅ |
| 86 | iPhone desde el ícono: pide permiso y se activan como en Android | ✅ |
| 87 | iPhone viejo (antes de iOS 16.4): sugiere usar «Calendario» | ✅ |
| 88 | computadora con navegador sin avisos: la ventana no se ofrece | ✅ |
| 89 | sin la llave pública en config.js la ventana no aparece | ✅ |
