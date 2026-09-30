# Resultados de las pruebas

**✅ TODO BIEN** — 223 de 223 casos pasaron.

- Fecha: 30/09/2026 17:53 (hora de Ciudad de México)
- Versión probada: `7b8438e` + cambios aún sin guardar
- Duración: 44 s
- Grupos corridos: todos
- Cómo se prueba: navegador automatizado con Firebase simulado (no toca datos reales). No sustituye la revisión en el sitio de pruebas: estilos y servicios de Google reales solo se ven ahí.

## Resumen por grupo

| # | Grupo | Casos | Resultado |
|---|---|---|---|
| 1 | Página principal: sesión, mesas, suplentes y veto | 44 | ✅ |
| 2 | Limpieza de vencidas, eventos semanales, salir, editar horario y cerrar | 9 | ✅ |
| 3 | Fichas de estadísticas por cuenta y guardado separado | 12 | ✅ |
| 4 | Aviso de bienvenida y experiencia de uso | 23 | ✅ |
| 5 | Las 3 páginas: config.js, comun.js, 💬, "Acerca de" y aviso legal | 44 | ✅ |
| 6 | Arranque: enlace por ciudad y enlace directo a una mesa | 6 | ✅ |
| 7 | Sitio servido como en GitHub, con sus archivos separados | 8 | ✅ |
| 8 | Orden de Asientos: confirmados, una mesa y reparto en mesas | 9 | ✅ |
| 9 | Página de estadísticas: acceso y conteo de personas | 17 | ✅ |
| 10 | Revisión del código: sintaxis, versiones e integridad | 27 | ✅ |
| 11 | Tarjetas: fecha y hora al frente, datos de la partida siempre visibles | 24 | ✅ |

## Todos los casos

### 1. Página principal: sesión, mesas, suplentes y veto

| # | Caso | Resultado |
|---|---|---|
| 1 | mesa antigua visible con sus jugadores (sin sesión) | ✅ |
| 2 | sin sesión no se ven botones de gestión | ✅ |
| 3 | la barra de sesión ofrece entrar | ✅ |
| 4 | al unirse sin sesión aparece la ventana de Google | ✅ |
| 5 | tras iniciar sesión se abre la ventana para unirse | ✅ |
| 6 | se guarda signups/uidA con nick y hora del servidor | ✅ |
| 7 | contador virtualJoins +1 | ✅ |
| 8 | Ana aparece como "tú" con botón Salir | ✅ |
| 9 | ya anotada: no aparece el botón para unirse otra vez | ✅ |
| 10 | Ana no organiza la mesa vieja: sin gestión | ✅ |
| 11 | con sesión, el formulario de crear se abre directo | ✅ |
| 12 | crear mesa: se guarda la mesa nueva | ✅ |
| 13 | mesa nueva con ownerUid y utcMs, sin PIN ni lista vieja | ✅ |
| 14 | la organizadora queda anotada en signups | ✅ |
| 15 | aparece la ventana "¡Mesa creada con éxito!" | ✅ |
| 16 | la organizadora ve sus botones de gestión | ✅ |
| 17 | la organizadora puede anotar a otra persona | ✅ |
| 18 | al anotar a otra persona el nick viene vacío | ✅ |
| 19 | persona anotada con llave aleatoria y la cuenta de la organizadora | ✅ |
| 20 | Beto no ve gestión en una mesa ajena | ✅ |
| 21 | un nick repetido (sin importar mayúsculas) se rechaza | ✅ |
| 22 | Beto queda anotado con su cuenta | ✅ |
| 23 | Beto no ve × para quitar a otros | ✅ |
| 24 | mesa llena (5/5) dice "Mesa llena" y ofrece suplente | ✅ |
| 25 | Eli aparece como suplente 1 con su botón de salir | ✅ |
| 26 | la ficha de estadísticas registra al suplente | ✅ |
| 27 | la organizadora ve × en los demás jugadores | ✅ |
| 28 | aviso: Eli (suplente) ocupa la plaza | ✅ |
| 29 | Beto quitado de la mesa | ✅ |
| 30 | el suplente que sube cuenta como unión | ✅ |
| 31 | la ficha registra al suplente promovido | ✅ |
| 32 | ya no hay suplentes en la tarjeta | ✅ |
| 33 | la barra muestra "Administrador" | ✅ |
| 34 | la administradora puede gestionar la mesa antigua | ✅ |
| 35 | Caro vetada y quitada de la mesa | ✅ |
| 36 | una cuenta vetada se muestra bloqueada | ✅ |
| 37 | una cuenta vetada no puede unirse | ✅ |
| 38 | la administradora quita un registro antiguo (Old1) | ✅ |
| 39 | evento presencial: se guarda la hora de llegada del organizador | ✅ |
| 40 | contador de eventos presenciales +1 | ✅ |
| 41 | el jugador edita su propia hora de llegada | ✅ |
| 42 | tras cerrar sesión no hay botones de gestión | ✅ |
| 43 | sin errores de JavaScript | ✅ |
| 44 | dentro de WhatsApp (Android) pide abrir en Chrome | ✅ |

