# Pruebas automáticas del Organizador VTES

Pruebas que abren las páginas reales del sitio en un navegador automatizado, con
**Firebase simulado** (no tocan ninguna base de datos real ni necesitan internet).
Viven solo en este repositorio de pruebas (Vtes-UAT) y **no se publican** en la página
(ver `_config.yml` en la raíz).

## Cómo correrlas

Desde la carpeta del repositorio:

```
python3 pruebas/correr.py            # todas
python3 pruebas/correr.py sorteo     # solo los grupos cuyo archivo contiene "sorteo"
```

Necesita Python 3, Playwright con Chromium y Node (para revisar la sintaxis).
El entorno de Claude ya los trae.

Al terminar escribe **`pruebas/resultados.md`** con cada caso (✅ o ❌), la fecha y la
versión probada. Ese reporte se guarda junto con cada cambio, así queda el historial.

## Regla de trabajo

1. Antes de publicar cualquier cambio en el sitio de pruebas: correr `pruebas/correr.py`
   y guardar el `resultados.md` que genera en el mismo envío.
2. Si se agrega o cambia una función del sitio, agregar o ajustar su prueba.
3. Las pruebas **no sustituyen** la revisión en el sitio de pruebas: los estilos reales,
   Google (inicio de sesión, App Check) y el celular solo se ven ahí.

## Archivos

| Archivo | Qué es |
|---|---|
| `correr.py` | Corre todo y escribe `resultados.md`. |
| `herramientas.py` | Arma las páginas de prueba, sirve el sitio como GitHub Pages, registra resultados. |
| `firebase-simulado.js` | Firebase falso en memoria (base de datos, sesión, App Check). Imita también que App Check falla si se activa antes de que exista el `<body>`. |
| `prueba_01_principal.py` | Sesión, crear, unirse, anotar a otros, suplentes, veto, eventos presenciales, WhatsApp. |
| `prueba_02_limpieza_horario.py` | Mesas vencidas, eventos semanales, salir, editar horario, cerrar. |
| `prueba_03_fichas_estadisticas.py` | Fichas por cuenta; la mesa se guarda aunque fallen las estadísticas. |
| `prueba_04_aviso_y_experiencia.py` | Aviso de bienvenida, "Lista para jugar"/"Mesa llena", botones accesibles, letra, "Cargando" y error. |
| `prueba_05_paginas_y_comun.py` | Las 3 páginas con `config.js` y `comun.js`, 💬, "Acerca de", aviso legal Dark Pack. |
| `prueba_06_arranque.py` | Enlace por ciudad (`/Zaragoza`) y enlace directo (`#mesa-…`). |
| `prueba_07_archivos_reales.py` | El sitio servido con sus archivos separados de verdad, como en GitHub. |
| `prueba_08_sorteo.py` | Orden de Asientos: confirmados, una mesa, reparto en mesas de 4 y 5. |
| `prueba_09_pagina_estadisticas.py` | Acceso a estadísticas y conteo de personas (fechas relativas al mes actual). |
| `prueba_10_revision_codigo.py` | Sintaxis, versiones `?v=`, huellas de integridad y orden de carga. |

Para agregar un grupo nuevo: crear `prueba_NN_tema.py` con `TITULO` y una función
`correr(nav, r)` que llame `r.caso('descripción', condición, detalle_si_falla)`.
`correr.py` lo encuentra solo.
