# Resultados de las pruebas

**✅ TODO BIEN** — 22 de 22 casos pasaron.

- Fecha: 01/10/2026 09:36 (hora de Ciudad de México)
- Versión probada: `104d54a` + cambios aún sin guardar
- Duración: 6 s
- Grupos corridos: solo los que contienen «privadas»
- Cómo se prueba: navegador automatizado con Firebase simulado (no toca datos reales). No sustituye la revisión en el sitio de pruebas: estilos y servicios de Google reales solo se ven ahí.

## Resumen por grupo

| # | Grupo | Casos | Resultado |
|---|---|---|---|
| 1 | Mesas privadas: plegadas al final de la lista | 22 | ✅ |

## Todos los casos

### 1. Mesas privadas: plegadas al final de la lista

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
| 18 | al cerrar "Mesa creada", la privada nueva aparece desplegada | ✅ |
| 19 | al volver a abrir el formulario la casilla está desmarcada | ✅ |
| 20 | presencial: la casilla no aparece | ✅ |
| 21 | sin errores de JavaScript (mesas privadas) | ✅ |
| 22 | enlace directo (#mesa-…) a una privada la abre desplegada | ✅ |