### 2. Limpieza de vencidas, eventos semanales, salir, editar horario y cerrar

| # | Caso | Resultado |
|---|---|---|
| 1 | sin sesión no se intenta limpiar nada | ✅ |
| 2 | la mesa vencida no se muestra | ✅ |
| 3 | con sesión, la mesa vencida se borra | ✅ |
| 4 | evento semanal: solo cambia fecha y se vacían las listas | ✅ |
| 5 | evento semanal: nueva fecha dentro de lo que permiten las reglas | ✅ |
| 6 | Beto sale de la mesa por su cuenta | ✅ |
| 7 | editar horario guarda utcTime y utcMs juntos | ✅ |
| 8 | la organizadora cierra su mesa | ✅ |
| 9 | sin errores de JavaScript | ✅ |

### 3. Fichas de estadísticas por cuenta y guardado separado

| # | Caso | Resultado |
|---|---|---|
| 1 | al crear se guarda una ficha | ✅ |
| 2 | al crear: la ficha guarda la cuenta del organizador | ✅ |
| 3 | persona anotada por el organizador: cuenta por nick, no por cuenta | ✅ |
| 4 | cada jugador que se une queda con su cuenta | ✅ |
| 5 | el suplente no cuenta como jugador (solo en suplentes) | ✅ |
| 6 | el suplente que sube queda con su cuenta; el que salió se conserva | ✅ |
| 7 | sin errores de JavaScript | ✅ |
| 8 | el nombre de la mesa está limitado a 60 caracteres | ✅ |
| 9 | si las estadísticas fallan, la mesa se crea igual y aparece el aviso de éxito | ✅ |
| 10 | las estadísticas rechazadas no se guardan | ✅ |
| 11 | mesa y estadísticas se guardan en pasos separados | ✅ |
| 12 | sin errores de JavaScript (estadísticas rechazadas) | ✅ |

### 4. Aviso de bienvenida y experiencia de uso

| # | Caso | Resultado |
|---|---|---|
| 1 | sin sesión se ve el aviso de bienvenida | ✅ |
| 2 | botón grande "Entrar con Google" visible | ✅ |
| 3 | "Entendido" oculta el aviso | ✅ |
| 4 | el aviso no vuelve tras recargar | ✅ |
| 5 | el botón del aviso abre el inicio de sesión | ✅ |
| 6 | con sesión desaparecen el aviso y el botón | ✅ |
| 7 | sin errores de JavaScript (aviso) | ✅ |
| 8 | con 4 jugadores dice "Lista para jugar (4/5)" | ✅ |
| 9 | con 5 jugadores dice "Mesa llena (5/5)" | ✅ |
| 10 | ya no aparece "Mesa Completa" | ✅ |
| 11 | no quedan textos de 10–11 px | ✅ |
| 12 | botones × con descripción para lectores de pantalla | ✅ |
| 13 | zona táctil ampliada en × | ✅ |
| 14 | quitar suplente con descripción | ✅ |
| 15 | ✏️ más grande y con descripción | ✅ |
| 16 | 💬 con descripción | ✅ |
| 17 | sin errores de JavaScript (tarjetas) | ✅ |
| 18 | mientras llegan los datos dice "Cargando mesas…" | ✅ |
| 19 | al cambiar de pestaña sigue diciendo "Cargando" (no "no hay mesas") | ✅ |
| 20 | al llegar los datos aparecen las mesas | ✅ |
| 21 | sin errores de JavaScript (carga lenta) | ✅ |
| 22 | si Firebase falla muestra "No se pudo conectar" y botón para recargar | ✅ |
| 23 | sin errores de JavaScript (sin conexión) | ✅ |

