#!/bin/bash
# Lo ejecuta Cloudflare Pages cada vez que hay un cambio en GitHub.
# Copia SOLO los archivos del sitio a la carpeta "publicado" (la que Cloudflare pone en línea);
# deja fuera las pruebas automáticas y los archivos internos del repositorio.
# Configuración en Cloudflare: comando de construcción "bash cloudflare-publicar.sh",
# carpeta de salida "publicado".
set -e
rm -rf publicado
mkdir publicado
for f in *; do
  case "$f" in
    publicado|pruebas|README.md|_config.yml|cloudflare-publicar.sh) ;;
    *) cp -r "$f" publicado/ ;;
  esac
done
echo "Archivos publicados:"; ls -R publicado
