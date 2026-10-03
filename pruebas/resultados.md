# Resultados de las pruebas

**✅ TODO BIEN** — 356 de 356 casos pasaron.

- Fecha: 03/10/2026 09:30 (hora de Ciudad de México)
- Versión probada: `1d7c8fc`
- Duración: 64 s
- Grupos corridos: todos
- Cómo se prueba: navegador automatizado con Firebase simulado (no toca datos reales). No sustituye la revisión en el sitio de pruebas: estilos y servicios de Google reales solo se ven ahí.

## Resumen por grupo

| # | Grupo | Casos | Resultado |
|---|---|---|---|
| 1 | Página principal: sesión, mesas, suplentes y veto | 44 | ✅ |
| 2 | Limpieza de vencidas, eventos semanales, salir, editar horario y cerrar | 16 | ✅ |
| 3 | Fichas de estadísticas por cuenta y guardado separado | 12 | ✅ |
| 4 | Aviso de bienvenida y experiencia de uso | 23 | ✅ |
| 5 | Las 3 páginas: config.js, comun.js, 💬, "Acerca de" y aviso legal | 48 | ✅ |
| 6 | Arranque: enlace por ciudad y enlace directo a una mesa | 9 | ✅ |
| 7 | Sitio servido como en GitHub, con sus archivos separados | 8 | ✅ |
| 8 | Orden de Asientos: confirmados, una mesa y reparto en mesas | 9 | ✅ |
| 9 | Página de estadísticas: acceso y conteo de personas | 17 | ✅ |
| 10 | Revisión del código: sintaxis, versiones e integridad | 27 | ✅ |
| 11 | Tarjetas: fecha y hora al frente, datos de la partida siempre visibles | 36 | ✅ |
| 12 | Ícono del sitio e instalación en el celular | 11 | ✅ |
| 13 | Aviso temporal del ícono nuevo | 8 | ✅ |
| 14 | Mesas privadas: plegadas al final de la lista | 22 | ✅ |
| 15 | Aparatos: Android, iPhone, iPad, computadora y navegadores dentro de apps | 66 | ✅ |

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
| 8 | editar solo el horario no cambia el nombre | ✅ |
| 9 | la ventana se llama "Editar mesa" y trae el nombre actual | ✅ |
| 10 | cambiar solo el nombre lo guarda (sin espacios) y deja el horario igual | ✅ |
| 11 | la tarjeta muestra el nombre nuevo | ✅ |
| 12 | cambiar nombre y horario a la vez guarda los dos | ✅ |
| 13 | un nombre vacío no se guarda | ✅ |
| 14 | el campo de nombre limita a 60 caracteres | ✅ |
| 15 | la organizadora cierra su mesa | ✅ |
| 16 | sin errores de JavaScript | ✅ |

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
| 22 | index.html: ya no hay botón "?" en el encabezado | ✅ |
| 23 | index.html: el pie "Acerca de · Aviso legal" abre la ventana | ✅ |
| 24 | index.html: la ventana abre desde arriba ("Cómo funciona"), no en lo legal | ✅ |
| 25 | index.html: aviso legal Dark Pack completo (logo, no oficial, texto de Paradox) | ✅ |
| 26 | index.html: Escape cierra "Acerca de" | ✅ |
| 27 | sorteo.html: sin errores de JavaScript | ✅ |
| 28 | sorteo.html: franja de pruebas visible según config.js | ✅ |
| 29 | sorteo.html: Firebase arranca con el proyecto de config.js (vtes-uat) | ✅ |
| 30 | sorteo.html: App Check se activa con la clave de config.js | ✅ |
| 31 | sorteo.html: escapeHtml protege el texto | ✅ |
| 32 | sorteo.html: normalizePlayer entiende "Jesus 8:05" | ✅ |
| 33 | sorteo.html: botón 💬 visible | ✅ |
| 34 | sorteo.html: 💬 abre su ventana | ✅ |
| 35 | sorteo.html: 💬 envía el mensaje por EmailJS indicando la página (sorteo) | ✅ |
| 36 | sorteo.html: 💬 confirma el envío | ✅ |
| 37 | sorteo.html: ya no hay botón "?" en el encabezado | ✅ |
| 38 | sorteo.html: el pie "Acerca de · Aviso legal" abre la ventana | ✅ |
| 39 | sorteo.html: la ventana abre desde arriba ("Cómo funciona"), no en lo legal | ✅ |
| 40 | sorteo.html: aviso legal Dark Pack completo (logo, no oficial, texto de Paradox) | ✅ |
| 41 | sorteo.html: Escape cierra "Acerca de" | ✅ |
| 42 | estadisticas.html: sin errores de JavaScript | ✅ |
| 43 | estadisticas.html: franja de pruebas visible según config.js | ✅ |
| 44 | estadisticas.html: Firebase arranca con el proyecto de config.js (vtes-uat) | ✅ |
| 45 | estadisticas.html: App Check se activa con la clave de config.js | ✅ |
| 46 | estadisticas.html: escapeHtml protege el texto | ✅ |
| 47 | estadisticas.html: sin botón 💬 (a propósito) | ✅ |
| 48 | al cambiar esPruebas, la franja aparece o desaparece | ✅ |