### 5. Las 3 páginas: config.js, comun.js, 💬, "Acerca de" y aviso legal

| # | Caso | Resultado |
|---|---|---|
| 1 | index.html: no contiene datos propios del sitio (todo en config.js) | ✅ |
| 2 | sorteo.html: no contiene datos propios del sitio (todo en config.js) | ✅ |
| 3 | estadisticas.html: no contiene datos propios del sitio (todo en config.js) | ✅ |
| 4 | comun.js: no contiene datos propios del sitio (todo en config.js) | ✅ |
| 5 | js/arranque.js: no contiene datos propios del sitio (todo en config.js) | ✅ |
| 6 | js/compartir.js: no contiene datos propios del sitio (todo en config.js) | ✅ |
| 7 | js/fechas.js: no contiene datos propios del sitio (todo en config.js) | ✅ |
| 8 | js/mesas.js: no contiene datos propios del sitio (todo en config.js) | ✅ |
| 9 | js/sesion.js: no contiene datos propios del sitio (todo en config.js) | ✅ |
| 10 | js/tarjetas.js: no contiene datos propios del sitio (todo en config.js) | ✅ |
| 11 | js/ventanas.js: no contiene datos propios del sitio (todo en config.js) | ✅ |
| 12 | index.html: sin errores de JavaScript | ✅ |
| 13 | index.html: franja de pruebas visible según config.js | ✅ |
| 14 | index.html: Firebase arranca con el proyecto de config.js (vtes-uat) | ✅ |
| 15 | index.html: App Check se activa con la clave de config.js | ✅ |
| 16 | index.html: escapeHtml protege el texto | ✅ |
| 17 | index.html: normalizePlayer entiende "Jesus 8:05" | ✅ |
| 18 | index.html: botón 💬 visible | ✅ |
| 19 | index.html: 💬 abre su ventana | ✅ |
| 20 | index.html: 💬 envía el mensaje por EmailJS indicando la página (index) | ✅ |
| 21 | index.html: 💬 confirma el envío | ✅ |
| 22 | index.html: la línea del pie abre "Acerca de" | ✅ |
| 23 | index.html: aviso legal Dark Pack completo (logo, no oficial, texto de Paradox) | ✅ |
| 24 | index.html: Escape cierra "Acerca de" | ✅ |
| 25 | sorteo.html: sin errores de JavaScript | ✅ |
| 26 | sorteo.html: franja de pruebas visible según config.js | ✅ |
| 27 | sorteo.html: Firebase arranca con el proyecto de config.js (vtes-uat) | ✅ |
| 28 | sorteo.html: App Check se activa con la clave de config.js | ✅ |
| 29 | sorteo.html: escapeHtml protege el texto | ✅ |
| 30 | sorteo.html: normalizePlayer entiende "Jesus 8:05" | ✅ |
| 31 | sorteo.html: botón 💬 visible | ✅ |
| 32 | sorteo.html: 💬 abre su ventana | ✅ |
| 33 | sorteo.html: 💬 envía el mensaje por EmailJS indicando la página (sorteo) | ✅ |
| 34 | sorteo.html: 💬 confirma el envío | ✅ |
| 35 | sorteo.html: la línea del pie abre "Acerca de" | ✅ |
| 36 | sorteo.html: aviso legal Dark Pack completo (logo, no oficial, texto de Paradox) | ✅ |
| 37 | sorteo.html: Escape cierra "Acerca de" | ✅ |
| 38 | estadisticas.html: sin errores de JavaScript | ✅ |
| 39 | estadisticas.html: franja de pruebas visible según config.js | ✅ |
| 40 | estadisticas.html: Firebase arranca con el proyecto de config.js (vtes-uat) | ✅ |
| 41 | estadisticas.html: App Check se activa con la clave de config.js | ✅ |
| 42 | estadisticas.html: escapeHtml protege el texto | ✅ |
| 43 | estadisticas.html: sin botón 💬 (a propósito) | ✅ |
| 44 | al cambiar esPruebas, la franja aparece o desaparece | ✅ |

