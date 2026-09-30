# Vtes-UAT

Sitio de pruebas del Organizador VTES. Es una copia del sitio real (Organizador-Vtes)
conectada a la base de datos de pruebas `vtes-uat`, no a la real (`vtes-scheduler`).
Aquí se prueban los cambios antes de pasarlos al sitio real.

## Qué cambia entre este sitio y el real

Solo el archivo `config.js` (proyecto de Firebase, clave de reCAPTCHA y `esPruebas: true`,
que muestra la franja naranja). Todos los demás archivos son idénticos en los dos repositorios:
para pasar un cambio al sitio real se copian tal cual, sin tocar `config.js`.

Al cambiar `config.js` o `comun.js`, subir el número `?v=` con el que las páginas los cargan,
para que los navegadores no usen una copia vieja.