### 6. Arranque: enlace por ciudad y enlace directo a una mesa

| # | Caso | Resultado |
|---|---|---|
| 1 | enlace por ciudad: abre Presencial filtrado a Zaragoza | ✅ |
| 2 | enlace por ciudad: deja la dirección limpia (/Zaragoza) | ✅ |
| 3 | sin errores de JavaScript (enlace por ciudad) | ✅ |
| 4 | enlace directo: abre la pestaña correcta y muestra la mesa | ✅ |
| 5 | al arrancar escribe la zona horaria de quien visita (con nombre legible) | ✅ |
| 6 | la zona horaria está dentro de la ventana Acerca de, no en el encabezado | ✅ |
| 7 | encabezado: ícono, "ELYSIUM / The Eternal Schedule" y la sesión (sin "?") | ✅ |
| 8 | título de la pestaña con el nombre nuevo | ✅ |
| 9 | sin errores de JavaScript (enlace directo) | ✅ |

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
| 14 | botón principal "¡Unirme a esta Mesa!" y secundarios Invitar · Calendario; ya no hay "Compartir" | ✅ |
| 15 | el menú de Invitar empieza cerrado | ✅ |
| 16 | al tocar Invitar se abre con "Mensaje por WhatsApp" y "Copiar enlace" | ✅ |
| 17 | el botón avisa a lectores de pantalla que el menú está abierto | ✅ |
| 18 | tocar fuera cierra el menú | ✅ |
| 19 | Escape cierra el menú | ✅ |
| 20 | "Mensaje por WhatsApp" abre WhatsApp con la invitación y cierra el menú | ✅ |
| 21 | en computadora abre WhatsApp Web directo (sin la página que daña los emojis) | ✅ |
| 22 | los emojis y saltos de línea van codificados correctamente | ✅ |
| 23 | las fechas de México, España y Chile usan el mismo formato ("jue, 8 oct") | ✅ |
| 24 | en celular usa api.whatsapp.com (abre la app) | ✅ |
| 25 | "Copiar enlace" copia el enlace directo (aunque el celular tenga menú de compartir) | ✅ |
| 26 | al copiar avisa "Enlace copiado" | ✅ |
| 27 | el tiempo relativo sigue actualizándose (clase rel-time) | ✅ |
| 28 | presencial: dice "hora de Zaragoza" | ✅ |
| 29 | presencial: "Presencial · cada …" en una línea | ✅ |
| 30 | presencial: lugar, ciudad y "Ver mapa" | ✅ |
| 31 | presencial: sin lugares "libre" ni Discord | ✅ |
| 32 | presencial: cupo "1 confirmado" | ✅ |
| 33 | presencial: "Orden de Asientos" visible para todos | ✅ |
| 34 | organizador: "Organizas tú" en la línea de datos | ✅ |
| 35 | organizador: puede editar Discord y contraseña | ✅ |
| 36 | sin errores de JavaScript (tarjetas nuevas) | ✅ |

### 12. Ícono del sitio e instalación en el celular

| # | Caso | Resultado |
|---|---|---|
| 1 | manifest: nombre completo "Elysium: The Eternal Schedule" y corto "Elysium" | ✅ |
| 2 | manifest: abre en el navegador normal (el inicio de sesión de Google sigue funcionando) | ✅ |
| 3 | manifest: empieza y se queda en la carpeta del sitio | ✅ |
| 4 | manifest: íconos 192, 512 y versión recortable, con su tamaño real | ✅ |
| 5 | iconos/apple-touch-icon.png existe y mide 180×180 | ✅ |
| 6 | iconos/favicon-32.png existe y mide 32×32 | ✅ |
| 7 | iconos/favicon.svg es un dibujo válido | ✅ |
| 8 | index.html: enlaza ícono, ícono de iPhone y manifest en el <head> | ✅ |
| 9 | sorteo.html: enlaza ícono, ícono de iPhone y manifest en el <head> | ✅ |
| 10 | estadisticas.html: enlaza ícono, ícono de iPhone y manifest en el <head> | ✅ |
| 11 | sitio servido: todos los archivos del ícono responden (200) | ✅ |