### 6. Arranque: enlace por ciudad y enlace directo a una mesa

| # | Caso | Resultado |
|---|---|---|
| 1 | enlace por ciudad: abre Presencial filtrado a Zaragoza | ✅ |
| 2 | enlace por ciudad: deja la dirección limpia (/Zaragoza) | ✅ |
| 3 | sin errores de JavaScript (enlace por ciudad) | ✅ |
| 4 | enlace directo: abre la pestaña correcta y muestra la mesa | ✅ |
| 5 | al arrancar escribe la zona horaria de quien visita | ✅ |
| 6 | sin errores de JavaScript (enlace directo) | ✅ |

### 7. Sitio servido como en GitHub, con sus archivos separados

| # | Caso | Resultado |
|---|---|---|
| 1 | index.html: sin errores de JavaScript | ✅ |
| 2 | index.html: carga los datos (Mesa Real) | ✅ |
| 3 | sorteo.html?tableId=m1: sin errores de JavaScript | ✅ |
| 4 | sorteo.html?tableId=m1: carga los datos (Ana) | ✅ |
| 5 | estadisticas.html: sin errores de JavaScript | ✅ |
| 6 | todos los archivos propios responden (sin 404) | ✅ |
| 7 | cada archivo de js/ se usa en la página principal | ✅ |
| 8 | config.js y comun.js se cargan | ✅ |

### 8. Orden de Asientos: confirmados, una mesa y reparto en mesas

| # | Caso | Resultado |
|---|---|---|
| 1 | carga los confirmados: primero los antiguos, luego por orden de llegada | ✅ |
| 2 | muestra el nombre del evento | ✅ |
| 3 | una mesa: el resultado incluye a los 5 con su presa | ✅ |
| 4 | reparto: 9→5+4, 10→5+5, 11→5+5 y 1 sin mesa, 7→5 y 2, 6→5 y 1, 8→4+4, 3→3 sin mesa | ✅ |
| 5 | se pueden agregar nombres a mano | ✅ |
| 6 | varias mesas: 9 jugadores quedan en 2 mesas, sin "Mesa Incompleta" | ✅ |
| 7 | varias mesas con 7: una mesa de 5 y "Mesa Incompleta" con 2 | ✅ |
| 8 | el sorteo no escribe nada en la base de datos | ✅ |
| 9 | sin errores de JavaScript | ✅ |

### 9. Página de estadísticas: acceso y conteo de personas

| # | Caso | Resultado |
|---|---|---|
| 1 | sin sesión: botón "Entrar con Google" y sin datos | ✅ |
| 2 | no hay campo de contraseña | ✅ |
| 3 | cuenta sin permiso: mensaje "sin acceso" y Cerrar sesión | ✅ |
| 4 | un lector de estadísticas ve los datos | ✅ |
| 5 | el lector no borra ni escribe nada | ✅ |
| 6 | al cambiar a una cuenta sin permiso se ocultan los datos | ✅ |
| 7 | cerrar sesión regresa al botón de entrar | ✅ |
| 8 | el administrador ve las estadísticas | ✅ |
| 9 | se dibujan las cifras | ✅ |
| 10 | sin errores de JavaScript (acceso) | ✅ |
| 11 | personas este mes: 3 (A, E, F) | ✅ |
| 12 | personas nuevas este mes: 2 (E, F) | ✅ |
| 13 | regresaron: 1 de las 3 del mes pasado (33%) | ✅ |
| 14 | personas que organizan en 3 meses: 3 (A, B, E) | ✅ |
| 15 | sin errores de JavaScript (personas) | ✅ |
| 16 | sin datos de cuentas: mensaje de espera | ✅ |
| 17 | sin errores de JavaScript (sin datos de cuentas) | ✅ |

### 10. Revisión del código: sintaxis, versiones e integridad

