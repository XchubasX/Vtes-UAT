# Resultados de las pruebas

**✅ TODO BIEN** — 15 de 15 casos pasaron.

- Fecha: 03/10/2026 11:54 (hora de Ciudad de México)
- Versión probada: `177d6dd` + cambios aún sin guardar
- Duración: 1 s
- Grupos corridos: solo los que contienen «cloudflare»
- Cómo se prueba: navegador automatizado con Firebase simulado (no toca datos reales). No sustituye la revisión en el sitio de pruebas: estilos y servicios de Google reales solo se ven ahí.

## Resumen por grupo

| # | Grupo | Casos | Resultado |
|---|---|---|---|
| 1 | Cloudflare: enlaces de ciudad en GitHub y en dominio propio; qué se publica | 15 | ✅ |

## Todos los casos

### 1. Cloudflare: enlaces de ciudad en GitHub y en dominio propio; qué se publica

| # | Caso | Resultado |
|---|---|---|
| 1 | 404.html tiene la función que calcula a dónde redirigir | ✅ |
| 2 | 404: GitHub, sitio real con ciudad → /Organizador-Vtes/?city=Zaragoza | ✅ |
| 3 | 404: GitHub, sitio de pruebas con ciudad → /Vtes-UAT/?city=Zaragoza | ✅ |
| 4 | 404: GitHub, ciudad con acento y espacio → /Vtes-UAT/?city=Ciudad%20de%20M%C3%A9xico | ✅ |
| 5 | 404: GitHub, ciudad con diagonal final → /Vtes-UAT/?city=Zaragoza | ✅ |
| 6 | 404: GitHub, página que no existe sin ciudad → /Vtes-UAT/ | ✅ |
| 7 | 404: Cloudflare pages.dev con ciudad → /?city=Zaragoza | ✅ |
| 8 | 404: Dominio propio con ciudad → /?city=Zaragoza | ✅ |
| 9 | 404: Dominio propio con www y acento → /?city=M%C3%A1laga | ✅ |
| 10 | 404: Dominio propio, raíz → / | ✅ |
| 11 | el script de publicación de Cloudflare termina sin errores | ✅ |
| 12 | se publican las páginas y archivos del sitio | ✅ |
| 13 | NO se publica la carpeta de pruebas ni archivos internos | ✅ |
| 14 | wrangler.jsonc: publica la carpeta "publicado" y usa 404.html para lo que no existe | ✅ |
| 15 | se publican todos los archivos de js/ | ✅ |