### 13. Aviso temporal del ícono nuevo

| # | Caso | Resultado |
|---|---|---|
| 1 | celular: el aviso se ve | ✅ |
| 2 | el texto menciona la "G" (Android) y la "V" (iPhone) | ✅ |
| 3 | "Entendido" lo cierra | ✅ |
| 4 | no vuelve a salir tras recargar | ✅ |
| 5 | a partir del 9 oct (hora de México) ya no se muestra | ✅ |
| 6 | el 8 oct a las 23:59 (México) todavía se muestra | ✅ |
| 7 | sin errores de JavaScript (aviso del ícono) | ✅ |
| 8 | computadora: el aviso no se muestra | ✅ |

### 14. Mesas privadas: plegadas al final de la lista

| # | Caso | Resultado |
|---|---|---|
| 1 | las públicas van primero por hora y la privada al final (aunque sea antes) | ✅ |
| 2 | plegada: una línea con "Privada", nombre y cupo | ✅ |
| 3 | plegada: no muestra Discord ni botones | ✅ |
| 4 | plegada: avisa a lectores de pantalla que se puede abrir | ✅ |
| 5 | al tocarla se despliega la tarjeta completa | ✅ |
| 6 | desplegada: lleva la etiqueta "Privada" junto al nombre | ✅ |
| 7 | desplegada: cualquiera ve "¡Unirme a esta Mesa!" | ✅ |
| 8 | sin sesión no se ve "Hacer pública" | ✅ |
| 9 | "Ocultar" la vuelve a plegar | ✅ |
| 10 | una persona cualquiera se une a la mesa privada | ✅ |
| 11 | después de unirse la mesa sigue desplegada | ✅ |
| 12 | el organizador ve "Hacer pública" | ✅ |
| 13 | "Hacer pública" quita el dato privada | ✅ |
| 14 | ya pública, vuelve a su lugar por hora | ✅ |
| 15 | "Hacer privada" guarda privada: true y la pliega | ✅ |
| 16 | el formulario de mesa virtual tiene la casilla "Mesa privada" | ✅ |
| 17 | crear con la casilla guarda privada: true | ✅ |
| 18 | al cerrar "Mesa creada", la privada nueva aparece plegada, como la ven todos | ✅ |
| 19 | al volver a abrir el formulario la casilla está desmarcada | ✅ |
| 20 | presencial: la casilla no aparece | ✅ |
| 21 | sin errores de JavaScript (mesas privadas) | ✅ |
| 22 | enlace directo (#mesa-…) a una privada la abre desplegada | ✅ |

### 15. Aparatos: Android, iPhone, iPad, computadora y navegadores dentro de apps

| # | Caso | Resultado |
|---|---|---|
| 1 | Android · Chrome: se reconoce como celular | ✅ |
| 2 | Android · Chrome: WhatsApp por la app | ✅ |
| 3 | Android · Chrome: no confunde navegador dentro de otra app | ✅ |
| 4 | Android · Chrome: nada se sale de la pantalla (412 px) | ✅ |
| 5 | Android · Chrome: al entrar muestra la ventana de Google | ✅ |
| 6 | Android · Chrome: sin errores de JavaScript | ✅ |
| 7 | Android · pantalla chica (360 px): se reconoce como celular | ✅ |
| 8 | Android · pantalla chica (360 px): WhatsApp por la app | ✅ |
| 9 | Android · pantalla chica (360 px): no confunde navegador dentro de otra app | ✅ |
| 10 | Android · pantalla chica (360 px): nada se sale de la pantalla (360 px) | ✅ |
| 11 | Android · pantalla chica (360 px): al entrar muestra la ventana de Google | ✅ |
| 12 | Android · pantalla chica (360 px): sin errores de JavaScript | ✅ |
| 13 | iPhone · Safari: se reconoce como celular | ✅ |
| 14 | iPhone · Safari: WhatsApp por la app | ✅ |
| 15 | iPhone · Safari: no confunde navegador dentro de otra app | ✅ |
| 16 | iPhone · Safari: nada se sale de la pantalla (390 px) | ✅ |
| 17 | iPhone · Safari: al entrar muestra la ventana de Google | ✅ |
| 18 | iPhone · Safari: sin errores de JavaScript | ✅ |
| 19 | iPhone SE (320 px): se reconoce como celular | ✅ |
| 20 | iPhone SE (320 px): WhatsApp por la app | ✅ |
| 21 | iPhone SE (320 px): no confunde navegador dentro de otra app | ✅ |
| 22 | iPhone SE (320 px): nada se sale de la pantalla (320 px) | ✅ |
| 23 | iPhone SE (320 px): al entrar muestra la ventana de Google | ✅ |
| 24 | iPhone SE (320 px): sin errores de JavaScript | ✅ |
| 25 | iPad · Safari (se presenta como Mac): se reconoce como celular | ✅ |
| 26 | iPad · Safari (se presenta como Mac): WhatsApp por la app | ✅ |
| 27 | iPad · Safari (se presenta como Mac): no confunde navegador dentro de otra app | ✅ |
| 28 | iPad · Safari (se presenta como Mac): nada se sale de la pantalla (820 px) | ✅ |
| 29 | iPad · Safari (se presenta como Mac): al entrar muestra la ventana de Google | ✅ |
| 30 | iPad · Safari (se presenta como Mac): sin errores de JavaScript | ✅ |
| 31 | Computadora Windows · Edge/Chrome: se reconoce como computadora | ✅ |
| 32 | Computadora Windows · Edge/Chrome: WhatsApp por WhatsApp Web directo | ✅ |
| 33 | Computadora Windows · Edge/Chrome: no confunde navegador dentro de otra app | ✅ |
| 34 | Computadora Windows · Edge/Chrome: nada se sale de la pantalla (1366 px) | ✅ |
| 35 | Computadora Windows · Edge/Chrome: al entrar muestra la ventana de Google | ✅ |
| 36 | Computadora Windows · Edge/Chrome: sin errores de JavaScript | ✅ |
| 37 | Mac · Safari: se reconoce como computadora | ✅ |
| 38 | Mac · Safari: WhatsApp por WhatsApp Web directo | ✅ |
| 39 | Mac · Safari: no confunde navegador dentro de otra app | ✅ |
| 40 | Mac · Safari: nada se sale de la pantalla (1440 px) | ✅ |
| 41 | Mac · Safari: al entrar muestra la ventana de Google | ✅ |
| 42 | Mac · Safari: sin errores de JavaScript | ✅ |
| 43 | Android · dentro de WhatsApp: se reconoce como celular | ✅ |
| 44 | Android · dentro de WhatsApp: WhatsApp por la app | ✅ |
| 45 | Android · dentro de WhatsApp: detecta navegador dentro de otra app | ✅ |
| 46 | Android · dentro de WhatsApp: nada se sale de la pantalla (412 px) | ✅ |
| 47 | Android · dentro de WhatsApp: al entrar pide abrir en Chrome | ✅ |
| 48 | Android · dentro de WhatsApp: sin errores de JavaScript | ✅ |
| 49 | iPhone · dentro de Instagram: se reconoce como celular | ✅ |
| 50 | iPhone · dentro de Instagram: WhatsApp por la app | ✅ |
| 51 | iPhone · dentro de Instagram: detecta navegador dentro de otra app | ✅ |
| 52 | iPhone · dentro de Instagram: nada se sale de la pantalla (390 px) | ✅ |
| 53 | iPhone · dentro de Instagram: al entrar pide abrir en Safari | ✅ |
| 54 | iPhone · dentro de Instagram: sin errores de JavaScript | ✅ |
| 55 | Android · dentro de Facebook: se reconoce como celular | ✅ |
| 56 | Android · dentro de Facebook: WhatsApp por la app | ✅ |
| 57 | Android · dentro de Facebook: detecta navegador dentro de otra app | ✅ |
| 58 | Android · dentro de Facebook: nada se sale de la pantalla (412 px) | ✅ |
| 59 | Android · dentro de Facebook: al entrar pide abrir en Chrome | ✅ |
| 60 | Android · dentro de Facebook: sin errores de JavaScript | ✅ |
| 61 | copiar enlace: copia el enlace directo a la mesa | ✅ |
| 62 | copiar enlace: si el navegador no deja copiar, lo muestra para copiarlo a mano | ✅ |
| 63 | calendario de Google: enlace con título, fechas y enlace a la mesa | ✅ |
| 64 | archivo de calendario (.ics): formato válido para iPhone y Outlook | ✅ |
| 65 | archivo de calendario: conserva acentos y emojis de las notas | ✅ |
| 66 | el calendario no incluye la contraseña de la partida | ✅ |