| # | Caso | Resultado |
|---|---|---|
| 1 | config.js: sintaxis correcta | ✅ |
| 2 | comun.js: sintaxis correcta | ✅ |
| 3 | js/arranque.js: sintaxis correcta | ✅ |
| 4 | js/compartir.js: sintaxis correcta | ✅ |
| 5 | js/fechas.js: sintaxis correcta | ✅ |
| 6 | js/mesas.js: sintaxis correcta | ✅ |
| 7 | js/sesion.js: sintaxis correcta | ✅ |
| 8 | js/tarjetas.js: sintaxis correcta | ✅ |
| 9 | js/ventanas.js: sintaxis correcta | ✅ |
| 10 | index.html: sintaxis correcta del código dentro de la página | ✅ |
| 11 | index.html: todos los archivos propios que carga existen | ✅ |
| 12 | index.html: carga config.js antes que comun.js | ✅ |
| 13 | index.html: config.js y comun.js van dentro del <body> (App Check lo necesita) | ✅ |
| 14 | index.html: los programas de jsDelivr tienen versión fija y huella de integridad | ✅ |
| 15 | index.html: arranque.js se carga al final | ✅ |
| 16 | index.html: todos los archivos de js/ con la misma versión ?v= | ✅ |
| 17 | sorteo.html: sintaxis correcta del código dentro de la página | ✅ |
| 18 | sorteo.html: todos los archivos propios que carga existen | ✅ |
| 19 | sorteo.html: carga config.js antes que comun.js | ✅ |
| 20 | sorteo.html: config.js y comun.js van dentro del <body> (App Check lo necesita) | ✅ |
| 21 | sorteo.html: los programas de jsDelivr tienen versión fija y huella de integridad | ✅ |
| 22 | estadisticas.html: sintaxis correcta del código dentro de la página | ✅ |
| 23 | estadisticas.html: todos los archivos propios que carga existen | ✅ |
| 24 | estadisticas.html: carga config.js antes que comun.js | ✅ |
| 25 | estadisticas.html: config.js y comun.js van dentro del <body> (App Check lo necesita) | ✅ |
| 26 | estadisticas.html: los programas de jsDelivr tienen versión fija y huella de integridad | ✅ |
| 27 | las 3 páginas usan la misma versión ?v= de config.js y comun.js | ✅ |

### 11. Tarjetas: fecha y hora al frente, datos de la partida siempre visibles

| # | Caso | Resultado |
|---|---|---|
| 1 | la tarjeta empieza con la fecha, luego la hora y después el nombre | ✅ |
| 2 | la fecha lleva el día completo ("martes 30 sep") | ✅ |
| 3 | el cupo va junto a la fecha: "Faltan 2 · 3/5" | ✅ |
| 4 | se ven 2 lugares "libre" | ✅ |
| 5 | virtual: dice "hora de Ciudad de México" (la zona de quien mira) | ✅ |
| 6 | zona sin nombre en la lista: usa la última parte ("Europe/Oslo" → "Oslo") | ✅ |
| 7 | plataforma y formato en una sola línea: "LackeyCCG · V5" | ✅ |
| 8 | sin sesión (espectador) se ve el Discord | ✅ |
| 9 | sin sesión se ve el renglón de contraseña, oculta con puntitos | ✅ |
| 10 | "Ver" muestra la contraseña y el botón cambia a "Ocultar" | ✅ |
| 11 | "Ocultar" la vuelve a esconder | ✅ |
| 12 | sin sesión no hay botones de editar Discord ni contraseña | ✅ |
| 13 | los botones ya no llevan emojis | ✅ |
| 14 | botón principal "¡Unirme a esta Mesa!" y secundarios WhatsApp · Compartir · Calendario | ✅ |
| 15 | el tiempo relativo sigue actualizándose (clase rel-time) | ✅ |
| 16 | presencial: dice "hora de Zaragoza" | ✅ |
| 17 | presencial: "Presencial · cada …" en una línea | ✅ |
| 18 | presencial: lugar, ciudad y "Ver mapa" | ✅ |
| 19 | presencial: sin lugares "libre" ni Discord | ✅ |
| 20 | presencial: cupo "1 confirmado" | ✅ |
| 21 | presencial: "Orden de Asientos" visible para todos | ✅ |
| 22 | organizador: "Organizas tú" en la línea de datos | ✅ |
| 23 | organizador: puede editar Discord y contraseña | ✅ |
| 24 | sin errores de JavaScript (tarjetas nuevas) | ✅ |
